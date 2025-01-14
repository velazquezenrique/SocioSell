# Contributing to SocioSell

First off, thank you for considering contributing to SocioSell! It's people like you that make SocioSell such a great tool for transforming social media content into product listings.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Environment Setup](#environment-setup)
  - [Development Workflow](#development-workflow)
- [How Can I Contribute?](#how-can-i-contribute)
- [Project Roadmap](#project-roadmap)
- [Priority Areas For Contribution](#priority-areas-for-contribution)
- [Style Guidelines](#style-guidelines)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](./CODE_OF_CONDUCT.md). Please report unacceptable behavior to varshadewangan1605@gmail.com.

## Getting Started

### Environment Setup

I. Clone the repository 
> ```  
>  git clone https://github.com/Varsha-1605/SocioSell.git  
> cd SocioSell
> ```  

II. Set up a virtual environment
> ```
> python -m venv venv  
> source venv/bin/activate  # Windows: > venv\Scripts\activate  
> ```
III. Install dependencies
> ```
> pip install -r requirements.txt  
> ```
IV. Create a `.env` file
> ```
> cat > .env << EOL  
> GOOGLE_API_KEY=your_google_api_key  
> MONGODB_URL=your_mongodb_connection_string  
> EOL  
> ```
V. Initialize the database
> ```
> python database_setup.py  
> ```
VII. Start the development server
> ```
> uvicorn main:app --reload  
> ```
VIII. Access the application
- Open your browser and go to `http://localhost:8000`.

### Development Workflow

I. Create a new branch for your feature or bugfix:
> ```bash
> git checkout -b feature/your-feature-name
> # or
> git checkout -b fix/your-bugfix-name
> ```

II. Make your changes and commit them using conventional commits:
> ```bash
> git add .
> git commit -m "feat: description of your feature"
> # or
> git commit -m "fix: description of your bugfix"
> ```

III. Push your changes:
> ```bash
> git push origin your-branch-name
> ```

## How Can I Contribute?

### 1. Find an Issue
- Look for issues labeled with `good-first-issue` or `help-wanted`
- Check our [project board](https://github.com/Varsha-1605/SocioSell/projects) for planned features
- If you don't see an issue for your contribution, create one first

## Project Roadmap

### Phase 1 (Complete)
- ✅ Basic image and video processing
- ✅ Initial API setup
- ✅ Database integration

### Phase 2 (Current)
- 🔄 Enhanced error handling
- 📋 User authentication
- 📋 Batch processing capabilities

### Phase 3 (Future)
- 📋 Advanced AI features
- 📋 Social media platform integration
- 📋 Analytics dashboard

## Priority Areas for Contribution  

### 1. Database Enhancements  
With the MongoDB setup completed, further enhancements should focus on:  
- **Data Pooling**: Implement connection pooling using pymongo's built-in pooling feature to improve performance by reusing database connections and reducing overhead.
- **Error Handling**:  
  - Implement robust error-handling mechanisms for processing failures.  
  - Log errors to allow debugging and tracking. 

### 2. Processor Integration  
- **Connect Processors**: Integrate image_processor.py and video_processor.py with main.py.  
- **Error Handling**:  
  - Implement robust error-handling mechanisms for processing failures.  
  - Log errors to allow debugging and tracking.  
- **Input Validation**:  
  - Validate media file formats, sizes, and dimensions before processing.  
  - Reject unsupported formats with clear error messages.  

### 3. UI/UX Improvements  
- **Progress Indicators**:  
  - Show real-time status updates during image and video processing.  
- **Responsive Design**:  
  - Ensure a seamless user experience across devices, especially mobile.  
  - Test and optimize for different screen sizes and resolutions.  

## Style Guidelines

### Python Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints
- Include docstrings for all functions and classes
- Maximum line length: 88 characters

### Documentation Style
- Use Markdown for documentation
- Include code examples where applicable
- Keep language clear and concise
- Update README.md if adding new features

### Testing
- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage
```bash
python -m pytest
```

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the requirements.txt if you add dependencies
3. Fill out the pull request template completely
4. Link the PR to any related issues
5. Request review from maintainers
6. Wait for approval and address any feedback

### PR Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Conventional commit messages used
- [ ] No conflicts with main branch

## Community

- 💬 Join our [Discord Server](https://discord.gg/n34tSJ3TBs)
- 🔗 Connect on [LinkedIn](www.linkedin.com/in/varsha-dewangan-197983256)
- 🐦 Follow us on [Twitter](https://x.com/varsha_dew454)

### Getting Help
If you need help, you can:
1. Join our Discord server for real-time discussion
2. Open a [Discussion](https://github.com/Varsha-1605/SocioSell/discussions) on GitHub
3. Email the maintainers at varshadewangan1605@gmail.com

## Recognition

All contributors will be added to our [Contributors](https://github.com/Varsha-1605/SocioSell/graphs/contributors) page and the README.md.

---

Remember that this is an open-source project and we love to receive contributions from our community! Thanks for helping make SocioSell better 🚀
