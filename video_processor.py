# import cv2
# import numpy as np
# import torch
# from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
# import google.generativeai as genai
# import librosa
# from PIL import Image
# import os
# from tqdm import tqdm
# import subprocess
# import soundfile as sf

# class VideoProcessor:
#     def __init__(self, google_api_key):
#         # Configure Gemini
#         genai.configure(api_key=google_api_key)
#         self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
#         # Initialize wav2vec2 for speech recognition
#         self.audio_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
#         self.audio_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    
#     def extract_audio_ffmpeg(self, video_path):
#         try:
#             temp_audio_path = "temp_audio.wav"
            
#             command = [
#                 'ffmpeg',
#                 '-i', video_path,
#                 '-ab', '160k',
#                 '-ac', '2',
#                 '-ar', '16000',
#                 '-vn', temp_audio_path,
#                 '-y'
#             ]
            
#             subprocess.run(command, check=True, capture_output=True)
#             waveform, sample_rate = librosa.load(temp_audio_path, sr=16000)
#             os.remove(temp_audio_path)
            
#             return waveform, sample_rate
            
#         except Exception as e:
#             print(f"Error extracting audio: {str(e)}")
#             return None, None
            
#     def transcribe_audio(self, waveform):
#         try:
#             inputs = self.audio_processor(
#                 waveform, 
#                 sampling_rate=16000, 
#                 return_tensors="pt", 
#                 padding=True
#             )
            
#             with torch.no_grad():
#                 logits = self.audio_model(inputs.input_values).logits
            
#             predicted_ids = torch.argmax(logits, dim=-1)
#             transcription = self.audio_processor.batch_decode(predicted_ids)
            
#             return transcription[0]
#         except Exception as e:
#             print(f"Error transcribing audio: {str(e)}")
#             return ""
    
#     def extract_frames(self, video_path, num_frames=5):
#         frames = []
#         cap = cv2.VideoCapture(video_path)
#         total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#         frame_indices = np.linspace(0, total_frames-1, num_frames, dtype=int)
        
#         for idx in frame_indices:
#             cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
#             ret, frame = cap.read()
#             if ret:
#                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 frames.append(Image.fromarray(frame))
                
#         cap.release()
#         return frames
    
#     def analyze_frames(self, frames):
#         descriptions = []
        
#         for frame in tqdm(frames, desc="Analyzing frames"):
#             try:
#                 prompt = (
#                     "Analyze this product image and provide a detailed e-commerce style description.\n"
#                     "Include:\n"
#                     "1. Visual characteristics\n"
#                     "2. Notable features\n"
#                     "3. Potential uses\n"
#                     "4. Any visible technical specifications\n"
#                     "Keep the description professional and engaging."
#                 )
                
#                 response = self.model.generate_content([prompt, frame])
#                 descriptions.append(response.text)
                
#             except Exception as e:
#                 print(f"Error analyzing frame: {str(e)}")
#                 descriptions.append("")
            
#         return descriptions
    
#     def generate_final_description(self, frame_descriptions, audio_transcription=""):
#         try:
#             prompt = (
#                 "Based on the following frame descriptions and audio transcription, create a comprehensive "
#                 "e-commerce product description:\n\n"
#                 f"Visual Descriptions:\n{chr(10).join(frame_descriptions)}\n\n"
#                 f"Audio Transcription:\n{audio_transcription}\n\n"
#                 "Please provide a well-structured description that includes:\n"
#                 "1. Product overview\n"
#                 "2. Key features and benefits\n"
#                 "3. Technical specifications\n"
#                 "4. Recommended uses\n"
#                 "5. Notable information from the audio narration"
#             )
            
#             response = self.model.generate_content(prompt)
#             return response.text
            
#         except Exception as e:
#             print(f"Error generating final description: {str(e)}")
#             return "Error generating description"

#     def process_video(self, video_path):
#         try:
#             print("Extracting audio...")
#             waveform, _ = self.extract_audio_ffmpeg(video_path)
#             audio_transcription = ""
#             if waveform is not None:
#                 print("Transcribing audio...")
#                 audio_transcription = self.transcribe_audio(waveform)
            
