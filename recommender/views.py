"""
Movie Recommendation System Views
Integrates with advanced TMDB model training system
"""
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional
from difflib import get_close_matches

import pandas as pd
import numpy as np
from scipy.sparse import load_npz
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

# Global cache for recommender system
_RECOMMENDER = None


class MovieRecommender:
    """Integrated recommender system matching training/infer.py logic"""
    
    def __init__(self, model_dir='models'):
        """Initialize with trained model directory"""
        self.model_dir = Path(model_dir)
        self.metadata = None
        self.similarity_matrix = None
        self.title_to_idx = None
        self.config = None
        self._load_models()
    
    def _load_models(self):
        """Load all model artifacts"""
        logger.info(f"Loading models from {self.model_dir}...")
        
        # Load metadata
        self.metadata = pd.read_parquet(self.model_dir / 'movie_metadata.parquet')
        
        # Load similarity matrix (sparse or dense)
        if (self.model_dir / 'similarity_matrix.npz').exists():
            self.similarity_matrix = load_npz(self.model_dir / 'similarity_matrix.npz').toarray()
        else:
            self.similarity_matrix = np.load(self.model_dir / 'similarity_matrix.npy')
        
        # Load title mapping
        with open(self.model_dir / 'title_to_idx.json', 'r') as f:
            self.title_to_idx = json.load(f)
        
        # Load config
        with open(self.model_dir / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        logger.info(f"Loaded {self.config['n_movies']:,} movies successfully")
    
    def find_movie(self, title: str) -> Optional[str]:
        """Find closest matching movie title"""
        matches = get_close_matches(title, self.title_to_idx.keys(), n=1, cutoff=0.6)
        return matches[0] if matches else None
    
    def search_movies(self, query: str, n: int = 20) -> List[str]:
        """Search movies by partial title"""
        query_lower = query.lower()
        return [title for title in self.title_to_idx.keys() 
                if query_lower in title.lower()][:n]
    
    def get_recommendations(
        self,
        movie_title: str,
        n: int = 15,
        min_rating: float = None
    ) -> Dict:
        """Get movie recommendations with optional filtering"""
        matched_title = self.find_movie(movie_title)
        if not matched_title:
            return {'error': f"Movie '{movie_title}' not found", 'suggestions': self.search_movies(movie_title, 5)}
        
        movie_idx = self.title_to_idx[matched_title]
        source_movie = self.metadata.iloc[movie_idx]
        
        # Get similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[movie_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:]  # Exclude self
        
        recommendations = []
        for idx, score in sim_scores:
            if len(recommendations) >= n:
                break
            
            movie = self.metadata.iloc[idx]
            
            # Rating filter
            if min_rating and movie['vote_average'] < min_rating:
                continue
            
            recommendations.append({
                'title': movie['title'],
                'release_date': movie['release_date'] if pd.notna(movie['release_date']) else 'Unknown',
                'production': movie['primary_company'] if pd.notna(movie['primary_company']) else 'Unknown',
                'genres': ', '.join(movie['genres'][:3]) if isinstance(movie['genres'], list) else 'N/A',
                'rating': f"{movie['vote_average']:.1f}/10" if pd.notna(movie['vote_average']) else 'N/A',
                'votes': f"{movie['vote_count']:,}" if pd.notna(movie['vote_count']) else 'N/A',
                'similarity_score': f"{score:.3f}",
                'imdb_id': movie['imdb_id'] if pd.notna(movie['imdb_id']) else None,
                'poster_url': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if pd.notna(movie['poster_path']) else None,
                'google_link': f"https://www.google.com/search?q={'+'.join(movie['title'].split())}+movie",
                'imdb_link': f"https://www.imdb.com/title/{movie['imdb_id']}" if pd.notna(movie['imdb_id']) else None
            })
        
        return {
            'query_movie': matched_title,
            'source_movie': {
                'production': source_movie['primary_company'] if pd.notna(source_movie['primary_company']) else 'Unknown',
                'rating': f"{source_movie['vote_average']:.1f}/10" if pd.notna(source_movie['vote_average']) else 'N/A',
                'genres': ', '.join(source_movie['genres'][:3]) if isinstance(source_movie['genres'], list) else 'N/A'
            },
            'recommendations': recommendations
        }


def _get_recommender():
    """Get or initialize the recommender singleton"""
    global _RECOMMENDER
    
    if _RECOMMENDER is None:
        # Check for model directory (configurable via settings or environment)
        model_dir = getattr(settings, 'MODEL_DIR', os.environ.get('MODEL_DIR', 'models'))
        
        # Fallback to static directory if models directory doesn't exist
        if not Path(model_dir).exists():
            model_dir = 'static'
            logger.warning(f"Model directory not found, using static directory")
        
        try:
            _RECOMMENDER = MovieRecommender(model_dir)
        except Exception as e:
            logger.error(f"Failed to load recommender: {e}")
            raise
    
    return _RECOMMENDER


@require_http_methods(["GET", "POST"])
def main(request):
    """
    Main view for movie recommendation system.
    GET: Display search interface
    POST: Process search and display recommendations
    """
    try:
        recommender = _get_recommender()
        titles_list = list(recommender.title_to_idx.keys())
    except Exception as e:
        logger.error(f"Failed to load recommender: {e}")
        return render(request, 'recommender/error.html', {
            'error_message': 'Failed to load movie database. Please ensure models are trained and available.'
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
    
    # Get recommendations
    result = recommender.get_recommendations(movie_name, n=15)
    
    if 'error' in result:
        return render(
            request,
            'recommender/index.html',
            {
                'all_movie_names': titles_list,
                'total_movies': len(titles_list),
                'input_movie_name': movie_name,
                'error_message': result['error'],
                'suggestions': result.get('suggestions', [])
            }
        )
    
    return render(
        request,
        'recommender/result.html',
        {
            'all_movie_names': titles_list,
            'input_movie_name': result['query_movie'],
            'source_movie': result['source_movie'],
            'recommended_movies': result['recommendations'],
            'total_recommendations': len(result['recommendations']),
        }
    )


@require_http_methods(["GET"])
def search_movies(request):
    """API endpoint for searching movies (autocomplete)"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'movies': [], 'count': 0})
    
    try:
        recommender = _get_recommender()
        matching_movies = recommender.search_movies(query, n=20)
        
        return JsonResponse({
            'movies': matching_movies,
            'count': len(matching_movies)
        })
        
    except Exception as e:
        logger.error(f"Error in search: {e}")
        return JsonResponse({'error': 'Search failed'}, status=500)


@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        recommender = _get_recommender()
        return JsonResponse({
            'status': 'healthy',
            'movies_loaded': recommender.config['n_movies'],
            'model_dir': str(recommender.model_dir),
            'model_loaded': True
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)
