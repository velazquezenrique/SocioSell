# Social Media to Product Listing Generator 🛍️

A sophisticated system that transforms social media content into comprehensive Amazon-style product listings, enabling seamless product comparison and purchasing decisions. This project leverages AI image processing and text analysis to automatically generate detailed product information from social media posts.

## 🌟 Features

- **AI-Powered Image Analysis**: Utilizes Google's Generative AI to extract product details from images
- **Smart Product Matching**: Automatically matches products with existing database entries
- **Comparative Analysis**: Generates detailed product comparisons with similar items
- **Real-time Processing**: Asynchronous processing for quick response times
- **Interactive UI**: Modern, responsive interface with drag-and-drop functionality
- **Multi-category Support**: Handles various product categories including:
  - Electronics
  - Fashion
  - Home Decor
  - Beauty
  - Sports Equipment

## 🔧 Technology Stack

- **Backend**:
  - Python 3.8+
  - FastAPI
  - MongoDB
  - Google Generative AI (Gemini 1.5 Pro)
  - AsyncIO

- **Frontend**:
  - HTML5
  - TailwindCSS
  - JavaScript
  - Font Awesome

- **Database**:
  - MongoDB Atlas

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/social-media-product-listing.git
cd social-media-product-listing
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
GOOGLE_API_KEY=your_google_api_key
MONGODB_URL=your_mongodb_connection_string
```

5. Set up the database:
```bash
python database_setup.py
```

## 🚀 Usage

1. Start the server:
```bash
uvicorn main:app --reload
```
or 

```bash
python main.py
```

2. Open your browser and navigate to `http://localhost:8000`

3. Use the application:
   - Upload product images through the interface
   - Add product titles and optional captions
   - Generate detailed product listings
   - Compare with similar products
   - Search existing product database

## 📁 Project Structure

```
project/
├── main.py                # FastAPI application entry point
├── image_processor.py     # Image analysis using Google's Generative AI
├── content_processor.py   # Content processing and listing generation
├── database_setup.py      # MongoDB initialization and setup
├── static/               # Static files (images, CSS)
│   ├── electronics/
│   ├── fashion/
│   ├── home_decor/
│   ├── beauty/
│   └── sports/
|   |__styles.css/
├── templates/            # HTML templates
│   └── index.html       # Main application template
├── .env                 # Environment variables
└── requirements.txt     # Project dependencies
```

## 💡 API Endpoints

- `POST /upload/`: Upload product image and generate listing
- `GET /search/{title}`: Search products by title
- `GET /listings/{product_id}`: Get product listing details
- `GET /compare/{product_id}`: Get comparable products

## ⚠️ Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account
- Google Cloud account with Generative AI API access
- Node.js and npm (for TailwindCSS)

## 🔒 Environment Variables

| Variable | Description |
|----------|-------------|
| GOOGLE_API_KEY | Google Cloud API key for Generative AI |
| MONGODB_URL | MongoDB Atlas connection string |

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For any queries or support, please contact:
- Email: varshadewangan454@gmail.com

## 🙏 Acknowledgments

- Google Generative AI team for the Gemini API
- MongoDB Atlas for database services
- TailwindCSS team for the UI framework
- FastAPI team for the backend framework

---
