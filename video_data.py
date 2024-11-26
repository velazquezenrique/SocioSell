# video_data.py

# Video Database by Category
VIDEO_DATABASE = {
    "electronics": {
        "video_123": {
            "title": "iPhone 15 Pro Review",
            "category": "Smartphones",
            "duration": "10:25",
            "highlights": [
                "Camera system demo",
                "Performance benchmarks",
                "Battery life test",
                "Design overview"
            ],
            "transcript_summary": "Detailed review of iPhone 15 Pro features...",
            "key_features": [
                "A17 Pro chip",
                "48MP camera",
                "Titanium design",
                "USB-C port"
            ],
            "price_range": "$999 - $1199"
        },
        "video_124": {
            "title": "MacBook Pro M3 Analysis",
            "category": "Laptops",
            "duration": "15:30",
            "highlights": [
                "Performance tests",
                "Display quality",
                "Battery duration",
                "Port selection"
            ],
            "transcript_summary": "In-depth analysis of the new MacBook Pro...",
            "key_features": [
                "M3 chip",
                "Mini-LED display",
                "Up to 22hr battery",
                "Multiple ports"
            ],
            "price_range": "$1599 - $2499"
        }
    },
    "fashion": {
        "video_125": {
            "title": "Nike Air Jordan Collection",
            "category": "Sneakers",
            "duration": "8:45",
            "highlights": [
                "Design showcase",
                "Comfort testing",
                "Style combinations",
                "Size guide"
            ],
            "transcript_summary": "Comprehensive review of Air Jordan lineup...",
            "key_features": [
                "Air cushioning",
                "Premium materials",
                "Iconic design",
                "Multiple colorways"
            ],
            "price_range": "$180 - $200"
        }
    },
    # Add other categories...
    "beauty": {
        "video_126": {
            "title": "Summer Makeup Tutorial",
            "category": "Makeup",
            "duration": "12:15",
            "highlights": [
                "Product application",
                "Techniques demo",
                "Wear test",
                "Product reviews"
            ],
            "transcript_summary": "Step-by-step summer makeup guide...",
            "key_features": [
                "Waterproof products",
                "Natural look",
                "Long-lasting",
                "SPF protection"
            ],
            "price_range": "$20 - $150"
        }
    }
}


# Video Listings Database
VIDEO_LISTINGS_DATABASE = {
    "video_123": [
        {
            "id": "vlist_123",
            "platform": "YouTube",
            "title": "iPhone 15 Pro Detailed Review",
            "views": "1.2M",
            "rating": 4.8,
            "key_timestamps": {
                "unboxing": "0:00",
                "camera_test": "3:45",
                "performance": "7:30",
                "conclusion": "9:15"
            },
            "product_links": [
                {"store": "Apple", "price": "$999"},
                {"store": "Amazon", "price": "$989"},
                {"store": "Best Buy", "price": "$999"}
            ]
        },
        {
            "id": "vlist_124",
            "platform": "TikTok",
            "title": "iPhone 15 Pro Quick Review",
            "views": "500K",
            "rating": 4.7,
            "key_timestamps": {
                "features": "0:00",
                "camera": "1:30",
                "verdict": "2:45"
            },
            "product_links": [
                {"store": "Apple", "price": "$999"},
                {"store": "Walmart", "price": "$979"}
            ]
        }
    ]
}

# Comparable Videos Database
COMPARABLE_VIDEOS_DATABASE = {
    "video_123": [
        {
            "id": "video_127",
            "title": "Samsung S24 Ultra Review",
            "duration": "11:30",
            "views": "900K",
            "comparison_points": [
                "Camera quality",
                "Performance",
                "Battery life",
                "Price value"
            ],
            "price_range": "$1199 - $1299"
        },
        {
            "id": "video_128",
            "title": "Google Pixel 8 Pro Review",
            "duration": "9:45",
            "views": "750K",
            "comparison_points": [
                "AI features",
                "Photo capabilities",
                "Software experience",
                "Battery efficiency"
            ],
            "price_range": "$999 - $1099"
        }
    ]
}

# Video Analytics Database
VIDEO_ANALYTICS_DATABASE = {
    "video_123": {
        "engagement": {
            "views": "1.2M",
            "likes": "50K",
            "comments": "3.2K",
            "average_watch_time": "8:30"
        },
        "audience": {
            "demographics": {
                "18-24": "30%",
                "25-34": "45%",
                "35-44": "15%",
                "45+": "10%"
            },
            "top_regions": ["US", "UK", "Canada", "Australia"]
        },
        "performance": {
            "retention_rate": "68%",
            "click_through_rate": "4.2%",
            "conversion_rate": "2.8%"
        }
    }
}
