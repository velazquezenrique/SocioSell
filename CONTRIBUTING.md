# Contributing to SocioSell

First off, thank you for considering contributing to SocioSell! It's people like you that make SocioSell such a great tool for transforming social media content into product listings.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Environment Setup](#environment-setup)
  - [Development Workflow](#development-workflow)
- [How Can I Contribute?](#how-can-i-contribute)
- [Style Guidelines](#style-guidelines)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct. Please report unacceptable behavior to varshadewangan1605@gmail.com.

## Getting Started

### Environment Setup

1. Fork the repository:
```bash
git fork https://github.com/Varsha-1605/SocioSell
```

2. Clone your fork:
```bash
git clone [your-fork-url]
cd SocioSell
```

3. Set up your development environment:
```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys:
# - GOOGLE_API_KEY=your_google_api_key
# - MONGODB_URL=your_mongodb_connection_string
```

### Development Workflow

1. Create a new branch for your feature or bugfix:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bugfix-name
```

2. Make your changes and commit them using conventional commits:
```bash
git add .
git commit -m "feat: description of your feature"
# or
git commit -m "fix: description of your bugfix"
```

3. Push your changes:
```bash
git push origin your-branch-name
```

## How Can I Contribute?

### 1. Find an Issue
- Look for issues labeled with `good-first-issue` or `help-wanted`
- Check our [project board](https://github.com/Varsha-1605/SocioSell/projects) for planned features
- If you don't see an issue for your contribution, create one first

### 2. Priority Areas
We are currently focusing on:
1. Database Integration
   - MongoDB connection implementation
   - Data models for products and listings
   - Database querying functionality

2. Processor Integration
   - Linking image and video processors to main.py
   - Error handling for processing failures
   - Input validation for media files

3. UI/UX Improvements
   - Progress indicators
   - Drag-and-drop file upload
   - Responsive design for mobile

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
