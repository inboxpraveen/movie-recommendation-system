"""
Movie Recommendation System Views
Handles movie search and recommendation logic with efficient caching
"""
import logging
from functools import lru_cache
from typing import Dict, List, Optional

import pandas as pd
import pyarrow.parquet as pq
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

# Global cache for movie data (loaded once)
_MOVIES_DATA: Optional[pd.DataFrame] = None
_TITLES_LIST: Optional[List[str]] = None
_SIMILARITY_MODEL: Optional[pd.DataFrame] = None


def _load_movie_data() -> tuple[pd.DataFrame, List[str]]:
    """
    Load movie data from parquet file with caching.
    Returns: tuple of (movies_dataframe, titles_list)
    """
    global _MOVIES_DATA, _TITLES_LIST
    
    if _MOVIES_DATA is None or _TITLES_LIST is None:
        try:
            logger.info("Loading movie data from parquet file...")
            _MOVIES_DATA = pd.read_parquet("static/top_2k_movie_data.parquet")
            _TITLES_LIST = _MOVIES_DATA['title'].tolist()
            logger.info(f"Successfully loaded {len(_TITLES_LIST)} movies")
        except Exception as e:
            logger.error(f"Error loading movie data: {e}")
            raise
    
    return _MOVIES_DATA, _TITLES_LIST


def _load_similarity_model() -> pd.DataFrame:
    """
    Load similarity model from parquet file with lazy loading.
    This is loaded only when needed (when getting recommendations).
    """
    global _SIMILARITY_MODEL
    
    if _SIMILARITY_MODEL is None:
        try:
            logger.info("Loading similarity model...")
            _SIMILARITY_MODEL = pq.read_table('static/demo_model.parquet').to_pandas()
            logger.info("Successfully loaded similarity model")
        except Exception as e:
            logger.error(f"Error loading similarity model: {e}")
            raise
    
    return _SIMILARITY_MODEL


def get_recommendations(movie_id: int, top_n: int = 15) -> List[Dict[str, str]]:
    """
    Get movie recommendations based on similarity scores.
    
    Args:
        movie_id: Index of the movie in the dataset
        top_n: Number of recommendations to return (default: 15)
    
    Returns:
        List of dictionaries containing movie details
    """
    try:
        movies_data, _ = _load_movie_data()
        similarity_model = _load_similarity_model()
        
        # Get similarity scores for the given movie
        sim_scores = list(enumerate(similarity_model[movie_id]))
        
        # Sort by similarity score (descending)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N recommendations (excluding the movie itself)
        sim_scores = sim_scores[1:top_n + 1]
        
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        
        # Get movie details
        recommended_movies = movies_data.iloc[movie_indices].copy()
        recommended_movies['similarity_score'] = [score[1] for score in sim_scores]
        
        # Format response
        response = []
        for _, row in recommended_movies.iterrows():
            release_year = row['release_date'].split("-")[0] if pd.notna(row['release_date']) else "Unknown"
            movie_title = row['title']
            
            response.append({
                'movie_title': movie_title,
                'movie_release_date': row['release_date'] if pd.notna(row['release_date']) else "Unknown",
                'movie_director': row['main_director'] if pd.notna(row['main_director']) else "Unknown",
                'similarity_score': f"{row['similarity_score']:.2f}",
                'google_link': f"https://www.google.com/search?q={'+'.join(movie_title.strip().split())}+({release_year})",
                'imdb_link': f"https://www.imdb.com/find?q={'+'.join(movie_title.strip().split())}"
            })
        
        logger.info(f"Generated {len(response)} recommendations for movie_id {movie_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        return []


@require_http_methods(["GET", "POST"])
def main(request):
    """
    Main view for movie recommendation system.
    GET: Display search interface
    POST: Process search and display recommendations
    """
    try:
        movies_data, titles_list = _load_movie_data()
    except Exception as e:
        logger.error(f"Failed to load movie data: {e}")
        return render(request, 'recommender/error.html', {
            'error_message': 'Failed to load movie database. Please try again later.'
        })
    
    if request.method == 'GET':
        return render(
            request,
            'recommender/index.html',
            {
                'all_movie_names': titles_list,
                'total_movies': len(titles_list),
            }
        )
    
    # POST request - process search
    movie_name = request.POST.get('movie_name', '').strip()
    
    if not movie_name:
        return render(
            request,
            'recommender/index.html',
            {
                'all_movie_names': titles_list,
                'total_movies': len(titles_list),
                'error_message': 'Please enter a movie name.',
            }
        )
    
    # Check if movie exists in database
    if movie_name not in titles_list:
        return render(
            request,
            'recommender/index.html',
            {
                'all_movie_names': titles_list,
                'total_movies': len(titles_list),
                'input_movie_name': movie_name,
                'error_message': f'Movie "{movie_name}" not found in our database.',
            }
        )
    
    # Get movie index and recommendations
    movie_idx = titles_list.index(movie_name)
    recommendations = get_recommendations(movie_idx, top_n=15)
    
    if not recommendations:
        return render(
            request,
            'recommender/index.html',
            {
                'all_movie_names': titles_list,
                'total_movies': len(titles_list),
                'input_movie_name': movie_name,
                'error_message': 'Could not generate recommendations. Please try again.',
            }
        )
    
    return render(
        request,
        'recommender/result.html',
        {
            'all_movie_names': titles_list,
            'input_movie_name': movie_name,
            'recommended_movies': recommendations,
            'total_recommendations': len(recommendations),
        }
    )


@require_http_methods(["GET"])
def search_movies(request):
    """
    API endpoint for searching movies (autocomplete).
    Returns JSON list of matching movie titles.
    """
    query = request.GET.get('q', '').strip().lower()
    
    if len(query) < 2:
        return JsonResponse({'movies': []})
    
    try:
        _, titles_list = _load_movie_data()
        
        # Filter movies matching the query
        matching_movies = [
            title for title in titles_list 
            if query in title.lower()
        ][:20]  # Limit to 20 results
        
        return JsonResponse({
            'movies': matching_movies,
            'count': len(matching_movies)
        })
        
    except Exception as e:
        logger.error(f"Error in search: {e}")
        return JsonResponse({'error': 'Search failed'}, status=500)


@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for monitoring.
    """
    try:
        movies_data, titles_list = _load_movie_data()
        return JsonResponse({
            'status': 'healthy',
            'movies_loaded': len(titles_list),
            'model_loaded': _SIMILARITY_MODEL is not None
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)
