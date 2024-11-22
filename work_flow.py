import os
import asyncio
import json
from datetime import datetime
import logging
from pathlib import Path
import asyncpraw
from googleapiclient.discovery import build
import aiohttp
from typing import Dict, List, Optional
import youtube_dl
from tenacity import retry, stop_after_attempt, wait_exponential
import uuid
from dataclasses import dataclass, asdict
from video_processor import VideoProcessor
from image_processor import ImageProcessor
import time

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(correlation_id)s] %(message)s'
)
logger = logging.getLogger(__name__)

class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'correlation_id'):
            record.correlation_id = 'NO_CORR_ID'
        return True

logger.addFilter(CorrelationIdFilter())

@dataclass
class ProcessingMetrics:
    start_time: datetime
    end_time: Optional[datetime] = None
    total_posts: int = 0
    successful_posts: int = 0
    failed_posts: int = 0
    api_calls: int = 0
    api_errors: int = 0
    
    def calculate_duration(self):
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    def to_dict(self):
        return asdict(self)

class RateLimitHandler:
    def __init__(self, max_retries=3, base_delay=1, max_delay=32):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        
    async def execute_with_backoff(self, func, *args, correlation_id=None, **kwargs):
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if "429" in str(e) or "Resource exhausted" in str(e):
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    logger.warning(
                        f"Rate limit hit. Waiting {delay}s before retry...",
                        extra={'correlation_id': correlation_id}
                    )
                    await asyncio.sleep(delay)
                    continue
                raise e
        raise Exception("Max retries exceeded")

class AsyncSocialMediaConnector:
    def __init__(self, credentials: Dict):
        self.credentials = credentials
        self.rate_limiter = RateLimitHandler()
        self._init_clients()
    
    def _init_clients(self):
        self.reddit_client = asyncpraw.Reddit(
            client_id=self.credentials['reddit']['client_id'],
            client_secret=self.credentials['reddit']['client_secret'],
            user_agent="ProductAnalyzer/1.0"
        )
        
        self.youtube_client = build(
            'youtube', 'v3', 
            developerKey=self.credentials['youtube']['api_key']
        )
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        await self.reddit_client.close()

    async def fetch_reddit_content(self, subreddits: List[str], limit: int = 10, correlation_id: str = None) -> List[Dict]:
        posts = []
        
        for subreddit_name in subreddits:
            try:
                subreddit = await self.reddit_client.subreddit(subreddit_name)
                async for submission in subreddit.hot(limit=limit):
                    content_type = 'text'
                    content_url = None
                    
                    if submission.is_video:
                        content_type = 'video'
                        content_url = submission.media['reddit_video']['fallback_url']
                    elif hasattr(submission, 'url') and any(
                        submission.url.endswith(ext) for ext in ('.jpg', '.png', '.gif')
                    ):
                        content_type = 'image'
                        content_url = submission.url
                    
                    post_data = {
                        'id': str(submission.id),
                        'platform': 'reddit',
                        'content_type': content_type,
                        'content_url': content_url,
                        'title': submission.title,
                        'text': submission.selftext if hasattr(submission, 'selftext') else '',
                        'score': submission.score,
                        'created_utc': datetime.fromtimestamp(submission.created_utc),
                        'num_comments': submission.num_comments,
                        'author': str(submission.author),
                        'subreddit': subreddit_name,
                        'permalink': f"https://reddit.com{submission.permalink}",
                        'url': submission.url
                    }
                    
                    posts.append(post_data)
                    logger.info(
                        f"Found Reddit post: {submission.title[:50]}...",
                        extra={'correlation_id': correlation_id}
                    )
                    
            except Exception as e:
                logger.error(
                    f"Error fetching from subreddit {subreddit_name}: {str(e)}",
                    extra={'correlation_id': correlation_id}
                )
                continue
                
        return posts

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def fetch_youtube_content(self, search_query: str, limit: int = 10, correlation_id: str = None) -> List[Dict]:
        try:
            search_request = self.youtube_client.search().list(
                q=search_query,
                part='snippet',
                maxResults=limit,
                type='video'
            )
            
            # Execute synchronously since Google API client doesn't support async
            search_response = search_request.execute()
            
            posts = []
            for item in search_response.get('items', []):
                video_id = item['id']['videoId']
                
                # Get video statistics
                video_request = self.youtube_client.videos().list(
                    part='statistics',
                    id=video_id
                )
                video_response = video_request.execute()
                
                if video_response['items']:
                    stats = video_response['items'][0]['statistics']
                    
                    post_data = {
                        'id': video_id,
                        'platform': 'youtube',
                        'content_type': 'video',
                        'content_url': f"https://www.youtube.com/watch?v={video_id}",
                        'title': item['snippet']['title'],
                        'text': item['snippet']['description'],
                        'created_utc': datetime.strptime(
                            item['snippet']['publishedAt'], 
                            '%Y-%m-%dT%H:%M:%SZ'
                        ),
                        'views': int(stats.get('viewCount', 0)),
                        'likes': int(stats.get('likeCount', 0)),
                        'comments': int(stats.get('commentCount', 0)),
                        'author': item['snippet']['channelTitle']
                    }
                    
                    posts.append(post_data)
                    logger.info(
                        f"Found YouTube video: {item['snippet']['title'][:50]}...",
                        extra={'correlation_id': correlation_id}
                    )
            
            return posts
            
        except Exception as e:
            logger.error(
                f"Error fetching YouTube content: {str(e)}",
                extra={'correlation_id': correlation_id}
            )
            return []
        