#             print("Extracting frames...")
#             frames = self.extract_frames(video_path)
#             print("Analyzing frames...")
#             frame_descriptions = self.analyze_frames(frames)
            
#             print("Generating final description...")
#             final_description = self.generate_final_description(
#                 frame_descriptions, 
#                 audio_transcription
#             )
            
#             return {
#                 'status': 'success',
#                 'frame_descriptions': frame_descriptions,
#                 'audio_transcription': audio_transcription,
#                 'final_description': final_description
#             }
            
#         except Exception as e:
#             return {
#                 'status': 'error',
#                 'message': str(e)
#             }

# def main():
#     # Your Google API key
#     GOOGLE_API_KEY = " AIzaSyBCHP3hO3pLjqeSoyibkzn3C7tiquvMaCA"
    
#     # Initialize processor
#     processor = VideoProcessor(GOOGLE_API_KEY)
    
#     # Process a video
#     video_path = "A:/Users/VARSHA/Downloads/invideo-ai-1080 DIY in 30_ Quick Flower Vase 2023-11-14.mp4"
#     result = processor.process_video(video_path)
    
#     if result['status'] == 'success':
#         print("\nAudio Transcription:")
#         print("-------------------")
#         print(result['audio_transcription'])
        
#         print("\nFinal Product Description:")
#         print("-------------------------")
#         print(result['final_description'])
        
#         # Save results to a file
#         with open('video_analysis_results.txt', 'w', encoding='utf-8') as f:
#             f.write("AUDIO TRANSCRIPTION:\n")
#             f.write("-------------------\n")
#             f.write(result['audio_transcription'])
#             f.write("\n\nFINAL PRODUCT DESCRIPTION:\n")
#             f.write("-------------------------\n")
#             f.write(result['final_description'])
            
#     else:
#         print(f"Error processing video: {result['message']}")

# if __name__ == "__main__":
#     main()



























import cv2
import numpy as np
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import google.generativeai as genai
import librosa
from PIL import Image
import os
from tqdm import tqdm
import subprocess
import soundfile as sf
from pathlib import Path
import asyncio
import logging
import time
import yt_dlp as youtube_dl
import backoff
import aiofiles
import aiohttp
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def handle_rate_limit(max_tries=5, initial_wait=5):
    def decorator(func):
        @wraps(func)
        @backoff.on_exception(
            backoff.expo,
            Exception,
            max_tries=max_tries,
            giveup=lambda e: not (isinstance(e, Exception) and "429" in str(e)),
            base=2,
            factor=5
        )
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator

class TokenBucket:
    def __init__(self, tokens_per_second=0.1, max_tokens=30):  # Reduced rate significantly
        self.tokens_per_second = tokens_per_second
        self.max_tokens = max_tokens
        self.tokens = max_tokens
        self.last_update = time.time()
        self.lock = asyncio.Lock()
        self.waiting = False
    
    async def acquire(self):
        async with self.lock:
            now = time.time()
            time_passed = now - self.last_update
            self.tokens = min(
                self.max_tokens,
                self.tokens + time_passed * self.tokens_per_second
            )
            self.last_update = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False
    
    async def wait(self):
        while not await self.acquire():
            self.waiting = True
            await asyncio.sleep(10)  # Increased sleep time
        self.waiting = False

