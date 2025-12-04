# Contributing to Movie Recommendation System

First off, thank you for considering contributing to the Movie Recommendation System! It's people like you that make this project better for everyone.

## 🌟 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected behavior**
A clear description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g., Windows 10, macOS 12.0, Ubuntu 20.04]
 - Python Version: [e.g., 3.10.5]
 - Django Version: [e.g., 5.0]
 - Browser: [e.g., Chrome 120, Firefox 115]

**Additional context**
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List some examples** of how it would be used

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Ensure all tests pass**
6. **Submit your pull request**

## 🔧 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/movie-recommendation-system.git
cd movie-recommendation-system

# Add upstream remote
git remote add upstream https://github.com/original-owner/movie-recommendation-system.git
```

### 2. Create a Branch

```bash
# Create a branch for your feature or fix
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 3. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black flake8 pytest pytest-django
```

### 4. Make Your Changes

Follow the coding standards and best practices outlined below.

### 5. Test Your Changes

```bash
# Run tests
python manage.py test

# Run linting
flake8 .

# Format code
black .
```

### 6. Commit Your Changes

```bash
git add .
git commit -m "Add: Brief description of your changes"
```

**Commit Message Guidelines:**

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

**Commit Types:**
- `Add:` New feature or functionality
- `Fix:` Bug fix
- `Update:` Update existing feature
- `Refactor:` Code refactoring
- `Docs:` Documentation changes
- `Style:` Formatting, missing semicolons, etc.
- `Test:` Adding or updating tests
- `Chore:` Maintenance tasks

### 7. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Then create a Pull Request on GitHub
```

## 📋 Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

```python
# Good
def get_movie_recommendations(movie_id: int, limit: int = 10) -> List[Dict]:
    """
    Get movie recommendations based on similarity.
    
    Args:
        movie_id: ID of the movie
        limit: Maximum number of recommendations
        
    Returns:
        List of recommended movies
    """
    pass

# Bad
def GetRecommendations(id,limit=10):
    pass
```

### Key Points:

1. **Indentation**: Use 4 spaces (no tabs)
2. **Line Length**: Maximum 88 characters (Black default)
3. **Imports**: 
   - Group imports: stdlib, third-party, local
   - Use absolute imports
   - One import per line
4. **Naming**:
   - `snake_case` for functions and variables
   - `PascalCase` for classes
   - `UPPER_CASE` for constants
5. **Documentation**:
   - Docstrings for all public functions and classes
   - Use Google-style docstrings
6. **Type Hints**: Use type hints for function parameters and returns

### Django Best Practices

1. **Views**: Keep views thin, move business logic to services
2. **Models**: Use descriptive field names, add help_text
3. **Templates**: Use template inheritance, avoid logic in templates
4. **URLs**: Use meaningful URL patterns, include app namespaces
5. **Security**: Always use CSRF protection, validate inputs

### Frontend Guidelines

1. **HTML**: Use semantic HTML5 elements
2. **CSS**: 
   - Use CSS custom properties for theming
   - Mobile-first responsive design
   - Use meaningful class names
3. **JavaScript**:
   - Use modern ES6+ syntax
   - Add comments for complex logic
   - Handle errors gracefully

## 🧪 Testing Guidelines

### Writing Tests

```python
from django.test import TestCase, Client
from django.urls import reverse

class RecommenderViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.client.get(reverse('recommender:main'))
        self.assertEqual(response.status_code, 200)
        
    def test_movie_search_valid(self):
        """Test movie search with valid input"""
        response = self.client.post(
            reverse('recommender:main'),
            {'movie_name': 'The Matrix'}
        )
        self.assertEqual(response.status_code, 200)
```

### Test Coverage

- Aim for at least 80% code coverage
- Test both happy paths and edge cases
- Test error handling
- Test API endpoints

## 📚 Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Update README.md if adding new features
- Add inline comments for complex logic
- Keep documentation up to date

### README Updates

When adding features, update:
- Features list
- Usage examples
- API endpoints
- Configuration options
- Screenshots (if UI changed)

## 🔍 Code Review Process

### What We Look For

1. **Functionality**: Does it work as intended?
2. **Code Quality**: Is it clean, readable, and maintainable?
3. **Testing**: Are there adequate tests?
4. **Documentation**: Is it well documented?
5. **Performance**: Is it efficient?
6. **Security**: Does it follow security best practices?

### Review Timeline

- We aim to review PRs within 3-5 business days
- Large PRs may take longer
- Address review comments promptly

## 🎨 Design Guidelines

### UI/UX Principles

1. **Simplicity**: Keep interfaces clean and intuitive
2. **Consistency**: Use consistent colors, spacing, and patterns
3. **Accessibility**: Ensure WCAG 2.1 AA compliance
4. **Responsiveness**: Test on multiple screen sizes
5. **Performance**: Optimize for fast load times

### Color Palette

```css
--primary-color: #6366f1;
--secondary-color: #8b5cf6;
--background: #0f172a;
--text-primary: #f1f5f9;
```

## 🐛 Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information requested
- `wontfix`: This will not be worked on

## 💬 Communication

### Where to Ask Questions

- **General Questions**: GitHub Discussions
- **Bug Reports**: GitHub Issues
- **Feature Requests**: GitHub Issues
- **Security Issues**: Email directly (not public issues)

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Give constructive feedback
- Focus on what is best for the community

## 📜 Legal

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🙌

---

**Questions?** Feel free to open an issue or start a discussion.

