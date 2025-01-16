from models.product import Product

# Sample Responses for Image Upload
SAMPLE_RESPONSES = {
    "headphones": {
        "product_id": "audio_123",
        "title": "Sony WH-1000XM4",
        "category": "Electronics",
        "description": "Premium noise-cancelling headphones",
        "price": "$349",
        "features": ["Active Noise Cancellation", "30-hour Battery Life", "Touch Controls"]
    },
    "shoes": {
        "product_id": "shoe_123",
        "title": "Nike Air Max 270",
        "category": "Fashion",
        "description": "Modern lifestyle sneakers",
        "price": "$150",
        "features": ["Air Unit Cushioning", "Breathable Mesh", "Comfortable Fit"]
    },
    # Add other sample responses...
                "lamp": {
                "product_id": "decor_123",
                "title": "Scandinavian Floor Lamp",
                "category": "Home Decor",
                "description": "Modern minimalist lighting",
                "price": "$199",
                "features": ["Adjustable Height", "Energy Efficient", "Natural Wood Base"]
            },
            "lipstick": {
                "product_id": "beauty_123",
                "title": "MAC Ruby Woo",
                "category": "Beauty",
                "description": "Classic matte red lipstick",
                "price": "$19",
                "features": ["Long-lasting", "Matte Finish", "Highly Pigmented"]
            },
            "basketball": {
                "product_id": "sports_123",
                "title": "Wilson Evolution",
                "category": "Sports",
                "description": "Official game basketball",
                "price": "$59.99",
                "features": ["Moisture-Wicking", "Superior Grip", "Indoor Use"]
            }
}

# Sample products
sample_products = [
    # Category: Electronics
    # Subcategory: Smartphones
    Product(
        title="Samsung Galaxy S24",
        category="Electronics",
        subcategory="Smartphones",
        features=["5G Connectivity", "AI-Enhanced Camera", "AMOLED Display", "Fast Charging", "Wireless Charging"],
        price_range="premium"
    ),
    Product(
        title="iPhone 15",
        category="Electronics",
        subcategory="Smartphones",
        features=["5G Connectivity", "AI-Enhanced Camera", "AMOLED Display", "Fast Charging", "Wireless Charging"],
        price_range="premium"
    ),
    # Subcategory: Wireless Earbuds
    Product(
        title="Apple AirPods Pro",
        category="Electronics",
        subcategory="Wireless Earbuds",
        features=["Active Noise Cancellation", "Touch Controls", "Wireless Charging Case", "Water Resistance", "Voice Assistant Support"],
        price_range="mid_range"
    ),
    Product(
        title="Samsung Galaxy Buds",
        category="Electronics",
        subcategory="Wireless Earbuds",
        features=["Active Noise Cancellation", "Touch Controls", "Wireless Charging Case", "Water Resistance", "Voice Assistant Support"],
        price_range="budget"
    ),
    # Category: Wearables
    # Subcategory: Smartwatches
    Product(
        title="Apple Watch Series 9",
        category="Wearables",
        subcategory="Smartwatches",
        features=["Health Monitoring", "Fitness Tracking", "GPS", "Always-On Display", "Water Resistance"],
        price_range="premium"
    ),
    Product(
        title="Samsung Galaxy Watch 6",
        category="Wearables",
        subcategory="Smartwatches",
        features=["Health Monitoring", "Fitness Tracking", "GPS", "Always-On Display", "Water Resistance"],
        price_range="mid_range"
    ),
    # Subcategory: Fitness Bands
    Product(
        title="Fitbit Charge 6",
        category="Wearables",
        subcategory="Fitness Bands",
        features=["Heart Rate Monitoring", "Step Tracking", "Sleep Analysis", "Long Battery Life", "Water Resistance"],
        price_range="budget"
    ),
    Product(
        title="Xiaomi Mi Band 8",
        category="Wearables",
        subcategory="Fitness Bands",
        features=["Heart Rate Monitoring", "Step Tracking", "Sleep Analysis", "Long Battery Life", "Water Resistance"],
        price_range="budget"
    ),
]

