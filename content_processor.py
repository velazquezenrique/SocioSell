
import logging
from typing import Dict, Optional
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class ContentProcessor:
    def __init__(self, db, image_processor, video_processor):
        self.db = db
        self.image_processor = image_processor
        self.video_processor = video_processor
    
    async def match_product_reference(self, analysis: Dict) -> Optional[Dict]:
        """Match analysis results with product reference database"""
        try:
            # Search by category
            category_matches = await self.db.product_references.find({
                "category": {"$regex": analysis.get("category", ""), "$options": "i"}
            }).to_list(length=10)
            
            if not category_matches:
                return None
            
            best_match = None
            highest_score = 0
            
            # Score each potential match
            for reference in category_matches:
                score = 0
                
                # Match keywords
                analysis_keywords = set(k.lower() for k in analysis.get("search_keywords", []))
                reference_keywords = set(k.lower() for k in reference.get("keywords", []))
                keyword_matches = len(analysis_keywords.intersection(reference_keywords))
                score += keyword_matches * 2
                
                # Match features
                analysis_features = set(f.lower() for f in analysis.get("key_features", []))
                reference_features = set(f.lower() for f in reference.get("common_features", []))
                feature_matches = len(analysis_features.intersection(reference_features))
                score += feature_matches
                
                # Price range match
                if analysis.get("price"):
                    try:
                        price = float(analysis["price"].replace("$", "").replace(",", ""))
                        for range_name, range_values in reference["price_ranges"].items():
                            if range_values["min"] <= price <= range_values["max"]:
                                score += 3
                                break
                    except (ValueError, KeyError):
                        pass
                
                if score > highest_score:
                    highest_score = score
                    best_match = reference
            
            return best_match if highest_score > 3 else None
            
        except Exception as e:
            logger.error(f"Error matching product reference: {e}")
            return None
    
    async def generate_listing(self, analysis: Dict, reference: Dict) -> Dict:
        """Generate comprehensive product listing using analysis and reference data"""
        try:
            # Combine specifications
            specifications = {}
            specifications.update(reference["base_specifications"])
            specifications.update(analysis.get("specifications", {}))
            
            # Calculate price category
            price_category = "mid_range"
            if analysis.get("price"):
                try:
                    price = float(analysis["price"].replace("$", "").replace(",", ""))
                    for category, range_values in reference["price_ranges"].items():
                        if range_values["min"] <= price <= range_values["max"]:
                            price_category = category
                            break
                except (ValueError, KeyError):
                    pass
            
            # Generate listing
            listing = {
                "title": analysis.get("product_name", ""),
                "category": reference["category"],
                "subcategory": reference["subcategory"],
                "description": self._generate_description(analysis, reference),
                "price": analysis.get("price", f"${reference['price_ranges'][price_category]['min']:.2f}"),
                "features": self._combine_features(analysis, reference),
                "specifications": specifications,
                "keywords": list(set(reference["keywords"] + analysis.get("search_keywords", []))),
                "comparable_products": await self._find_comparable_products(reference),
                "created_at": datetime.utcnow()
            }
            
            return listing
            
        except Exception as e:
            logger.error(f"Error generating listing: {e}")
            return {}
    
    def _generate_description(self, analysis: Dict, reference: Dict) -> str:
        """Generate comprehensive product description"""
        description = analysis.get("description", "")
        
        # Add category-specific information
        description += f"\n\nThis {reference['subcategory']} comes with "
        description += ", ".join(reference["common_features"][:3]) + "."
        
        # Add price category context
        price_categories = {
            "budget": "affordable",
            "mid_range": "mid-range",
            "premium": "premium"
        }
        
        for category, range_values in reference["price_ranges"].items():
            try:
                price = float(analysis["price"].replace("$", "").replace(",", ""))
                if range_values["min"] <= price <= range_values["max"]:
                    description += f"\n\nThis {price_categories[category]} device offers excellent value for its feature set."
                    break
            except (ValueError, KeyError):
                pass
        
        return description
    
    def _combine_features(self, analysis: Dict, reference: Dict) -> list:
        """Combine and prioritize features from analysis and reference"""
        features = []
        
        # Add analysis features first
        features.extend(analysis.get("key_features", []))
        
        # Add complementary features from reference
        for feature in reference["common_features"]:
            if feature not in features:
                features.append(feature)
        
        return features[:10]  # Limit to top 10 features
    
    async def _find_comparable_products(self, reference: Dict) -> list:
        """Find comparable products in the same category and price range"""
        try:
            comparables = await self.db.product_listings.find({
                "category": reference["category"],
                "subcategory": reference["subcategory"]
            }).limit(5).to_list(length=5)
            
            return [
                {
                    "title": comp["title"],
                    "price": comp["price"],
                    "key_features": comp["features"][:3]
                }
                for comp in comparables
            ]
        except Exception as e:
            logger.error(f"Error finding comparable products: {e}")
            return []

    async def process_content(self, post_id: str):
        """Process social media content and generate listing"""
        try:
            # Get post
            post = await self.db.social_posts.find_one({"_id": post_id})
            if not post:
                return
            
            # Process content based on type
            if post["content_type"] == "image":
                analysis = await self.image_processor.analyze_product(post["content_url"])
            elif post["content_type"] == "video":
                analysis = await self.video_processor.process_video(post["content_url"])
            else:
                analysis = await self.image_processor.text_processor.analyze_text(post["caption"])
            
            if analysis["status"] == "success":
                # Match with product reference
                reference = await self.match_product_reference(analysis)
                
                if reference:
                    # Generate listing
                    listing = await self.generate_listing(analysis, reference)
                    listing["source_post_id"] = post_id
                    listing["status"] = "draft"
                    
                    # Save listing
                    await self.db.product_listings.insert_one(listing)
                    
                    # Update post
                    await self.db.social_posts.update_one(
                        {"_id": post_id},
                        {
                            "$set": {
                                "processed": True,
                                "analysis_result": analysis,
                                "reference_id": reference["_id"]
                            }
                        }
                    )
                    
                    logger.info(f"Successfully processed post {post_id}")
                else:
                    logger.warning(f"No matching product reference found for post {post_id}")
            else:
                logger.error(f"Processing failed for post {post_id}")
                
        except Exception as e:
            logger.error(f"Error processing content: {e}")
