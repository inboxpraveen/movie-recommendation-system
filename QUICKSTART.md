# ⚡ Quick Start Guide

Get the Movie Recommendation System up and running in 5 minutes!

## 🎯 Prerequisites

Before you begin, ensure you have:
- Python 3.10 or higher installed
- pip (Python package manager)
- Git (for cloning the repository)

## 🚀 Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 5.0
- Pandas
- PyArrow
- Gunicorn
- And other required packages

### Step 4: Set Up Environment Variables

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

**Optional**: Edit `.env` file if needed (default values work fine for local development).

### Step 5: Run Migrations

```bash
python manage.py migrate
```

### Step 6: Collect Static Files (Optional for development)

```bash
python manage.py collectstatic --noinput
```

### Step 7: Start the Server

```bash
python manage.py runserver
```

### Step 8: Open Your Browser

Navigate to: **http://localhost:8000**

🎉 **That's it!** You should see the Movie Recommendation System home page.

## 📖 Usage

1. **Type a movie name** in the search box (e.g., "The Matrix")
2. **Select from suggestions** or type the full name
3. **Click "Get Recommendations"**
4. **Browse similar movies** and click links to learn more

## 🎬 Quick Demo

Try these movies for great recommendations:
- The Matrix
- The Shawshank Redemption
- Inception
- The Dark Knight
- Pulp Fiction

## 🔧 Common Issues

### Port Already in Use

If port 8000 is busy:

```bash
# Windows
python manage.py runserver 8080

# macOS/Linux
python manage.py runserver 0.0.0.0:8080
```

Then visit: http://localhost:8080

### Static Files Not Loading

```bash
python manage.py collectstatic --clear --noinput
```

### Module Not Found Error

```bash
pip install -r requirements.txt --upgrade
```

### Permission Denied (macOS/Linux)

```bash
chmod +x build.sh
```

## 🎨 Customization

### Change Number of Recommendations

Edit `recommender/views.py`:

```python
recommendations = get_recommendations(movie_idx, top_n=20)  # Change 15 to 20
```

### Customize Colors

Edit the CSS in `recommender/templates/recommender/index.html`:

```css
:root {
    --primary-color: #6366f1;  /* Change to your color */
    --secondary-color: #8b5cf6;  /* Change to your color */
}
```

### Add Your Own Movies

Replace `static/top_2k_movie_data.parquet` with your own movie dataset (must have same columns).

## 📱 Testing on Mobile

1. Find your local IP address:
   - **Windows**: `ipconfig`
   - **macOS/Linux**: `ifconfig` or `ip addr`

2. Start server with:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

3. On your mobile device (same network), visit:
   ```
   http://YOUR_IP:8000
   ```

## 🚀 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Browse [CHANGELOG.md](CHANGELOG.md) for version history

## 💡 Tips

- The first recommendation query may be slow (model loading). Subsequent queries are fast!
- Autocomplete starts after typing 2+ characters
- The demo includes 2,000+ popular movies
- Click movie titles to see details on Google/IMDb

## 🆘 Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/movie-recommendation-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/movie-recommendation-system/discussions)
- **Email**: your.email@example.com

## 🎓 Learn More

- [Django Documentation](https://docs.djangoproject.com/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

**Enjoy discovering great movies! 🎬🍿**

