# 📘 Movie Recommendation System - Complete Project Guide

> **Comprehensive technical documentation** for developers, covering installation, configuration, development, deployment, and troubleshooting.

---

## 📑 Table of Contents

### Getting Started
- [Overview](#-overview)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Quick Verification](#-quick-verification)

### Core Functionality
- [Project Architecture](#-project-architecture)
- [How It Works](#-how-it-works)
- [Model Training](#-model-training)
- [Using Different Models](#-using-different-models)

### Configuration & Development
- [Configuration](#-configuration)
- [Development Guide](#-development-guide)
- [Testing](#-testing)

### Deployment
- [Deployment](#-deployment)
  - [Render](#deploy-to-render)
  - [Heroku](#deploy-to-heroku)
  - [Docker](#deploy-with-docker)
  - [AWS](#deploy-to-aws)

### Reference
- [API Reference](#-api-reference)
- [Command Reference](#-command-reference)
- [Troubleshooting](#-troubleshooting)
- [Best Practices](#-best-practices)
- [FAQ](#-faq)

---

## 🎯 Overview

This guide provides comprehensive documentation for the Movie Recommendation System, a production-ready Django application that delivers intelligent movie recommendations using advanced machine learning algorithms.

### What This Guide Covers

- ✅ **Installation**: Step-by-step setup instructions
- ✅ **Configuration**: Environment variables and settings
- ✅ **Model Training**: Creating custom recommendation models
- ✅ **Development**: Working with the codebase
- ✅ **Deployment**: Production deployment guides
- ✅ **API Reference**: Complete endpoint documentation
- ✅ **Troubleshooting**: Common issues and solutions

### Related Documentation

- **[README.md](README.md)** - Project overview and quick start
- **[training/guide.md](training/guide.md)** - Detailed model training documentation
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

---

## ✅ Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Python** | 3.10+ | 3.10+ |
| **RAM** | 4GB | 8GB+ |
| **Storage** | 2GB | 5GB+ |
| **OS** | Windows/macOS/Linux | Any |

### Required Software

- **Python 3.10 or higher** - [Download here](https://www.python.org/downloads/)
- **pip** - Python package manager (included with Python)
- **Git** - Version control [Download here](https://git-scm.com/)
- **Virtual environment tool** - venv (included with Python)

### Optional Software

- **PostgreSQL** - For production database
- **Redis** - For caching (production)
- **Docker** - For containerized deployment

---

## 💻 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

**Verification**: Your terminal should show `(venv)` prefix.

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

**Expected output**: All packages installed successfully without errors.

### Step 4: Database Setup

```bash
# Run database migrations
python manage.py migrate
```

**Output**: Should show migrations applied successfully.

### Step 5: Start Development Server

```bash
python manage.py runserver
```

**Output**: 
```
Starting development server at http://127.0.0.1:8000/
```

### Step 6: Verify Installation

Open your browser and navigate to:
```
http://localhost:8000
```

You should see the Movie Recommendation System home page. ✅

---

## ✓ Quick Verification

Run these commands to verify everything is working:

```bash
# 1. Check Python version
python --version
# Expected: Python 3.10.x or higher

# 2. Check Django installation
python manage.py --version
# Expected: Django version number

# 3. Test health endpoint
curl http://localhost:8000/api/health/
# Expected: {"status": "healthy", ...}

# 4. Test search API
curl "http://localhost:8000/api/search/?q=matrix"
# Expected: {"movies": [...], "count": ...}
```

---

## 🏗️ Project Architecture

### High-Level Architecture

![Project Architecture](./assets/images-for-readme/Architecture.png)

### Component Breakdown

#### Django Application (`movie_recommendation/`)
- **settings.py**: Configuration and environment settings
- **urls.py**: URL routing to apps
- **wsgi.py**: WSGI application entry point

#### Recommender App (`recommender/`)
- **views.py**: Core recommendation logic
  - `MovieRecommender` class (model loading, recommendations)
  - View functions (main, search_movies, health_check)
- **urls.py**: URL patterns for the app
- **templates/**: HTML templates with inline CSS

#### Model Files (`models/` or `static/`)
- **movie_metadata.parquet**: Movie information (title, rating, genres, etc.)
- **similarity_matrix.npz**: Precomputed similarity scores (sparse format)
- **title_to_idx.json**: Mapping from titles to indices
- **tfidf_vectorizer.pkl**: TF-IDF model (for future retraining)
- **svd_model.pkl**: SVD dimensionality reduction model

#### Training Scripts (`training/`)
- **train.py**: Complete training pipeline
- **infer.py**: Inference examples and usage
- **guide.md**: Training documentation

---

## 🔍 How It Works

### Recommendation Pipeline

```
1. User Input
   └─> "Inception"

2. Fuzzy Matching
   └─> Find closest title in database
       └─> "Inception" (exact match) ✓

3. Get Movie Index
   └─> title_to_idx["Inception"] = 42

4. Fetch Similarity Scores
   └─> similarity_matrix[42] = [0.95, 0.87, 0.82, ...]

5. Sort & Filter
   └─> Top 15 similar movies (excluding input)
   └─> Apply filters (rating, year, genre)

6. Format Response
   └─> Return movie details with metadata

7. Display Results
   └─> Render cards with ratings, genres, links
```

### Content-Based Filtering

The system uses **content-based filtering** with these features:

1. **TF-IDF Vectorization**
   - Converts movie features (genres, keywords, plot) into numerical vectors
   - Captures importance of terms relative to corpus

2. **SVD Dimensionality Reduction** (optional)
   - Reduces feature space from thousands to 300-600 dimensions
   - Captures latent patterns and reduces noise
   - Makes computation more efficient

3. **Cosine Similarity**
   - Measures similarity between movie vectors
   - Ranges from 0 (completely different) to 1 (identical)

4. **Ranking & Filtering**
   - Ranks movies by similarity score
   - Applies user-defined filters (year, rating, genre)

For more details, see [training/guide.md - How It Works](training/guide.md)

---

## 🎓 Model Training

### Overview

The system supports two model sources:

1. **Demo Model** (included) - 2,000 popular movies, ready to use
2. **Custom Model** (train your own) - 10K to 1M+ movies

### Using Demo Model

```bash
# Demo model is in static/ directory
export MODEL_DIR=./static
python manage.py runserver
```

No training needed! Works out of the box.

### Training Your Own Model

For complete training documentation, see **[training/guide.md](training/guide.md)**

**Quick Training Example:**

```python
from training.train import MovieRecommenderTrainer

# Initialize trainer
trainer = MovieRecommenderTrainer(
    output_dir='./models',
    use_dimensionality_reduction=True,
    n_components=500
)

# Train on your dataset
df, sim_matrix = trainer.train(
    'path/to/your/dataset.csv',
    quality_threshold='medium',  # low/medium/high
    max_movies=100000
)
```

### Training Configurations

| Configuration | Movies | Time | Memory | Model Size | Use Case |
|--------------|--------|------|--------|------------|----------|
| **Small** | 10K | 2 min | 500MB | 40MB | Testing |
| **Medium** ⭐ | 100K | 15 min | 2GB | 180MB | Production |
| **Large** | 1M+ | 60 min | 6GB | 800MB | Full dataset |

### Dataset Requirements

Your CSV must have these columns:
- `title` (required)
- `genres` (required)
- `keywords` (required)
- `vote_average`, `vote_count` (recommended)
- `release_date`, `imdb_id`, `poster_path` (optional)

For detailed requirements and training guide, see **[training/guide.md](training/guide.md)**

---

## 🔧 Using Different Models

### Switching Models

The system uses the `MODEL_DIR` environment variable to locate models:

```bash
# Method 1: Environment variable
export MODEL_DIR=./models
python manage.py runserver

# Method 2: .env file
echo "MODEL_DIR=./models" >> .env
python manage.py runserver

# Method 3: Modify settings.py
# MODEL_DIR = os.path.join(BASE_DIR, 'models')
```

### Model Directory Structure

Your model directory must contain:
```
models/
├── movie_metadata.parquet    # Required
├── similarity_matrix.npy     # Required (or .npz)
├── title_to_idx.json         # Required
├── config.json               # Optional (for metadata)
├── tfidf_vectorizer.pkl      # Optional (for retraining)
└── svd_model.pkl            # Optional (for retraining)
```

### Verifying Model

```bash
# Check health endpoint
curl http://localhost:8000/api/health/

# Response shows model information
{
  "status": "healthy",
  "movies_loaded": 100000,
  "model_dir": "./models",
  "model_loaded": true
}
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Core
SECRET_KEY=your-secret-key-here-minimum-50-characters
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Model Configuration
MODEL_DIR=./models

# Database (optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# CORS (if using separate frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Admin Panel
ADMIN_ENABLED=False

# Deployment
RENDER_EXTERNAL_HOSTNAME=your-app.onrender.com
```

### Generating SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Database Configuration

**Development (SQLite - default):**
```python
# Already configured in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL - recommended):**
```python
# Install: pip install dj-database-url psycopg2-binary
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}
```

---

## 🔨 Development Guide

### Project Structure

```
recommender/
├── views.py          # Core logic
├── urls.py           # URL patterns
├── models.py         # Database models (currently empty)
├── admin.py          # Admin configuration
├── apps.py           # App configuration
└── templates/        # HTML templates
    └── recommender/
        ├── index.html    # Home/search page
        ├── result.html   # Recommendations page
        └── error.html    # Error page
```

### Development Workflow

```bash
# 1. Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Run development server
python manage.py runserver

# 3. Access application
# http://localhost:8000

# 4. Make changes to code
# Files auto-reload on save

# 5. Run tests (when available)
python manage.py test
```

### Django Management Commands

```bash
# Database
python manage.py migrate                    # Apply migrations
python manage.py makemigrations            # Create migrations
python manage.py showmigrations            # Show migration status

# Static files
python manage.py collectstatic --noinput   # Collect static files

# Development
python manage.py runserver                 # Run dev server
python manage.py runserver 8080           # Run on different port
python manage.py shell                     # Django shell

# Admin (if enabled)
python manage.py createsuperuser           # Create admin user
```

### Viewing Logs

```bash
# Real-time logs (Unix/macOS)
tail -f logs/django.log

# Real-time logs (Windows PowerShell)
Get-Content logs\django.log -Wait

# Last 100 lines
tail -n 100 logs/django.log
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test recommender

# Run with verbose output
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb
```

### Writing Tests

```python
from django.test import TestCase, Client
from django.urls import reverse

class RecommenderTests(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_home_page(self):
        """Test home page loads"""
        response = self.client.get(reverse('recommender:main'))
        self.assertEqual(response.status_code, 200)
    
    def test_search_api(self):
        """Test search API"""
        response = self.client.get('/api/search/?q=matrix')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('movies', data)
```

---

## 🚀 Deployment

### Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG=False`
- [ ] Generate secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure static files
- [ ] Set up logging
- [ ] Enable HTTPS
- [ ] Configure backup strategy
- [ ] Set up monitoring

### Deploy to Render

**Step 1: Prepare Repository**
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

**Step 2: Create Render Account**
- Go to [render.com](https://render.com)
- Sign up (free tier available)

**Step 3: Create New Web Service**
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Render auto-detects `render.yaml`

**Step 4: Configure Environment Variables**
```
SECRET_KEY=<auto-generated>
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
MODEL_DIR=./models
```

**Step 5: Deploy**
- Click "Create Web Service"
- Wait for build to complete
- Access at `https://your-app.onrender.com`

### Deploy to Heroku

**Prerequisites:**
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login
```

**Deployment:**
```bash
# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set MODEL_DIR=./models

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Open app
heroku open
```

### Deploy with Docker

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "movie_recommendation.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**Build and Run:**
```bash
# Build
docker build -t movie-recommender .

# Run
docker run -p 8000:8000 -e DEBUG=False movie-recommender

# Access
http://localhost:8000
```

### Deploy to AWS

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.10 movie-recommender

# Create environment
eb create movie-recommender-env

# Deploy
eb deploy

# Open
eb open
```

---

## 📡 API Reference

### Endpoints

#### 1. Home Page / Search

**Endpoint:** `GET /`

**Description:** Display search interface

**Response:** HTML page

---

#### 2. Submit Search

**Endpoint:** `POST /`

**Content-Type:** `application/x-www-form-urlencoded`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| movie_name | string | Yes | Movie title to search |
| csrfmiddlewaretoken | string | Yes | CSRF token |

**Response:** HTML page with recommendations or error

---

#### 3. Search Movies (Autocomplete)

**Endpoint:** `GET /api/search/`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| q | string | Yes | Search query (min 2 chars) |

**Example Request:**
```bash
curl "http://localhost:8000/api/search/?q=matrix"
```

**Example Response:**
```json
{
  "movies": [
    "The Matrix",
    "The Matrix Reloaded",
    "The Matrix Revolutions"
  ],
  "count": 3
}
```

---

#### 4. Health Check

**Endpoint:** `GET /api/health/`

**Description:** Check service health and model status

**Example Request:**
```bash
curl "http://localhost:8000/api/health/"
```

**Example Response:**
```json
{
  "status": "healthy",
  "movies_loaded": 100000,
  "model_dir": "./models",
  "model_loaded": true
}
```

**Status Codes:**
- `200 OK` - Service healthy
- `503 Service Unavailable` - Service unhealthy

---

## 💻 Command Reference

### Virtual Environment

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Unix/macOS)
source venv/bin/activate

# Deactivate
deactivate
```

### Django Commands

```bash
# Server
python manage.py runserver              # Start dev server
python manage.py runserver 8080        # Custom port

# Database
python manage.py migrate                # Apply migrations
python manage.py makemigrations        # Create migrations
python manage.py showmigrations        # Show status

# Static files
python manage.py collectstatic         # Collect static files

# Shell
python manage.py shell                 # Django shell

# Testing
python manage.py test                  # Run tests
```

### Git Commands

```bash
# Clone
git clone <url>

# Status
git status

# Stage changes
git add .

# Commit
git commit -m "message"

# Push
git push origin main

# Pull
git pull origin main
```

---

## 🐛 Troubleshooting

### Common Issues

#### Issue 1: Module Not Found

**Problem:** `ModuleNotFoundError: No module named 'package'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

---

#### Issue 2: Model Not Found

**Problem:** `FileNotFoundError: Model files not found`

**Solution:**
```bash
# Check MODEL_DIR
echo $MODEL_DIR

# Verify files exist
ls -la models/  # or dir models\ on Windows

# Use demo model
export MODEL_DIR=./static

# Or train new model
python training/train.py
```

---

#### Issue 3: Port Already in Use

**Problem:** `Error: That port is already in use`

**Solution:**
```bash
# Use different port
python manage.py runserver 8080

# Or kill process (Unix/macOS)
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

#### Issue 4: Static Files Not Loading

**Problem:** CSS/images not displaying in production

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Verify settings
# STATIC_ROOT should be set
# WhiteNoise should be in MIDDLEWARE
```

---

#### Issue 5: Database Errors

**Problem:** `OperationalError: no such table`

**Solution:**
```bash
# Run migrations
python manage.py migrate

# If still failing, reset database
rm db.sqlite3
python manage.py migrate
```

---

#### Issue 6: Memory Error During Training

**Problem:** System crashes or `MemoryError` during training

**Solution:**
```python
# Reduce dataset size
trainer.train(data_path, max_movies=50000)

# Or reduce SVD components
trainer = MovieRecommenderTrainer(n_components=300)

# Or use higher quality threshold
trainer.train(data_path, quality_threshold='high')
```

See [training/guide.md - Troubleshooting](training/guide.md) for training-specific issues.

---

## ⚡ Best Practices

### Performance

1. **Use Production Server**
   ```bash
   # Don't use runserver in production
   gunicorn movie_recommendation.wsgi:application
   ```

2. **Enable Caching**
   ```python
   # Use Redis for production
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

3. **Optimize Database**
   - Use PostgreSQL in production
   - Add database indexes
   - Use connection pooling

4. **Enable Compression**
   - Enable gzip compression
   - Use CDN for static files
   - Optimize model files

### Security

1. **Environment Variables**
   - Never commit secrets
   - Use `.env` files
   - Rotate keys regularly

2. **Dependencies**
   ```bash
   # Check for outdated packages
   pip list --outdated
   
   # Update dependencies
   pip install --upgrade package_name
   ```

3. **Security Headers**
   ```python
   # Already in settings.py for production
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

### Development

1. **Code Quality**
   ```bash
   # Use linting
   pip install flake8 black
   
   # Check code
   flake8 recommender/
   
   # Format code
   black recommender/
   ```

2. **Version Control**
   - Commit frequently
   - Write descriptive messages
   - Use feature branches
   - Review before merging

3. **Documentation**
   - Add docstrings to functions
   - Comment complex logic
   - Update README when needed
   - Keep documentation current

---

## ❓ FAQ

### General

**Q: Do I need to train a model to use the system?**  
A: No! The project includes a pre-trained demo model with 2,000 movies. Just run and use.

**Q: What's the difference between `models/` and `static/`?**  
A: `static/` contains the demo model (2K movies). `models/` is for your custom trained models (created after training).

**Q: How do I switch between models?**  
A: Set the `MODEL_DIR` environment variable:
```bash
export MODEL_DIR=./static     # Demo model
export MODEL_DIR=./models     # Your trained model
```

### Training

**Q: How long does training take?**  
A: Depends on dataset size:
- 10K movies: ~2 minutes
- 100K movies: ~15 minutes
- 1M+ movies: ~60 minutes

**Q: How much memory do I need for training?**  
A: 
- 10K movies: 500MB RAM
- 100K movies: 2GB RAM
- 1M+ movies: 6-8GB RAM

For detailed training FAQ, see [training/guide.md - FAQ](training/guide.md)

### Deployment

**Q: Can I deploy for free?**  
A: Yes! Render and Heroku offer free tiers suitable for this project.

**Q: Do I need a database for deployment?**  
A: SQLite works for development. Use PostgreSQL for production (most platforms provide it).

**Q: How do I configure HTTPS?**  
A: Most cloud platforms (Render, Heroku) provide HTTPS automatically.

### Development

**Q: Can I modify the UI?**  
A: Yes! Edit the templates in `recommender/templates/recommender/`. All CSS is inline for easy modification.

**Q: How do I add new features?**  
A: 
1. Create a feature branch
2. Make changes in `recommender/views.py` or templates
3. Test locally
4. Update documentation
5. Submit pull request

---

## 📚 Additional Resources

### Documentation
- [README.md](README.md) - Quick start and overview
- [training/guide.md](training/guide.md) - Model training guide
- [CHANGELOG.md](CHANGELOG.md) - Version history

### External Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [pandas Documentation](https://pandas.pydata.org/)

### Community
- GitHub Issues - Bug reports and feature requests
- GitHub Discussions - Questions and community support

---

<div align="center">

**Need more help?** Check [training/guide.md](training/guide.md) for training help or open an issue on GitHub.

[⬆ Back to Top](#-table-of-contents)

</div>