# Product Analytics
product_analytics = [
    {
        "title": "Samsung Galaxy S24",
        "sales_performance": {
            "total_sales": "$5M",
            "revenue": "$4.8M",
            "average_price": "$349",
            "growth_rate": "12%"
        },
        "customer_behavior": {
            "view_to_purchase_rate": "2:1",
            "cart_abandonment_rate": "25%",
            "repeat_purchase_rate": "15%",
            "average_rating": 4.7
        },
        "demographics": {
            "age_groups": {
                "18-24": "35%",
                "25-34": "45%",
                "35-44": "15%",
                "45+": "5%"
            },
            "top_locations": ["USA", "UK", "Germany", "South Korea"]
        },
        "marketing_metrics": {
            "click_through_rate": "1.2%",
            "conversion_rate": "5%",
            "return_on_ad_spend": "3.5",
            "social_media_engagement": "High"
        }
    },
    {
        "title": "iPhone 15",
        "sales_performance": {
            "total_sales": "$6M",
            "revenue": "$5.5M",
            "average_price": "$399",
            "growth_rate": "8%"
        },
        "customer_behavior": {
            "view_to_purchase_rate": "1.5:1",
            "cart_abandonment_rate": "20%",
            "repeat_purchase_rate": "18%",
            "average_rating": 4.8
        },
        "demographics": {
            "age_groups": {
                "18-24": "30%",
                "25-34": "50%",
                "35-44": "10%",
                "45+": "10%"
            },
            "top_locations": ["USA", "China", "Japan", "India"]
        },
        "marketing_metrics": {
            "click_through_rate": "1.0%",
            "conversion_rate": "4.5%",
            "return_on_ad_spend": "4.0",
            "social_media_engagement": "Moderate"
        }
    },
    {
        "title": "Apple AirPods Pro",
        "sales_performance": {
            "total_sales": "$2M",
            "revenue": "$1.9M",
            "average_price": "$249",
            "growth_rate": "18%"
        },
        "customer_behavior": {
            "view_to_purchase_rate": "3:1",
            "cart_abandonment_rate": "18%",
            "repeat_purchase_rate": "20%",
            "average_rating": 4.6
        },
        "demographics": {
            "age_groups": {
                "18-24": "40%",
                "25-34": "40%",
                "35-44": "10%",
                "45+": "10%"
            },
            "top_locations": ["USA", "UK", "Canada", "Australia"]
        },
        "marketing_metrics": {
            "click_through_rate": "1.5%",
            "conversion_rate": "6%",
            "return_on_ad_spend": "5.0",
            "social_media_engagement": "High"
        }
    },
    {
        "title": "Samsung Galaxy Buds",
        "sales_performance": {
            "total_sales": "$5M",
            "revenue": "$4.8M",
            "average_price": "$349",
            "growth_rate": "12%"
        },
        "customer_behavior": {
            "view_to_purchase_rate": "2:1",
            "cart_abandonment_rate": "25%",
            "repeat_purchase_rate": "15%",
            "average_rating": 4.7
        },
        "demographics": {
            "age_groups": {
                "18-24": "35%",
                "25-34": "45%",
                "35-44": "15%",
                "45+": "5%"
            },
            "top_locations": ["USA", "UK", "Germany", "South Korea"]
        },
        "marketing_metrics": {
            "click_through_rate": "1.2%",
            "conversion_rate": "5%",
            "return_on_ad_spend": "3.5",
            "social_media_engagement": "High"
        }
    },
    {
        "title": "Apple Watch Series 9",
        "sales_performance": {
            "total_sales": "$6M",
            "revenue": "$5.5M",
            "average_price": "$399",
            "growth_rate": "8%"
        },
        "customer_behavior": {
            "view_to_purchase_rate": "1.5:1",
            "cart_abandonment_rate": "20%",
            "repeat_purchase_rate": "18%",
            "average_rating": 4.8
        },
        "demographics": {
            "age_groups": {
                "18-24": "30%",
                "25-34": "50%",
                "35-44": "10%",
                "45+": "10%"
            },
            "top_locations": ["USA", "China", "Japan", "India"]
        },
        "marketing_metrics": {
            "click_through_rate": "1.0%",
            "conversion_rate": "4.5%",
            "return_on_ad_spend": "4.0",
            "social_media_engagement": "Moderate"
        }
    },
    {
        "title": "Samsung Galaxy Watch 6",
        "sales_performance": {
            "total_sales": "$2M",
            "revenue": "$1.9M",
            "average_price": "$249",
            "growth_rate": "18%"
        },
        "customer_behavior": {
            "view_to_purchase_rate": "3:1",
            "cart_abandonment_rate": "18%",
            "repeat_purchase_rate": "20%",
            "average_rating": 4.6
        },
        "demographics": {
            "age_groups": {
                "18-24": "40%",
                "25-34": "40%",
                "35-44": "10%",
                "45+": "10%"
            },
            "top_locations": ["USA", "UK", "Canada", "Australia"]
        },
        "marketing_metrics": {
            "click_through_rate": "1.5%",
            "conversion_rate": "6%",
            "return_on_ad_spend": "5.0",
            "social_media_engagement": "High"
        }
    },
    {
        "title": "Fitbit Charge 6",
        "sales_performance": {
            "total_sales": "$2.5M",
            "revenue": "$2.2M",
            "average_price": "$129",
            "growth_rate": "15%"
        },
        "customer_behavior": {
            "view_to_purchase_rate": "4:1",
            "cart_abandonment_rate": "12%",
            "repeat_purchase_rate": "25%",
            "average_rating": 4.7
        },
        "demographics": {
            "age_groups": {
                "18-24": "45%",
                "25-34": "40%",
                "35-44": "10%",
                "45+": "5%"
            },
            "top_locations": ["USA", "India", "UK", "Australia"]
        },
        "marketing_metrics": {
            "click_through_rate": "2.0%",
            "conversion_rate": "5.5%",
            "return_on_ad_spend": "4.2",
            "social_media_engagement": "Moderate"
        }
    },
    {
        "title": "Xiaomi Mi Band 8",
        "sales_performance": {
            "total_sales": "$1.8M",
            "revenue": "$1.6M",
            "average_price": "$79",
            "growth_rate": "10%"
        },
        "customer_behavior": {
            "view_to_purchase_rate": "3:1",
            "cart_abandonment_rate": "22%",
            "repeat_purchase_rate": "18%",
            "average_rating": 4.4
        },
        "demographics": {
            "age_groups": {
                "18-24": "40%",
                "25-34": "35%",
                "35-44": "15%",
                "45+": "10%"
            },
            "top_locations": ["USA", "China", "Brazil", "Russia"]
        },
        "marketing_metrics": {
            "click_through_rate": "1.8%",
            "conversion_rate": "4.2%",
            "return_on_ad_spend": "3.8",
            "social_media_engagement": "Low"
        }
    }
]

