<div align="center">
  
  <img src="https://img.shields.io/badge/AI%20Powered-Product%20Listings-FF5733" width="300" alt="Project Logo"/>

# SocioSell: Social Media to Product Listing Generator 🛍️

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248.svg)](https://www.mongodb.com/atlas)
[![Gemini AI](https://img.shields.io/badge/Gemini-1.5%20Pro-red.svg)](https://cloud.google.com/ai-platform)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Social Winter of Code](https://img.shields.io/badge/SWOC-2024-orange.svg)](https://swoc.tech)
[![Contributors](https://img.shields.io/github/contributors/Varsha-1605/SocioSell)](https://github.com/Varsha-1605/SocioSell/graphs/contributors)

<p align="center">
  An open-source initiative to transform social media content into comprehensive Amazon-style product listings using cutting-edge AI technology. Selected for Social Winter of Code 2024! 🎉
</p>

[🌟 Features](#-features) •
[⚙️ Installation](#️-installation) •
[🚀 Usage](#-usage) •
[💡 API Endpoints](#-api-endpoints) •
[🤝 Contributing](#-contributing) •
[👥 Community](#-community)

<img src="https://raw.githubusercontent.com/Varsha-1605/SocioSell/main/static/banner.png" width="100%" alt="Project Banner"/>

</div>

---

## 🎯 Project Vision

SocioSell aims to bridge the gap between social media content and e-commerce by providing an open-source solution for automated product listing generation. Whether you're a developer, marketer, or e-commerce enthusiast, your contributions can help shape the future of social commerce.

## 📺 Project Demo

Watch our community demo:

[🎥 Watch Demo](https://github.com/Varsha-1605/SocioSell/blob/main/static/folder/Untitled%20video%20-%20Made%20with%20Clipchamp.mp4)

---

## 🌟 Features

<table>
  <tr>
    <td>
      <h3>🤖 AI-Powered Analysis</h3>
      <ul>
        <li>Google Generative AI integration</li>
        <li>Smart product detection</li>
        <li>Automatic feature extraction</li>
      </ul>
    </td>
    <td>
      <h3>🔄 Smart Processing</h3>
      <ul>
        <li>Real-time processing</li>
        <li>Async operations</li>
        <li>Intelligent matching</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>
      <h3>🎯 Product Categories</h3>
      <ul>
        <li>Electronics</li>
        <li>Fashion</li>
        <li>Home Decor</li>
        <li>Beauty</li>
        <li>Sports Equipment</li>
      </ul>
    </td>
    <td>
      <h3>💫 User Experience</h3>
      <ul>
        <li>Modern UI/UX</li>
        <li>Drag-and-drop uploads</li>
        <li>Interactive comparisons</li>
      </ul>
    </td>
  </tr>
</table>

## ⚠️ Current Implementation Status and Limitations

### Processing Limitations
- The system currently processes custom data that is not linked to the database
- Uses `image_data` and `video_data` for accessing media details
- Maximum processing capacity (due to Gemini API constraints):
  - Images: Maximum 5 images per request
  - Videos: Maximum 3 videos, each limited to 10 seconds

### Implementation Notes for Contributors
- `image_processor.py` and `video_processor.py` are implemented and functional
- Integration needed: These processors need to be linked to `main.py`
- Database integration is pending and is a key area for contribution


## 🔧 Technology Stack

### Backend Infrastructure
```mermaid
graph LR
    A[Python 3.8+] --> B[FastAPI]
    B --> C[MongoDB]
    B --> D[Gemini AI]
    B --> E[AsyncIO]
```

### Frontend Technologies
```mermaid
graph LR
    A[HTML5] --> B[TailwindCSS]
    B --> C[JavaScript]
    C --> D[Font Awesome]
```

## ⚙️ Development Setup

```bash
# Clone repository
git clone https://github.com/Varsha-1605/SocioSell.git
cd SocioSell

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOL
GOOGLE_API_KEY=your_google_api_key
MONGODB_URL=your_mongodb_connection_string
EOL

# Initialize database
python database_setup.py
```

## 📁 Project Structure

```ascii
project/
├── 📜 main.py                # Entry point
├── 🖼️ image_processor.py     # AI image analysis
├── 🔄 content_processor.py   # Content processing
├── 💾 database_setup.py      # DB initialization
├── 📁 static/               # Static assets
├── 📝 templates/            # HTML templates
├── 🔒 .env                 # Environment vars
└── 📋 requirements.txt     # Dependencies
```

## 🚀 Usage

1. Start the development server:
```bash
uvicorn main:app --reload
```

2. Access the application at `http://localhost:8000`

## 💡 API Endpoints

<table>
  <tr>
    <th>Endpoint</th>
    <th>Method</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>/upload/</code></td>
    <td>POST</td>
    <td>Upload & analyze products</td>
  </tr>
  <tr>
    <td><code>/search/{title}</code></td>
    <td>GET</td>
    <td>Search product database</td>
  </tr>
  <tr>
    <td><code>/listings/{product_id}</code></td>
    <td>GET</td>
    <td>Get listing details</td>
  </tr>
  <tr>
    <td><code>/compare/{product_id}</code></td>
    <td>GET</td>
    <td>Compare products</td>
  </tr>
</table>

## 🤝 Contributing

We warmly welcome contributions from developers of all skill levels! Here's how you can help:

```mermaid
graph TD
    A[Fork Repository] --> B[Create Branch]
    B --> C[Make Changes]
    C --> D[Commit Changes]
    D --> E[Push to Branch]
    E --> F[Create Pull Request]
```

Check out our [Contributing Guidelines](CONTRIBUTING.md) to get started.

### 🎯 Good First Issues
- Look for issues tagged with `good-first-issue`
- Check the [Project Board](https://github.com/Varsha-1605/SocioSell/projects) for tasks
- Join our community discussions for guidance

## 👥 Community

- 💬 Join our [Discord Server](discord-invite-link)
- 📝 Follow our [Blog](blog-link)
- 🐦 Follow us on [Twitter](twitter-link)
- 📧 Contact maintainers: varshadewangan454@gmail.com

### 🌟 Contributors

Thanks to these wonderful people:

<a href="https://github.com/Varsha-1605/SocioSell/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Varsha-1605/SocioSell" />
</a>

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- All our amazing contributors
- [Social Winter of Code](https://swoc.tech) for selecting our project
- [Google Generative AI](https://cloud.google.com/ai-platform)
- [MongoDB Atlas](https://www.mongodb.com/atlas)
- [TailwindCSS](https://tailwindcss.com/)
- [FastAPI](https://fastapi.tiangolo.com/)

---

<div align="center">

Made with ❤️ by the SocioSell Community

[⬆ Back to Top](#socialsell-social-media-to-product-listing-generator-)

</div>
