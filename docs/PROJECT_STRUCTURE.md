## 📁 Project Structure
```
SocioSell/
├── 📜 main.py                      # FastAPI application entry point
├── 📁 .github/                     # GitHub specific files
│   └── ISSUE_TEMPLATE/              # Issue templates for contributions
├── 📁 static/                      # Static assets and files
├── 📁 templates/                   # HTML templates
│   ├── 📊 index.html                  
├── 📁 models/                      # Models folder
│   ├── 📊 analytics.py             # Analytics model
│   ├── 📊 listing.py               # Listing model
│   ├── 📊 product.py               # Product model
│   ├── 📊 review.py                # Review model
│   ├── 📊 video.py                 # Video model
│   ├── 📊 analytics_video.py       # Analytics Video model
│   ├── 📊 video_listing.py         # Video Listing model
├── 📁 routes/                      # Routes folder
│   ├── 🖼️ image.py                 # Image routes
│   ├── 🎥 video.py                 # Video routes
│   ├── 🔗 combined.py              # Combined routes
├── 📁 schema/                      # Schema folder
│   ├── 🖼️ image.py                 # Image schema
│   ├── 🎥 video.py                 # Video schema
│   ├── 🔗 combined.py              # Combined schema
├── 🔧 content_processor.py         # Content analysis and processing
├── 💾 database_setup.py            # Database initialization
├── 🖼️ image_processor.py           # Image processing module
├── 📊 image_data.py                # Image data structures
├── 🎥 video_processor.py           # Video processing module
├── 📊 video_data.py                # Video data structures
├── 🧪 test_image_processor.py      # Image processing tests
├── 🧪 test_video_processor.py      # Video processing tests
├── 📋 requirements.txt             # Project dependencies
├── 📝 README.md                    # Project documentation
├── 🔒 .env                         # Environment variables
└── 📝 .gitignore                   # Git ignore rules
```

## 💡 API Endpoints  

### Image Endpoints  

<table>
  <tr>
    <th>Endpoint</th>
    <th>Method</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>/upload/image/</code></td>
    <td>POST</td>
    <td>Upload & analyze a product image</td>
  </tr>
  <tr>
    <td><code>/upload/image/search/{title}</code></td>
    <td>GET</td>
    <td>Search product database by title</td>
  </tr>
  <tr>
    <td><code>/upload/image/listings/{product_id}</code></td>
    <td>GET</td>
    <td>Get listing details for a product</td>
  </tr>
  <tr>
    <td><code>/upload/image/compare/{product_id}</code></td>
    <td>GET</td>
    <td>Compare products</td>
  </tr>
  <tr>
    <td><code>/upload/image/product/details/{product_id}</code></td>
    <td>GET</td>
    <td>Get detailed information about a product</td>
  </tr>
  <tr>
    <td><code>/upload/image/product/analytics/{product_id}</code></td>
    <td>GET</td>
    <td>Get product analytics</td>
  </tr>
  <tr>
    <td><code>/upload/image/product/recommendations/{product_id}</code></td>
    <td>GET</td>
    <td>Get product recommendations based on a specific product</td>
  </tr>
  <tr>
    <td><code>/upload/image/categories</code></td>
    <td>GET</td>
    <td>Get list of all available categories for products and videos</td>
  </tr>
  <tr>
    <td><code>/upload/image/product/reviews/{product_id}</code></td>
    <td>GET</td>
    <td>Get reviews for a product</td>
  </tr>
</table>

---

### Video Endpoints  

<table>
  <tr>
    <th>Endpoint</th>
    <th>Method</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>/upload/video/</code></td>
    <td>POST</td>
    <td>Upload & analyze a product video</td>
  </tr>
  <tr>
    <td><code>/upload/video/search/{title}</code></td>
    <td>GET</td>
    <td>Search for videos by title</td>
  </tr>
  <tr>
    <td><code>/upload/video/listings/{video_id}</code></td>
    <td>GET</td>
    <td>Get video listings details</td>
  </tr>
  <tr>
    <td><code>/upload/video/compare/{video_id}</code></td>
    <td>GET</td>
    <td>Compare videos</td>
  </tr>
  <tr>
    <td><code>/upload/video/analytics/{video_id}</code></td>
    <td>GET</td>
    <td>Get video analytics</td>
  </tr>
</table>

---

### Combined Endpoints  

<table>
  <tr>
    <th>Endpoint</th>
    <th>Method</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>/search/all/{query}</code></td>
    <td>GET</td>
    <td>Search both products and videos across all categories</td>
  </tr>
</table>

---
---

## 🗂️ Indexing Overview  

The indexing strategy is designed to:  
- **Speed Up Queries**: Makes searching faster for fields like `id`, `title`, and timestamps.  
- **Handle Complex Searches**: Uses combined indexes for multi-field lookups.  
- **Prepare for the Future**: Supports flexible data searches, including text-based queries.  
- **Keep Data Clean**: Ensures no duplicate records with unique constraints.  

This makes the system faster, reliable, and ready for future needs.