# Product Listings
product_listings = [
    {
        "title": "Samsung Galaxy S24",
        "price": "$349",
        "description": "The latest Samsung flagship smartphone with top-tier performance.",
        "features": ["5G Connectivity", "AI Camera", "AMOLED Display", "Fast Charging"]
    },
    {
        "title": "iPhone 15",
        "price": "$399",
        "description": "Apple's new iPhone with a stunning display and powerful A16 Bionic chip.",
        "features": ["OLED Display", "AI-Enhanced Camera", "5G Connectivity", "Ceramic Shield"]
    },
    {
        "title": "Apple AirPods Pro",
        "price": "$249",
        "description": "Noise-cancelling wireless earbuds with excellent sound quality and comfort.",
        "features": ["Active Noise Cancellation", "Spatial Audio", "Touch Controls", "Sweat & Water Resistant"]
    },
    {
        "title": "Samsung Galaxy Buds",
        "price": "$179",
        "description": "Wireless earbuds with a comfortable fit and great sound quality for everyday use.",
        "features": ["Noise Cancellation", "Long Battery Life", "Touch Controls", "Water-Resistant"]
    },
    {
        "title": "Apple Watch Series 9",
        "price": "$399",
        "description": "A powerful smartwatch with fitness tracking, health monitoring, and app integration.",
        "features": ["Health Monitoring", "Fitness Tracking", "GPS", "Always-On Display"]
    },
    {
        "title": "Samsung Galaxy Watch 6",
        "price": "$349",
        "description": "Advanced smartwatch featuring comprehensive fitness tracking and a sleek design.",
        "features": ["Sleep Tracking", "ECG Monitor", "Fitness Tracking", "Water-Resistant"]
    },
    {
        "title": "Fitbit Charge 6",
        "price": "$129",
        "description": "A fitness tracker with heart rate monitoring, step counting, and sleep analysis.",
        "features": ["Heart Rate Monitor", "Step Tracking", "Sleep Tracking", "Water-Resistant"]
    },
    {
        "title": "Xiaomi Mi Band 8",
        "price": "$79",
        "description": "Affordable fitness tracker with advanced health features and long battery life.",
        "features": ["Heart Rate Monitor", "Step Counting", "Sleep Tracking", "Waterproof"]
    }
]