class ContentProcessor:
    def __init__(self, google_api_key: str):
        self.video_processor = VideoProcessor(google_api_key)
        self.image_processor = ImageProcessor()
        self.rate_limiter = RateLimitHandler()
        self.batch_size = 5  # Process in smaller batches
        
    async def _process_video_with_retry(self, post: Dict, correlation_id: str) -> Dict:
        try:
            result = await self.rate_limiter.execute_with_backoff(
                self.video_processor.process_video,
                post['content_url'],
                correlation_id=correlation_id
            )
            return {
                'post_id': post['id'],
                'processed_content': result,
                'processed_date': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(
                f"Error processing video {post['id']}: {str(e)}",
                extra={'correlation_id': correlation_id}
            )
            return None

    async def _process_image_with_retry(self, post: Dict, correlation_id: str) -> Dict:
        try:
            result = await self.rate_limiter.execute_with_backoff(
                self.image_processor.analyze_product,
                post['content_url'],
                correlation_id=correlation_id
            )
            return {
                'post_id': post['id'],
                'processed_content': result,
                'processed_date': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(
                f"Error processing image {post['id']}: {str(e)}",
                extra={'correlation_id': correlation_id}
            )
            return None

    async def _process_text_with_retry(self, post: Dict, correlation_id: str) -> Dict:
        try:
            result = await self.rate_limiter.execute_with_backoff(
                self.image_processor.text_processor.analyze_text,
                post['text'],
                correlation_id=correlation_id
            )
            return {
                'post_id': post['id'],
                'processed_content': result,
                'processed_date': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(
                f"Error processing text {post['id']}: {str(e)}",
                extra={'correlation_id': correlation_id}
            )
            return None
        
    async def process_content(self, posts: List[Dict], metrics: ProcessingMetrics) -> List[Dict]:
        processed_posts = []
        
        # Process in batches
        for i in range(0, len(posts), self.batch_size):
            batch = posts[i:i + self.batch_size]
            
            # Process batch concurrently
            tasks = []
            for post in batch:
                correlation_id = str(uuid.uuid4())  # Generate unique correlation ID for each post
                
                if post['content_type'] == 'video':
                    task = self._process_video_with_retry(post, correlation_id)
                elif post['content_type'] == 'image':
                    task = self._process_image_with_retry(post, correlation_id)
                else:
                    task = self._process_text_with_retry(post, correlation_id)
                tasks.append(task)
            
            # Wait for batch to complete
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Update metrics and process results
            for result in batch_results:
                metrics.total_posts += 1
                
                if isinstance(result, Exception):
                    metrics.failed_posts += 1
                    metrics.api_errors += 1
                    logger.error(f"Batch processing error: {str(result)}")
                    continue
                    
                if result and result.get('processed_content', {}).get('status') == 'success':
                    processed_posts.append(result)
                    metrics.successful_posts += 1
                else:
                    metrics.failed_posts += 1
            
            # Add delay between batches
            await asyncio.sleep(2)
        
        return processed_posts


class ProductWorkflow:
    def __init__(self):
        self.setup_credentials()
        self.setup_directories()
        self.metrics = ProcessingMetrics(start_time=datetime.now())
        
    def setup_credentials(self):
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            'REDDIT_CLIENT_ID',
            'REDDIT_CLIENT_SECRET',
            'YOUTUBE_API_KEY',
            'GOOGLE_API_KEY'
        ]
        
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")
            
        self.credentials = {
            'reddit': {
                'client_id': os.getenv('REDDIT_CLIENT_ID'),
                'client_secret': os.getenv('REDDIT_CLIENT_SECRET')
            },
            'youtube': {
                'api_key': os.getenv('YOUTUBE_API_KEY')
            }
        }
        
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
    
    def setup_directories(self):
        dirs = ['data', 'temp', 'listings', 'logs', 'processed']
        for d in dirs:
            Path(d).mkdir(exist_ok=True)
    
    def _save_metrics(self):
        metrics_file = f'logs/metrics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(self.metrics.to_dict(), f, indent=2, default=str)
    
    async def run(self):
        correlation_id = str(uuid.uuid4())
        try:
            # Step 1: Collect content
            logger.info(
                "Step 1: Collecting content...",
                extra={'correlation_id': correlation_id}
            )
            
            async with AsyncSocialMediaConnector(self.credentials) as connector:
                subreddits = ['ProductReviews', 'gadgets', 'BuyItForLife']
                youtube_queries = ['product review 2024', 'new product unboxing']
                
                reddit_posts = await connector.fetch_reddit_content(
                    subreddits,
                    correlation_id=correlation_id
                )
                
                youtube_posts = []
                for query in youtube_queries:
                    posts = await connector.fetch_youtube_content(
                        query,
                        correlation_id=correlation_id
                    )
                    youtube_posts.extend(posts)
                
                all_posts = reddit_posts + youtube_posts
                self.all_posts = all_posts  # Store for metrics calculation
            
            # Save raw data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_data_file = f'data/raw_posts_{timestamp}.json'
            with open(raw_data_file, 'w', encoding='utf-8') as f:
                json.dump(all_posts, f, indent=2, default=str)
            
            # Step 2: Process content
            logger.info(
                "Step 2: Processing content...",
                extra={'correlation_id': correlation_id}
            )
            
            processor = ContentProcessor(self.google_api_key)
            processed_posts = await processor.process_content(all_posts, self.metrics)
            
            # Save processed data
            processed_file = f'processed/processed_posts_{timestamp}.json'
            with open(processed_file, 'w', encoding='utf-8') as f:
                json.dump(processed_posts, f, indent=2, default=str)
            
            # Update metrics and generate summary
            self.metrics.end_time = datetime.now()
            self._save_metrics()
            self._generate_summary()
            
            logger.info(
                "Workflow completed successfully",
                extra={'correlation_id': correlation_id}
            )
            
        except Exception as e:
            logger.error(
                f"Workflow error: {str(e)}",
                extra={'correlation_id': correlation_id}
            )
            # Update metrics for failure case
            self.metrics.end_time = datetime.now()
            self.metrics.api_errors += 1
            self._save_metrics()
            raise
            
        finally:
            # Cleanup any temporary files
            temp_dir = Path('temp')
            if temp_dir.exists():
                for file in temp_dir.glob('*'):
                    try:
                        file.unlink()
                    except Exception as e:
                        logger.warning(
                            f"Failed to clean up temporary file {file}: {str(e)}",
                            extra={'correlation_id': correlation_id}
                        )

    def _generate_summary(self):
            """Generate and print workflow summary with detailed metrics"""
            duration = self.metrics.calculate_duration()
            
            print("\nWorkflow Summary:")
            print("-" * 50)
            print(f"Total Runtime: {duration:.2f} seconds")
            print(f"Total posts collected: {self.metrics.total_posts}")
            print(f"Successfully processed: {self.metrics.successful_posts}")
            print(f"Failed to process: {self.metrics.failed_posts}")
            
            # Calculate success rate
            if self.metrics.total_posts > 0:
                success_rate = (self.metrics.successful_posts / self.metrics.total_posts) * 100
                print(f"Processing success rate: {success_rate:.1f}%")
            
            # API metrics
            print(f"\nAPI Performance:")
            print(f"Total API calls: {self.metrics.api_calls}")
            print(f"API errors: {self.metrics.api_errors}")
            if self.metrics.api_calls > 0:
                error_rate = (self.metrics.api_errors / self.metrics.api_calls) * 100
                print(f"API error rate: {error_rate:.1f}%")
            
            # Platform breakdown
            platforms = {}
            content_types = {}
            
            for post in self.all_posts:
                platform = post['platform']
                content_type = post['content_type']
                
                platforms[platform] = platforms.get(platform, 0) + 1
                content_types[content_type] = content_types.get(content_type, 0) + 1
            
            print("\nPosts by platform:")
            for platform, count in platforms.items():
                print(f"- {platform}: {count}")
            
            print("\nContent types processed:")
            for type_, count in content_types.items():
                print(f"- {type_}: {count}")
                
            # Save summary to file
            summary_file = f'logs/summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("Workflow Summary\n")
                f.write("-" * 50 + "\n")
                f.write(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Runtime: {duration:.2f} seconds\n")
                f.write(f"Total Posts: {self.metrics.total_posts}\n")
                f.write(f"Successful: {self.metrics.successful_posts}\n")
                f.write(f"Failed: {self.metrics.failed_posts}\n")
                f.write(f"Success Rate: {success_rate:.1f}%\n")
                f.write("\nAPI Metrics:\n")
                f.write(f"Total API Calls: {self.metrics.api_calls}\n")
                f.write(f"API Errors: {self.metrics.api_errors}\n")
                f.write(f"Error Rate: {error_rate:.1f}%\n")

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

async def main():
    """Main entry point for the workflow"""
    try:
        # Set up logging for the main process
        correlation_id = str(uuid.uuid4())
        logger.info(
            "Starting product analysis workflow",
            extra={'correlation_id': correlation_id}
        )
        
        # Initialize and run workflow
        workflow = ProductWorkflow()
        await workflow.run()
        
    except Exception as e:
        logger.error(
            f"Fatal error in main workflow: {str(e)}",
            extra={'correlation_id': correlation_id}
        )
        raise
    finally:
        logger.info(
            "Workflow completed",
            extra={'correlation_id': correlation_id}
        )

if __name__ == "__main__":
    # Set up asyncio event loop with proper error handling
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Workflow interrupted by user")
    except Exception as e:
        logger.error(f"Unhandled exception in main loop: {str(e)}")
        raise
    finally:
        loop.close()