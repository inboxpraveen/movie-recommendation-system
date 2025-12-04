# 🔌 API Documentation

## Movie Recommendation System API Reference

This document provides detailed information about the API endpoints available in the Movie Recommendation System.

---

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

---

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

---

## Endpoints

### 1. Home Page / Get Recommendations

Get movie recommendations based on a selected movie.

#### Request

```http
POST /
Content-Type: application/x-www-form-urlencoded
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| movie_name | string | Yes | Exact name of the movie from the database |
| csrfmiddlewaretoken | string | Yes | CSRF token for form submission |

**Example Request:**

```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "movie_name=The Matrix" \
  -d "csrfmiddlewaretoken=YOUR_CSRF_TOKEN"
```

#### Response

**Success (200 OK):**

Returns HTML page with recommendations or renders the result template.

**Movie Not Found:**

Returns HTML page with error message indicating movie not found in database.

---

### 2. Search Movies (Autocomplete)

Search for movies by name with autocomplete functionality.

#### Request

```http
GET /api/search/?q={query}
```

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| q | string | Yes | Search query (minimum 2 characters) |

**Example Request:**

```bash
curl -X GET "http://localhost:8000/api/search/?q=matrix"
```

#### Response

**Success (200 OK):**

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

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| movies | array | List of matching movie titles (max 20) |
| count | integer | Number of results returned |

**Error (500 Internal Server Error):**

```json
{
  "error": "Search failed"
}
```

**Example with cURL:**

```bash
# Search for movies containing "inception"
curl -X GET "http://localhost:8000/api/search/?q=inception"

# Response:
# {
#   "movies": ["Inception", "Inception: The Cobol Job"],
#   "count": 2
# }
```

**Example with JavaScript:**

```javascript
fetch('/api/search/?q=matrix')
  .then(response => response.json())
  .then(data => {
    console.log(`Found ${data.count} movies:`, data.movies);
  })
  .catch(error => console.error('Error:', error));
```

**Example with Python:**

```python
import requests

response = requests.get('http://localhost:8000/api/search/?q=matrix')
data = response.json()

print(f"Found {data['count']} movies:")
for movie in data['movies']:
    print(f"  - {movie}")
```

---

### 3. Health Check

Check the health status of the application and verify data is loaded.

#### Request

```http
GET /api/health/
```

**No parameters required.**

**Example Request:**

```bash
curl -X GET "http://localhost:8000/api/health/"
```

#### Response

**Healthy (200 OK):**

```json
{
  "status": "healthy",
  "movies_loaded": 2000,
  "model_loaded": true
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| status | string | Health status: "healthy" or "unhealthy" |
| movies_loaded | integer | Number of movies in database |
| model_loaded | boolean | Whether recommendation model is loaded |

**Unhealthy (503 Service Unavailable):**

```json
{
  "status": "unhealthy",
  "error": "Failed to load movie data"
}
```

**Use Cases:**

1. **Monitoring**: Check application health regularly
2. **Load Balancers**: Use for health checks
3. **Debugging**: Verify data is loaded correctly
4. **Deployment**: Verify successful deployment

**Example Monitoring Script:**

```bash
#!/bin/bash
# health_check.sh

response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health/)

if [ $response -eq 200 ]; then
    echo "✓ Application is healthy"
    exit 0
else
    echo "✗ Application is unhealthy (HTTP $response)"
    exit 1
fi
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Service temporarily unavailable |

### Error Response Format

```json
{
  "error": "Error message describing what went wrong"
}
```

---

## Rate Limiting

Currently, there are no rate limits implemented. For production use, consider implementing rate limiting to prevent abuse.

**Recommended Implementation:**

```python
# Using django-ratelimit
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='100/h')
def search_movies(request):
    # ... endpoint logic
```

---

## CORS (Cross-Origin Resource Sharing)

CORS is configured in `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]
```

To modify allowed origins, update the `CORS_ALLOWED_ORIGINS` environment variable.

---

## Pagination

Currently, API responses are limited to:
- Search results: 20 movies maximum
- Recommendations: 15 movies (configurable)

Future versions may include pagination support.

---

## Data Models

### Movie Object

```json
{
  "movie_title": "The Matrix",
  "movie_release_date": "1999-03-31",
  "movie_director": "Lana Wachowski, Lilly Wachowski",
  "similarity_score": "0.95",
  "google_link": "https://www.google.com/search?q=The+Matrix+(1999)",
  "imdb_link": "https://www.imdb.com/find?q=The+Matrix"
}
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| movie_title | string | Title of the movie |
| movie_release_date | string | Release date (YYYY-MM-DD format) |
| movie_director | string | Director name(s) |
| similarity_score | string | Similarity score (0.00-1.00) |
| google_link | string | Google search URL |
| imdb_link | string | IMDb search URL |

---

## Code Examples