# Reviews
product_reviews = [
    {
        "product_title": "Samsung Galaxy S24",
        "user_id": "user_1",
        "rating": 4.5,
        "title": "Great phone with amazing display",
        "comment": "The Samsung Galaxy S24 has a vibrant AMOLED display, and the camera is great for everyday use.",
        "verified_purchase": True
    },
    {
        "product_title": "iPhone 15",
        "user_id": "user_2",
        "rating": 4.8,
        "title": "Apple’s best iPhone yet",
        "comment": "The iPhone 15 has an excellent camera and performance. The battery life is impressive too.",
        "verified_purchase": True
    },
    {
        "product_title": "Apple AirPods Pro",
        "user_id": "user_3",
        "rating": 4.7,
        "title": "Best wireless earbuds!",
        "comment": "These AirPods are fantastic. The noise cancellation feature is great, and they are comfortable to wear.",
        "verified_purchase": True
    },
    {
        "product_title": "Samsung Galaxy Buds",
        "user_id": "user_4",
        "rating": 4.3,
        "title": "Good but could be better",
        "comment": "The sound quality is good, but I found the fit a little uncomfortable for long sessions.",
        "verified_purchase": True
    },
    {
        "product_title": "Apple Watch Series 9",
        "user_id": "user_5",
        "rating": 4.9,
        "title": "Fantastic smartwatch for fitness tracking",
        "comment": "The fitness tracking features of the Apple Watch Series 9 are top-notch. Highly recommend it.",
        "verified_purchase": True
    },
    {
        "product_title": "Samsung Galaxy Watch 6",
        "user_id": "user_6",
        "rating": 4.6,
        "title": "Sleek and functional",
        "comment": "The Samsung Galaxy Watch 6 is a great fitness tracker, and the design is sleek and comfortable.",
        "verified_purchase": True
    },
    {
        "product_title": "Fitbit Charge 6",
        "user_id": "user_7",
        "rating": 4.2,
        "title": "Decent fitness tracker",
        "comment": "The Fitbit Charge 6 works well for basic tracking but could use some improvements in the app.",
        "verified_purchase": False
    },
    {
        "product_title": "Xiaomi Mi Band 8",
        "user_id": "user_8",
        "rating": 4.0,
        "title": "Affordable and decent",
        "comment": "Great value for money. Does the job well, but lacks some advanced features.",
        "verified_purchase": True
    }
]