class VideoProcessor:
    def __init__(self, google_api_key):
        self.api_key = google_api_key
        self.rate_limiter = TokenBucket(tokens_per_second=0.1)
        
        # Configure Gemini
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Set FFmpeg path
        self.ffmpeg_path = r"C:/ProgramData/chocolatey/lib/ffmpeg/tools/ffmpeg/bin/ffmpeg.exe"
        if not os.path.exists(self.ffmpeg_path):
            raise RuntimeError(f"FFmpeg not found at: {self.ffmpeg_path}")
        logger.info(f"FFmpeg found at: {self.ffmpeg_path}")
        
        # Initialize wav2vec2 for speech recognition
        self.audio_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
        self.audio_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
        
        # Setup temp directory
        self._setup_temp_dir()
    
    def _setup_temp_dir(self):
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
    
    def _download_with_ytdl(self, ydl_opts, url):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                return True
            except Exception as e:
                logger.error(f"YouTube-DL error: {str(e)}")
                return False
    
    async def download_video(self, video_url):
        try:
            temp_path = self.temp_dir / f"{abs(hash(video_url))}.mp4"
            ydl_opts = {
                'format': 'best',
                'outtmpl': str(temp_path),
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True
            }
            
            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(
                None, 
                lambda: self._download_with_ytdl(ydl_opts, video_url)
            )
            
            if success and temp_path.exists():
                logger.info(f"Successfully downloaded video to {temp_path}")
                return temp_path
            
            logger.error("Failed to download video")
            return None
            
        except Exception as e:
            logger.error(f"Error downloading video: {str(e)}")
            return None
    
    async def _extract_audio(self, video_path):
        try:
            if not os.path.exists(str(video_path)):
                raise FileNotFoundError(f"Video file not found: {video_path}")
                
            temp_audio_path = self.temp_dir / "temp_audio.wav"
            
            command = [
                str(self.ffmpeg_path),  # Use the full FFmpeg path
                '-i', str(video_path),
                '-ab', '160k',
                '-ac', '2',
                '-ar', '16000',
                '-vn', str(temp_audio_path),
                '-y'
            ]
            
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"FFmpeg error: {stderr.decode() if stderr else 'Unknown error'}")
                return None, None
            
            if not os.path.exists(str(temp_audio_path)):
                logger.error("Audio extraction failed: output file not created")
                return None, None
                
            waveform, sample_rate = librosa.load(str(temp_audio_path), sr=16000)
            
            try:
                if os.path.exists(str(temp_audio_path)):
                    os.remove(str(temp_audio_path))
            except Exception as e:
                logger.warning(f"Failed to delete temporary audio file: {str(e)}")
            
            return waveform, sample_rate
            
        except Exception as e:
            logger.error(f"Error extracting audio: {str(e)}")
            return None, None

    
    async def _transcribe_audio(self, waveform):
        try:
            inputs = self.audio_processor(
                waveform, 
                sampling_rate=16000, 
                return_tensors="pt", 
                padding=True
            )
            
            with torch.no_grad():
                logits = self.audio_model(inputs.input_values).logits
            
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.audio_processor.batch_decode(predicted_ids)
            
            return transcription[0]
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            return ""
    
    async def _extract_frames(self, video_path, num_frames=5):
        frames = []
        try:
            cap = cv2.VideoCapture(str(video_path))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if total_frames == 0:
                logger.error("No frames found in video")
                return frames
            
            frame_indices = np.linspace(0, total_frames-1, num_frames, dtype=int)
            
            for idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(Image.fromarray(frame))
                else:
                    logger.warning(f"Failed to read frame at index {idx}")
                    
        except Exception as e:
            logger.error(f"Error extracting frames: {str(e)}")
            
        finally:
            if 'cap' in locals():
                cap.release()
                
        return frames
    
    @handle_rate_limit(max_tries=3, initial_wait=2)
    async def _analyze_frame(self, frame):
        await self.rate_limiter.wait()
        
        prompt = (
            "Analyze this product image and provide a detailed e-commerce style description.\n"
            "Include:\n"
            "1. Visual characteristics\n"
            "2. Notable features\n"
            "3. Potential uses\n"
            "4. Any visible technical specifications\n"
            "Keep the description professional and engaging."
        )
        
        response = self.model.generate_content([prompt, frame])
        return response.text
    
    async def _analyze_frames(self, frames):
        descriptions = []
        
        for frame in tqdm(frames, desc="Analyzing frames"):
            try:
                description = await self._analyze_frame(frame)
                descriptions.append(description)
                # Add small delay between frames
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error analyzing frame: {str(e)}")
                descriptions.append("")
                # Add longer delay after error
                await asyncio.sleep(5)
        
        return descriptions
    
    @handle_rate_limit(max_tries=3, initial_wait=2)
    async def _generate_description(self, frame_descriptions, audio_transcription=""):
        await self.rate_limiter.wait()
        
        prompt = (
            "Based on the following frame descriptions and audio transcription, create a comprehensive "
            "e-commerce product description:\n\n"
            f"Visual Descriptions:\n{chr(10).join(frame_descriptions)}\n\n"
            f"Audio Transcription:\n{audio_transcription}\n\n"
            "Please provide a well-structured description that includes:\n"
            "1. Product overview\n"
            "2. Key features and benefits\n"
            "3. Technical specifications\n"
            "4. Recommended uses\n"
            "5. Notable information from the audio narration"
        )
        
        response = self.model.generate_content(prompt)
        return response.text
    
    async def process_video(self, video_url):
        try:
            # Download video
            video_path = await self.download_video(video_url)
            if not video_path:
                return {
                    'status': 'error',
                    'message': 'Failed to download video'
                }
            
            try:
                logger.info("Extracting audio...")
                waveform, sr = await self._extract_audio(video_path)
                
                audio_transcription = ""
                if waveform is not None:
                    logger.info("Transcribing audio...")
                    audio_transcription = await self._transcribe_audio(waveform)
                
                logger.info("Extracting frames...")
                frames = await self._extract_frames(video_path)
                
                if not frames:
                    return {
                        'status': 'error',
                        'message': 'Failed to extract frames from video'
                    }
                
                logger.info("Analyzing frames...")
                frame_descriptions = await self._analyze_frames(frames)
                
                logger.info("Generating final description...")
                final_description = await self._generate_description(
                    frame_descriptions,
                    audio_transcription
                )
                
                return {
                    'status': 'success',
                    'frame_descriptions': frame_descriptions,
                    'audio_transcription': audio_transcription,
                    'final_description': final_description
                }
                
            finally:
                # Cleanup
                try:
                    video_path.unlink()
                except Exception as e:
                    logger.warning(f"Failed to cleanup video file: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
# async def main():
#     try:
#         GOOGLE_API_KEY = "AIzaSyByq6McW4oN7KqJcWFxqAGIn3yzuU5HDgk"
#         processor = VideoProcessor(GOOGLE_API_KEY)
        
#         video_urls = [
#             "https://www.youtube.com/watch?v=TzPS6ELoZ1I",
#             # Add backup URLs if needed
#         ]
        
#         max_retries = 3
#         for retry in range(max_retries):
#             for video_url in video_urls:
#                 try:
#                     logger.info(f"Attempt {retry + 1}/{max_retries} - Processing video: {video_url}")
#                     result = await processor.process_video(video_url)
                    
#                     if result['status'] == 'success':
#                         logger.info("Successfully processed video")
#                         save_results(result)
#                         return
                    
#                     logger.warning(f"Failed to process video: {result['message']}")
#                     await asyncio.sleep(30)  # Wait 30 seconds before next attempt
                    
#                 except Exception as e:
#                     logger.error(f"Error processing video {video_url}: {str(e)}")
#                     await asyncio.sleep(30)
#                     continue
            
#             logger.warning(f"Retry {retry + 1} failed, waiting before next attempt...")
#             await asyncio.sleep(60)  # Wait 1 minute between retry cycles
        
#         logger.error("All retries exhausted. Process failed.")
        
#     except Exception as e:
#         logger.error(f"Fatal error in main: {str(e)}")
#         raise

# def save_results(result):
#     """Save processing results to file"""
#     try:
#         with open('video_analysis_results.txt', 'w', encoding='utf-8') as f:
#             f.write("AUDIO TRANSCRIPTION:\n")
#             f.write("-------------------\n")
#             f.write(result['audio_transcription'])
#             f.write("\n\nFINAL PRODUCT DESCRIPTION:\n")
#             f.write("-------------------------\n")
#             f.write(result['final_description'])
#         logger.info("Results saved successfully")
#     except Exception as e:
#         logger.error(f"Error saving results: {str(e)}")

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         logger.info("Process interrupted by user")
#     except Exception as e:
#         logger.error(f"Unhandled exception: {str(e)}")