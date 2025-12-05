"""
Advanced Movie Recommendation System - Inference Engine
Optimized for TMDB Movies Dataset 2023 (930K+ movies)
"""

import pandas as pd
import numpy as np
from scipy.sparse import load_npz
import pickle
import json
from pathlib import Path
from typing import List, Dict, Optional
from difflib import get_close_matches
import warnings
warnings.filterwarnings('ignore')


class MovieRecommender:
    def __init__(self, model_dir='./models'):
        """
        Initialize recommender with trained models
        
        Args:
            model_dir: Directory containing trained model artifacts
        """
        self.model_dir = Path(model_dir)
        self.metadata = None
        self.similarity_matrix = None
        self.title_to_idx = None
        self.config = None
        self.load_models()
    
    def load_models(self):
        """Load all model artifacts"""
        print("🎬 Loading TMDB Movie Recommendation Engine...")
        
        # Load metadata
        self.metadata = pd.read_parquet(self.model_dir / 'movie_metadata.parquet')
        
        # Load similarity matrix
        if (self.model_dir / 'similarity_matrix.npz').exists():
            print("Loading sparse similarity matrix...")
            self.similarity_matrix = load_npz(self.model_dir / 'similarity_matrix.npz').toarray()
        else:
            print("Loading dense similarity matrix...")
            self.similarity_matrix = np.load(self.model_dir / 'similarity_matrix.npy')
        
        # Load title mapping
        with open(self.model_dir / 'title_to_idx.json', 'r') as f:
            self.title_to_idx = json.load(f)
        
        # Load config
        with open(self.model_dir / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        print(f"✅ Loaded {self.config['n_movies']:,} movies from {self.config.get('dataset', 'dataset')}")
        print(f"   Model ready for inference!")
    
    def find_movie(self, title: str, threshold: float = 0.6) -> Optional[str]:
        """
        Fuzzy search for movie title
        
        Args:
            title: Movie title to search
            threshold: Similarity threshold (0-1)
        
        Returns:
            Best matching title or None
        """
        matches = get_close_matches(title, self.title_to_idx.keys(), n=1, cutoff=threshold)
        return matches[0] if matches else None
    
    def get_movie_details(self, movie_title: str) -> Dict:
        """Get detailed information about a movie"""
        matched_title = self.find_movie(movie_title)
        if not matched_title:
            return {'error': f"Movie '{movie_title}' not found"}
        
        idx = self.title_to_idx[matched_title]
        movie = self.metadata.iloc[idx]
        
        return {
            'title': movie['title'],
            'release_date': movie['release_date'],
            'production': movie['primary_company'],
            'genres': movie['genres'] if isinstance(movie['genres'], list) else [],
            'rating': f"{movie['vote_average']:.1f}/10",
            'votes': f"{movie['vote_count']:,}",
            'popularity': f"{movie['popularity']:.1f}",
            'overview': movie['overview'][:200] + '...' if len(str(movie['overview'])) > 200 else movie['overview'],
            'imdb_id': movie['imdb_id'] if pd.notna(movie['imdb_id']) else 'N/A',
            'poster_url': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if pd.notna(movie['poster_path']) else None
        }
    
    def get_recommendations(
        self, 
        movie_title: str, 
        n_recommendations: int = 10,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
        genres: Optional[List[str]] = None,
        min_rating: Optional[float] = None,
        exclude_same_company: bool = False
    ) -> Dict:
        """
        Get movie recommendations with advanced filtering
        
        Args:
            movie_title: Title of the movie to base recommendations on
            n_recommendations: Number of recommendations to return
            min_year: Minimum release year filter
            max_year: Maximum release year filter
            genres: List of genres to filter by
            min_rating: Minimum vote_average (0-10)
            exclude_same_company: Exclude movies by same production company
        
        Returns:
            Dictionary with recommendations and metadata
        """
        # Find exact or closest match
        matched_title = self.find_movie(movie_title)
        if not matched_title:
            suggestions = self.search_movies(movie_title, n=5)
            return {
                'error': f"Movie '{movie_title}' not found",
                'suggestions': suggestions if suggestions else "Try different spelling or search by partial title"
            }
        
        if matched_title != movie_title:
            print(f"📌 Found closest match: '{matched_title}'")
        
        # Get movie index
        movie_idx = self.title_to_idx[matched_title]
        source_movie = self.metadata.iloc[movie_idx]
        
        # Get similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[movie_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Exclude the input movie itself
        sim_scores = sim_scores[1:]
        
        # Apply filters
        recommendations = []
        source_company = source_movie['primary_company']
        
        for idx, score in sim_scores:
            if len(recommendations) >= n_recommendations:
                break
            
            movie = self.metadata.iloc[idx]
            
            # Year filter
            if min_year or max_year:
                try:
                    release_str = str(movie['release_date'])
                    if len(release_str) >= 4:
                        year = int(release_str.split('-')[-1]) if '-' in release_str else int(release_str[:4])
                        if min_year and year < min_year:
                            continue
                        if max_year and year > max_year:
                            continue
                except:
                    continue
            
            # Rating filter
            if min_rating and movie['vote_average'] < min_rating:
                continue
            
            # Genre filter
            if genres:
                movie_genres = movie['genres'] if isinstance(movie['genres'], list) else []
                movie_genres_lower = [g.lower().replace(' ', '') for g in movie_genres]
                genres_lower = [g.lower().replace(' ', '') for g in genres]
                if not any(g in movie_genres_lower for g in genres_lower):
                    continue
            
            # Company filter
            if exclude_same_company and movie['primary_company'] == source_company:
                continue
            
            # Build recommendation entry
            recommendations.append({
                'rank': len(recommendations) + 1,
                'title': movie['title'],
                'production': movie['primary_company'] if pd.notna(movie['primary_company']) else 'N/A',
                'release_date': movie['release_date'],
                'genres': movie['genres'] if isinstance(movie['genres'], list) else [],
                'rating': f"{movie['vote_average']:.1f}/10",
                'votes': f"{movie['vote_count']:,}",
                'similarity_score': float(score),
                'tmdb_id': int(movie['id']),
                'imdb_id': movie['imdb_id'] if pd.notna(movie['imdb_id']) else None,
                'poster_url': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if pd.notna(movie['poster_path']) else None,
                'google_search': f"https://www.google.com/search?q={'+'.join(movie['title'].split())}+movie",
                'imdb_link': f"https://www.imdb.com/title/{movie['imdb_id']}" if pd.notna(movie['imdb_id']) else None
            })
        
        return {
            'query_movie': matched_title,
            'query_details': {
                'production': source_movie['primary_company'],
                'genres': source_movie['genres'] if isinstance(source_movie['genres'], list) else [],
                'rating': f"{source_movie['vote_average']:.1f}/10",
                'release_date': source_movie['release_date']
            },
            'total_recommendations': len(recommendations),
            'recommendations': recommendations
        }
    
    def search_movies(self, query: str, n: int = 10, min_rating: float = None) -> List[str]:
        """
        Search for movies by partial title match
        
        Args:
            query: Search query
            n: Number of results
            min_rating: Minimum rating filter
        
        Returns:
            List of matching movie titles
        """
        query_lower = query.lower()
        matches = []
        
        for title in self.title_to_idx.keys():
            if query_lower in title.lower():
                if min_rating:
                    idx = self.title_to_idx[title]
                    rating = self.metadata.iloc[idx]['vote_average']
                    if rating < min_rating:
                        continue
                matches.append(title)
        
        return matches[:n]
    
    def get_top_rated(self, n: int = 10, min_votes: int = 1000, genres: List[str] = None) -> List[Dict]:
        """
        Get top-rated movies
        
        Args:
            n: Number of movies to return
            min_votes: Minimum vote count
            genres: Filter by genres
        
        Returns:
            List of top-rated movies
        """
        df = self.metadata[self.metadata['vote_count'] >= min_votes].copy()
        
        if genres:
            genres_lower = [g.lower().replace(' ', '') for g in genres]
            df = df[
                df['genres'].apply(
                    lambda x: any(
                        g in [genre.lower().replace(' ', '') for genre in (x if isinstance(x, list) else [])]
                        for g in genres_lower
                    ) if isinstance(x, list) else False
                )
            ]
        
        df = df.nlargest(n, 'vote_average')
        
        results = []
        for idx, row in df.iterrows():
            results.append({
                'title': row['title'],
                'rating': f"{row['vote_average']:.1f}/10",
                'votes': f"{row['vote_count']:,}",
                'release_date': row['release_date'],
                'genres': row['genres'] if isinstance(row['genres'], list) else [],
                'production': row['primary_company'] if pd.notna(row['primary_company']) else 'N/A'
            })
        
        return results
    
    def get_diverse_recommendations(
        self, 
        movie_title: str, 
        n_recommendations: int = 10,
        diversity_weight: float = 0.3
    ) -> Dict:
        """
        Get diverse recommendations using MMR (Maximal Marginal Relevance)
        
        Args:
            movie_title: Input movie title
            n_recommendations: Number of recommendations
            diversity_weight: Weight for diversity (0-1, higher = more diverse)
        
        Returns:
            Diverse list of recommendations
        """
        matched_title = self.find_movie(movie_title)
        if not matched_title:
            return {'error': f"Movie '{movie_title}' not found"}
        
        movie_idx = self.title_to_idx[matched_title]
        sim_to_query = self.similarity_matrix[movie_idx]
        
        selected = []
        candidates = list(range(len(self.metadata)))
        candidates.remove(movie_idx)
        
        for _ in range(min(n_recommendations, len(candidates))):
            mmr_scores = []
            
            for candidate in candidates:
                if candidate in selected:
                    continue
                
                relevance = sim_to_query[candidate]
                
                if selected:
                    max_sim = max(self.similarity_matrix[candidate][s] for s in selected)
                else:
                    max_sim = 0
                
                mmr = (1 - diversity_weight) * relevance - diversity_weight * max_sim
                mmr_scores.append((candidate, mmr))
            
            if not mmr_scores:
                break
            
            best = max(mmr_scores, key=lambda x: x[1])[0]
            selected.append(best)
            candidates.remove(best)
        
        recommendations = []
        for rank, idx in enumerate(selected, 1):
            movie = self.metadata.iloc[idx]
            recommendations.append({
                'rank': rank,
                'title': movie['title'],
                'production': movie['primary_company'] if pd.notna(movie['primary_company']) else 'N/A',
                'rating': f"{movie['vote_average']:.1f}/10",
                'genres': movie['genres'] if isinstance(movie['genres'], list) else [],
                'similarity_score': float(sim_to_query[idx])
            })
        
        return {
            'query_movie': matched_title,
            'recommendations': recommendations
        }
    
    def print_recommendations(self, results: Dict, show_scores: bool = False):
        """Pretty print recommendations"""
        if 'error' in results:
            print(f"\n❌ {results['error']}")
            if 'suggestions' in results:
                sugg = results['suggestions']
                if isinstance(sugg, list) and sugg:
                    print("\n💡 Did you mean:")
                    for s in sugg[:5]:
                        print(f"   • {s}")
                elif isinstance(sugg, str):
                    print(f"\n💡 {sugg}")
            return
        
        print(f"\n{'='*100}")
        print(f"🎬 Recommendations for: {results['query_movie']}")
        if 'query_details' in results:
            details = results['query_details']
            genres_str = ", ".join(details['genres'][:3]) if details['genres'] else 'N/A'
            print(f"   Production: {details['production']} | Rating: {details['rating']} | Genres: {genres_str}")
        print(f"{'='*100}\n")
        
        for rec in results['recommendations']:
            score_str = f" [Similarity: {rec['similarity_score']:.3f}]" if show_scores else ""
            genres_str = ", ".join(rec['genres'][:3]) if rec['genres'] else 'N/A'
            
            print(f"{rec['rank']:2d}. {rec['title']}")
            print(f"    ⭐ {rec['rating']} ({rec['votes']} votes) | 📅 {rec['release_date']}")
            print(f"    🎭 {genres_str} | 🏢 {rec['production']}{score_str}")
            
            if rec.get('imdb_link'):
                print(f"    🔗 {rec['imdb_link']}")
            print()


# Example usage
if __name__ == "__main__":
    # Initialize recommender
    recommender = MovieRecommender(model_dir='./models')
    
    print("\n" + "="*100)
    print("🎬 TMDB Movie Recommendation System - Examples")
    print("="*100)
    
    # Example 1: Basic recommendations
    print("\n📌 Example 1: Recommendations for 'Inception'")
    print("-" * 100)
    results = recommender.get_recommendations("Inception", n_recommendations=5)
    recommender.print_recommendations(results, show_scores=True)
    
    # Example 2: Filtered recommendations
    print("\n📌 Example 2: Recent Action movies like 'The Dark Knight'")
    print("-" * 100)
    results = recommender.get_recommendations(
        "The Dark Knight",
        n_recommendations=5,
        min_year=2015,
        genres=['Action'],
        min_rating=7.0
    )
    recommender.print_recommendations(results)
    
    # Example 3: Top rated movies
    print("\n📌 Example 3: Top Rated Sci-Fi Movies")
    print("-" * 100)
    top_scifi = recommender.get_top_rated(n=5, min_votes=5000, genres=['Science Fiction'])
    for i, movie in enumerate(top_scifi, 1):
        print(f"{i}. {movie['title']} - {movie['rating']} ({movie['votes']} votes)")
    
    # Example 4: Movie details
    print("\n📌 Example 4: Movie Details")
    print("-" * 100)
    details = recommender.get_movie_details("Interstellar")
    if 'error' not in details:
        print(f"Title: {details['title']}")
        print(f"Rating: {details['rating']} ({details['votes']} votes)")
        print(f"Genres: {', '.join(details['genres'])}")
        print(f"Production: {details['production']}")
        print(f"Overview: {details['overview']}")
    
    # Example 5: Interactive mode
    print("\n" + "="*100)
    print("🎮 Interactive Mode")
    print("="*100)
    
    movie_name = input("\n🎬 Enter a movie title (or press Enter for random): ").strip()
    if not movie_name:
        movie_name = "The Matrix"
    
    results = recommender.get_recommendations(movie_name, n_recommendations=10, min_rating=6.5)
    recommender.print_recommendations(results, show_scores=True)
