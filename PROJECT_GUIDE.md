# 📘 Movie Recommendation System - Complete Project Guide

This guide contains everything you need to set up, develop, deploy, and maintain the Movie Recommendation System.

---

## 📑 Table of Contents

1. [Getting Started](#-getting-started)
2. [Installation](#-installation)
3. [Model Training](#-model-training)
4. [Configuration](#-configuration)
5. [Development](#-development)
6. [Deployment](#-deployment)
7. [API Reference](#-api-reference)
8. [Troubleshooting](#-troubleshooting)
9. [Best Practices](#-best-practices)

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:
- **Python 3.10+** installed
- **pip** (Python package manager)
- **Git** for version control
- **8GB RAM** (minimum) for training medium-sized models
- **Virtual environment** tool (venv, conda, or virtualenv)

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.10+ | 3.10+ |
| RAM | 4GB | 8GB+ |
| Storage | 2GB | 5GB+ |
| OS | Windows/macOS/Linux | Any |

---

## 💻 Installation

### Installation Steps

**Step 1: Clone Repository**
```bash
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
```

**Step 2: Create Virtual Environment**
```bash
# Create venv
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

**Step 3: Install Dependencies**
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**Step 4: Setup Environment (Optional)**
```bash
# Create .env file for custom configuration if needed
# Default settings work fine for local development
```

**Step 5: Initialize Database**
```bash
python manage.py migrate
```

**Step 6: Run Application**
```bash
python manage.py runserver
```

**Step 7: Access Application**

Open browser: http://localhost:8000

---

## 🎓 Model Training

### Quick Start Training

The system works with pre-trained models or you can train your own.

#### Option 1: Use Demo Model (Included)

The repository includes a demo model with 2,000+ movies in the `static/` directory. It works out of the box - no training needed!

#### Option 2: Train Your Own Model

**Prerequisites for Training:**
- Movie dataset (CSV format)
- Additional Python packages:
  ```bash
  pip install nltk kagglehub
  python -m nltk.downloader stopwords
  ```

**Basic Training Script:**

```python
from training.train import MovieRecommenderTrainer

# Initialize trainer
trainer = MovieRecommenderTrainer(
    output_dir='./models',
    use_dimensionality_reduction=True,
    n_components=500
)

# Train model
df, similarity_matrix = trainer.train(
    data_path='path/to/your/dataset.csv',
    quality_threshold='medium',  # Options: low, medium, high
    max_movies=100000            # Limit dataset size (None = all)
)

print(f"✅ Training complete! Trained on {len(df):,} movies")
```

### Dataset Requirements

Your CSV dataset should have these columns:
- `title` - Movie title (required)
- `genres` - Movie genres (required)
- `keywords` - Descriptive keywords (required)
- `production_companies` - Production companies (recommended)
- `overview` - Plot summary (recommended)
- `vote_average` - Rating 0-10 (recommended)
- `vote_count` - Number of votes (recommended)
- `release_date` - Release date (optional)
- `imdb_id` - IMDb ID (optional)
- `poster_path` - Poster image path (optional)

### Training Configurations

**Configuration 1: Quick Test (10K movies)**
```python
trainer = MovieRecommenderTrainer(
    output_dir='./models_test',
    use_dimensionality_reduction=False
)
df, sim = trainer.train(
    data_path,
    quality_threshold='high',  # 500+ votes only
    max_movies=10000
)
```
- **Time**: 2-3 minutes
- **Memory**: 500MB
- **Model Size**: 40MB
- **Use Case**: Testing, development

**Configuration 2: Production (100K movies)** ⭐ Recommended
```python
trainer = MovieRecommenderTrainer(
    output_dir='./models',
    use_dimensionality_reduction=True,
    n_components=500
)
df, sim = trainer.train(
    data_path,
    quality_threshold='medium',  # 50+ votes
    max_movies=100000
)
```
- **Time**: 15-20 minutes
- **Memory**: 2GB
- **Model Size**: 180MB
- **Use Case**: Production deployment

**Configuration 3: Full Dataset (1M+ movies)**
```python
trainer = MovieRecommenderTrainer(
    output_dir='./models_full',
    use_dimensionality_reduction=True,
    n_components=400
)
df, sim = trainer.train(
    data_path,
    quality_threshold='low',  # 5+ votes
    max_movies=None  # All movies
)
```
- **Time**: 45-60 minutes
- **Memory**: 6GB
- **Model Size**: 800MB
- **Use Case**: Comprehensive movie database

### Using Trained Models

After training, your models are saved to the specified `output_dir`:

```
models/
├── movie_metadata.parquet    # Movie details
├── similarity_matrix.npy     # Similarity scores
├── title_to_idx.json         # Title to index mapping
├── tfidf_vectorizer.pkl      # TF-IDF vectorizer
├── svd_model.pkl            # SVD model (if used)
└── config.json              # Model configuration
```

**Configure Django to use your models:**

Method 1: Environment Variable
```bash
export MODEL_DIR=./models
python manage.py runserver
```

Method 2: .env File
```env
MODEL_DIR=./models
```

Method 3: Settings.py
```python
# In movie_recommendation/settings.py
MODEL_DIR = os.path.join(BASE_DIR, 'models')
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Core Settings
SECRET_KEY=your-very-secure-secret-key-here-minimum-50-characters
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Model Configuration
MODEL_DIR=./models

# Database (SQLite by default, PostgreSQL for production)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# CORS (if using separate frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Admin Panel
ADMIN_ENABLED=False

# Deployment (for Render/Heroku)
RENDER_EXTERNAL_HOSTNAME=your-app.onrender.com
```

### Generating SECRET_KEY

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or use:
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
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}
```

---

## 🔧 Development

### Project Structure

```
movie-recommendation-system/
├── movie_recommendation/       # Django project settings
│   ├── settings.py            # Main configuration
│   ├── urls.py                # Root URL routing
│   └── wsgi.py               # WSGI application
│
├── recommender/               # Main application
│   ├── views.py              # Recommender logic
│   ├── urls.py               # App URL routing
│   └── templates/            # HTML templates
│       └── recommender/
│           ├── index.html    # Home/search page
│           ├── result.html   # Results page
│           └── error.html    # Error page
│
├── training/                  # Model training scripts
│   ├── train.py              # Training pipeline
│   ├── infer.py              # Inference examples
│   └── guide.md              # Training documentation
│
├── models/                    # Trained models (created after training)
│   ├── movie_metadata.parquet
│   ├── similarity_matrix.npy
│   └── title_to_idx.json
│
├── static/                    # Static files & demo model
│   ├── logo.png
│   ├── demo_model.parquet
│   └── top_2k_movie_data.parquet
│
├── logs/                      # Application logs (auto-created)
│
├── requirements.txt           # Python dependencies
├── README.md                 # Project overview
├── PROJECT_GUIDE.md          # Complete guide
├── CHANGELOG.md              # Version history
└── manage.py                 # Django management
```

### Running Development Server

```bash
# Standard server
python manage.py runserver

# Custom port
python manage.py runserver 8080

# Listen on all interfaces
python manage.py runserver 0.0.0.0:8000

# With specific settings
python manage.py runserver --settings=movie_recommendation.settings
```

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

### Django Management Commands

```bash
# Create superuser (if admin enabled)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Show migrations
python manage.py showmigrations

# Apply migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Django shell
python manage.py shell
```

### Viewing Logs

```bash
# Real-time logs (Linux/macOS)
tail -f logs/django.log

# Windows
Get-Content logs\django.log -Wait

# Last 100 lines
tail -n 100 logs/django.log
```

---

## 🚀 Deployment

### Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure static files
- [ ] Set up logging
- [ ] Enable HTTPS
- [ ] Test application thoroughly
- [ ] Set up monitoring
- [ ] Configure backup strategy

### Deploy to Render (Recommended)

**Step 1: Prepare Repository**
```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for deployment"
git push origin main
```

**Step 2: Create Render Account**
- Go to https://render.com
- Sign up (free tier available)

**Step 3: Create New Web Service**
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Render will auto-detect `render.yaml`

**Step 4: Configure Environment Variables**
In Render dashboard, add:
```
SECRET_KEY=<auto-generated>
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
MODEL_DIR=./models
```

**Step 5: Deploy**
- Click "Create Web Service"
- Wait for build to complete
- Access your app at `https://your-app.onrender.com`

### Deploy to Heroku

**Prerequisites:**
```bash
# Install Heroku CLI
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login
```

**Deployment Steps:**
```bash
# Create Heroku app
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

**Dockerfile (create if needed):**
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
# Build image
docker build -t movie-recommender .

# Run container
docker run -p 8000:8000 -e DEBUG=False movie-recommender

# Access app
# http://localhost:8000
```

### Deploy to AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.10 movie-recommender

# Create environment
eb create movie-recommender-env

# Deploy
eb deploy

# Open app
eb open
```

---

## 📡 API Reference

### Endpoints

#### 1. Main Page / Get Recommendations

**Endpoint:** `POST /`

**Content-Type:** `application/x-www-form-urlencoded`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| movie_name | string | Yes | Movie title to get recommendations for |
| csrfmiddlewaretoken | string | Yes | CSRF token |

**Response:** HTML page with recommendations

---

#### 2. Search Movies (Autocomplete)

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

#### 3. Health Check

**Endpoint:** `GET /api/health/`

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

---

## 🐛 Troubleshooting

### Common Issues

#### Issue 1: Module Not Found Error

**Problem:** `ModuleNotFoundError: No module named 'package_name'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

---

#### Issue 2: Model Not Found

**Problem:** `FileNotFoundError: Model files not found`

**Solution:**
```bash
# Check MODEL_DIR setting
echo $MODEL_DIR

# Verify model files exist
ls -la models/

# If missing, train a model or use demo model
# Demo model is in static/ directory
export MODEL_DIR=./static
```

---

#### Issue 3: Port Already in Use

**Problem:** `Error: That port is already in use`

**Solution:**
```bash
# Use different port
python manage.py runserver 8080

# Or kill process using port (Linux/macOS)
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

#### Issue 4: Static Files Not Loading

**Problem:** CSS/JS files not loading in production

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Verify STATIC_ROOT in settings
# Check WhiteNoise is in MIDDLEWARE
```

---

#### Issue 5: Database Errors

**Problem:** `OperationalError: no such table`

**Solution:**
```bash
# Run migrations
python manage.py migrate

# If still issues, reset database
rm db.sqlite3
python manage.py migrate
```

---

#### Issue 6: Memory Error During Training

**Problem:** `MemoryError` or system crashes during training

**Solution:**
```python
# Reduce dataset size
trainer.train(data_path, max_movies=50000)

# Or reduce SVD components
trainer = MovieRecommenderTrainer(n_components=300)

# Or increase quality threshold
trainer.train(data_path, quality_threshold='high')
```

---

## ⚡ Best Practices

### Performance Optimization

1. **Use Production Server**
   ```bash
   # Don't use runserver in production
   gunicorn movie_recommendation.wsgi:application
   ```

2. **Enable Caching**
   ```python
   # Use Redis for caching
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

3. **Optimize Database Queries**
   - Use select_related and prefetch_related
   - Add database indexes
   - Use connection pooling

4. **Enable Compression**
   - Enable gzip compression
   - Use CDN for static files
   - Optimize images

### Security Best Practices

1. **Never commit secrets**
   - Use `.env` files
   - Add `.env` to `.gitignore`
   - Use environment variables

2. **Keep dependencies updated**
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```

3. **Enable security headers**
   ```python
   # Already configured in settings.py
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

4. **Regular backups**
   - Backup database regularly
   - Backup model files
   - Version control everything

### Code Quality

1. **Follow PEP 8**
   ```bash
   pip install flake8
   flake8 recommender/
   ```

2. **Use type hints**
   ```python
   def get_recommendations(movie_id: int, n: int = 10) -> List[Dict]:
       pass
   ```

3. **Write tests**
   ```python
   from django.test import TestCase

   class RecommenderTests(TestCase):
       def test_recommendations(self):
           # Test logic
           pass
   ```

4. **Document code**
   - Add docstrings to functions
   - Comment complex logic
   - Update README when needed

---

## 📞 Support

### Resources

- **GitHub Issues**: Report bugs or request features
- **README.md**: Quick overview and setup
- **training/guide.md**: Model training details
- **CHANGELOG.md**: Version history

### Community

- Star the repository to show support
- Share with other developers
- Contribute improvements
- Report issues

---

<div align="center">

**Made with ❤️ for developers and movie lovers**

[⭐ Star on GitHub](https://github.com/yourusername/movie-recommendation-system)

</div>