### JavaScript (Frontend Integration)

```javascript
class MovieRecommender {
  constructor(baseUrl = '') {
    this.baseUrl = baseUrl;
  }

  async searchMovies(query) {
    try {
      const response = await fetch(`${this.baseUrl}/api/search/?q=${encodeURIComponent(query)}`);
      if (!response.ok) throw new Error('Search failed');
      return await response.json();
    } catch (error) {
      console.error('Error searching movies:', error);
      return { movies: [], count: 0 };
    }
  }

  async checkHealth() {
    try {
      const response = await fetch(`${this.baseUrl}/api/health/`);
      return await response.json();
    } catch (error) {
      console.error('Error checking health:', error);
      return { status: 'unhealthy' };
    }
  }
}

// Usage
const recommender = new MovieRecommender();

// Search movies
recommender.searchMovies('matrix').then(data => {
  console.log('Found movies:', data.movies);
});

// Check health
recommender.checkHealth().then(status => {
  console.log('Service status:', status.status);
});
```

### Python (External Integration)

```python
import requests
from typing import List, Dict, Optional

class MovieRecommenderClient:
    """Client for Movie Recommendation System API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def search_movies(self, query: str) -> Optional[List[str]]:
        """
        Search for movies by name.
        
        Args:
            query: Search query string
            
        Returns:
            List of movie titles or None if error
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/search/",
                params={"q": query}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("movies", [])
        except requests.RequestException as e:
            print(f"Error searching movies: {e}")
            return None
    
    def check_health(self) -> Dict:
        """
        Check service health.
        
        Returns:
            Health status dictionary
        """
        try:
            response = self.session.get(f"{self.base_url}/api/health/")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error checking health: {e}")
            return {"status": "unhealthy", "error": str(e)}

# Usage
client = MovieRecommenderClient()

# Search movies
movies = client.search_movies("matrix")
if movies:
    print(f"Found {len(movies)} movies:")
    for movie in movies:
        print(f"  - {movie}")

# Check health
health = client.check_health()
print(f"Service status: {health['status']}")
if health['status'] == 'healthy':
    print(f"Movies loaded: {health['movies_loaded']}")
```

### cURL Examples

```bash
# Search for movies
curl -X GET "http://localhost:8000/api/search/?q=inception" \
  -H "Accept: application/json"

# Check health
curl -X GET "http://localhost:8000/api/health/" \
  -H "Accept: application/json"

# Pretty print JSON response (with jq)
curl -s "http://localhost:8000/api/search/?q=matrix" | jq .
```

---

## Webhook Support

Currently not implemented. Future versions may include webhook support for:
- New recommendation requests
- User activity tracking
- System events

---

## Best Practices

### 1. Always Handle Errors

```javascript
try {
  const response = await fetch('/api/search/?q=matrix');
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const data = await response.json();
} catch (error) {
  console.error('API request failed:', error);
}
```

### 2. Implement Caching

```javascript
const cache = new Map();

async function searchWithCache(query) {
  if (cache.has(query)) {
    return cache.get(query);
  }
  
  const data = await fetchSearchResults(query);
  cache.set(query, data);
  return data;
}
```

### 3. Use Debouncing for Search

```javascript
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

const debouncedSearch = debounce(searchMovies, 300);
```

### 4. Validate Inputs

```javascript
function searchMovies(query) {
  if (!query || query.length < 2) {
    console.warn('Query too short');
    return;
  }
  
  if (query.length > 100) {
    console.warn('Query too long');
    return;
  }
  
  // Proceed with search
}
```

---

## Troubleshooting

### Common Issues

**1. CORS Errors**

**Problem**: API requests fail with CORS errors

**Solution**: 
- Ensure your origin is in `CORS_ALLOWED_ORIGINS`
- Check that `corsheaders` is properly configured

**2. Empty Search Results**

**Problem**: Search returns no results

**Solution**:
- Verify query is at least 2 characters
- Check movie database is loaded
- Ensure correct movie names

**3. Health Check Fails**

**Problem**: Health endpoint returns 503

**Solution**:
- Check if movie data files exist in `static/` directory
- Verify file permissions
- Check application logs

---

## Future API Enhancements

Planned features for future versions:

- [ ] User authentication endpoints
- [ ] Recommendation history API
- [ ] Rating submission endpoint
- [ ] Advanced filtering options
- [ ] Batch recommendation requests
- [ ] WebSocket support for real-time updates
- [ ] GraphQL API
- [ ] API versioning (v2, v3)

---

## Support

For API-related questions or issues:
- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check README.md for general information
- **Community**: Join GitHub Discussions

---

**Last Updated**: December 4, 2024  
**API Version**: 1.0.0  
**Stability**: Stable ✅

---

<div align="center">

**Happy Coding! 🚀**

[View on GitHub](https://github.com/yourusername/movie-recommendation-system)

</div>

