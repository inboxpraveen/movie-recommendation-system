"""
Advanced Movie Recommendation System - Training Pipeline
Optimized for TMDB Movies Dataset 2023 (930K+ movies)
"""

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix, save_npz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from nltk.stem.snowball import SnowballStemmer
import pickle
import json
from pathlib import Path
from ast import literal_eval
import warnings
warnings.filterwarnings('ignore')


class MovieRecommenderTrainer:
    def __init__(self, output_dir='./models', use_dimensionality_reduction=True, n_components=500):
        """
        Initialize the trainer with advanced configurations
        
        Args:
            output_dir: Directory to save trained models
            use_dimensionality_reduction: Use SVD to reduce memory footprint
            n_components: Number of latent features for SVD
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.use_svd = use_dimensionality_reduction
        self.n_components = n_components
        self.stemmer = SnowballStemmer('english')
        
    def load_data(self, data_path):
        """
        Load TMDB dataset from single CSV file
        
        Args:
            data_path: Path to TMDB_movie_dataset_v11.csv
        
        Returns:
            DataFrame with movie data
        """
        print("Loading TMDB dataset...")
        
        # Handle both file path and directory path
        if Path(data_path).is_file():
            df = pd.read_csv(data_path, low_memory=False)
        else:
            # Assume it's a directory
            csv_path = Path(data_path) / 'TMDB_movie_dataset_v11.csv'
            df = pd.read_csv(csv_path, low_memory=False)
        
        print(f"Loaded {len(df)} movies")
        print(f"Columns: {df.columns.tolist()}")
        
        return df
    
    def parse_json_column(self, col_data, key='name'):
        """
        Parse JSON-like string columns (genres, keywords, production_companies)
        Handles both string representation and actual lists
        """
        if pd.isna(col_data) or col_data == '' or col_data == '[]':
            return []
        
        try:
            # Try literal_eval first
            parsed = literal_eval(col_data) if isinstance(col_data, str) else col_data
            
            if isinstance(parsed, list):
                # Extract the specified key from each dict
                return [item[key] for item in parsed if isinstance(item, dict) and key in item]
            return []
        except:
            # Fallback: split by comma if it's a simple comma-separated string
            if isinstance(col_data, str):
                return [item.strip() for item in col_data.split(',') if item.strip()]
            return []
    
    def extract_director_from_companies(self, companies_data):
        """
        Extract primary production company as a proxy for director
        (TMDB dataset doesn't have separate crew/director info)
        """
        companies = self.parse_json_column(companies_data)
        return companies[0] if companies else None
    
    def clean_and_engineer_features(self, df, quality_threshold='medium'):
        """
        Advanced feature engineering pipeline for TMDB dataset
        
        Args:
            df: Input DataFrame
            quality_threshold: 'low', 'medium', or 'high' - filters by vote_count
        
        Returns:
            Processed DataFrame
        """
        print("Engineering features...")
        
        # Filter by quality threshold
        thresholds = {
            'low': 5,      # 5+ votes
            'medium': 50,  # 50+ votes (recommended)
            'high': 500    # 500+ votes (high quality only)
        }
        min_votes = thresholds.get(quality_threshold, 50)
        df = df[df['vote_count'] >= min_votes].copy()
        print(f"Filtered to {len(df)} movies with {min_votes}+ votes")
        
        # Filter only released movies
        df = df[df['status'] == 'Released'].copy()
        
        # Parse JSON columns
        print("Parsing genres, keywords, and production companies...")
        df['genres'] = df['genres'].apply(lambda x: self.parse_json_column(x, 'name'))
        df['keywords'] = df['keywords'].apply(lambda x: self.parse_json_column(x, 'name'))
        df['companies'] = df['production_companies'].apply(lambda x: self.parse_json_column(x, 'name'))
        df['countries'] = df['production_countries'].apply(lambda x: self.parse_json_column(x, 'name'))
        
        # Extract primary production company as director proxy
        df['primary_company'] = df['companies'].apply(lambda x: x[0] if x else None)
        
        # Process overview (plot summary)
        df['overview_clean'] = df['overview'].fillna('').astype(str)
        df['overview_words'] = df['overview_clean'].apply(
            lambda x: [word.lower() for word in x.split()[:50]]  # First 50 words
        )
        
        # Process tagline
        df['tagline_clean'] = df['tagline'].fillna('').astype(str)
        df['tagline_words'] = df['tagline_clean'].apply(
            lambda x: [word.lower() for word in x.split()]
        )
        
        # Clean and stem keywords
        df['keywords'] = df['keywords'].apply(
            lambda x: [self.stemmer.stem(kw.lower().replace(" ", "")) for kw in x[:15]]  # Top 15 keywords
        )
        
        # Clean genres
        df['genres'] = df['genres'].apply(
            lambda x: [genre.lower().replace(" ", "") for genre in x]
        )
        
        # Clean companies (top 3, with weight)
        df['companies_weighted'] = df['companies'].apply(
            lambda x: [x[0].lower().replace(" ", "")] * 2 if x and len(x) > 0 else []  # Weight first company
        )
        df['companies_clean'] = df['companies'].apply(
            lambda x: [comp.lower().replace(" ", "") for comp in x[:3]]
        )
        
        # Clean countries
        df['countries_clean'] = df['countries'].apply(
            lambda x: [country.lower().replace(" ", "") for country in x[:2]]
        )
        
        # Create comprehensive soup feature
        df['soup'] = (
            df['keywords'] + 
            df['genres'] * 2 +  # Weight genres more
            df['companies_weighted'] + 
            df['companies_clean'] +
            df['countries_clean'] +
            df['overview_words'] +
            df['tagline_words']
        )
        df['soup'] = df['soup'].apply(lambda x: ' '.join(x) if x else '')
        
        # Filter valid entries
        df = df[df['soup'].str.len() > 20].copy()
        df = df.dropna(subset=['title'])
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['title'], keep='first')
        
        # Sort by popularity (combination of vote_average and vote_count)
        df['quality_score'] = df['vote_average'] * np.log1p(df['vote_count'])
        df = df.sort_values('quality_score', ascending=False)
        
        if 'tconst' in df.columns and 'imdb_id' not in df.columns:
          df['imdb_id'] = df['tconst']

        df = df.reset_index(drop=True)
        
        print(f"Processed {len(df)} valid movies")
        return df
    
    def build_tfidf_matrix(self, df):
        """Build TF-IDF matrix with optimized parameters"""
        print("Building TF-IDF matrix...")
        
        # Adjust max_features based on dataset size
        n_movies = len(df)
        if n_movies < 10000:
            max_features = 10000
        elif n_movies < 100000:
            max_features = 15000
        else:
            max_features = 20000
        
        print(f"Using max_features={max_features} for {n_movies} movies")
        
        tfidf = TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 2),
            min_df=3,  # Increased for larger dataset
            max_df=0.7,  # More aggressive filtering
            stop_words='english',
            max_features=max_features,
            sublinear_tf=True  # Use log scaling
        )
        
        tfidf_matrix = tfidf.fit_transform(df['soup'])
        
        print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")
        sparsity = (1 - tfidf_matrix.nnz / (tfidf_matrix.shape[0] * tfidf_matrix.shape[1])) * 100
        print(f"Matrix sparsity: {sparsity:.2f}%")
        
        return tfidf_matrix, tfidf
    
    def compute_similarity_matrix(self, tfidf_matrix):
        """Compute similarity with optional dimensionality reduction"""
        if self.use_svd and tfidf_matrix.shape[0] > 1000:
            print(f"Applying SVD dimensionality reduction to {self.n_components} components...")
            
            # Adjust components based on matrix size
            n_components = min(
                self.n_components,
                tfidf_matrix.shape[0] - 1,
                tfidf_matrix.shape[1] - 1
            )
            
            svd = TruncatedSVD(n_components=n_components, random_state=42)
            reduced_matrix = svd.fit_transform(tfidf_matrix)
            
            explained_var = svd.explained_variance_ratio_.sum()
            print(f"Explained variance ratio: {explained_var:.3f}")
            print(f"Reduced matrix shape: {reduced_matrix.shape}")
            
            # For very large datasets, compute similarity in chunks
            if reduced_matrix.shape[0] > 50000:
                print("Computing similarity in chunks for large dataset...")
                chunk_size = 10000
                n_chunks = (reduced_matrix.shape[0] + chunk_size - 1) // chunk_size
                
                similarity_matrix = np.zeros((reduced_matrix.shape[0], reduced_matrix.shape[0]), dtype=np.float32)
                
                for i in range(n_chunks):
                    start_i = i * chunk_size
                    end_i = min((i + 1) * chunk_size, reduced_matrix.shape[0])
                    
                    chunk_sim = cosine_similarity(
                        reduced_matrix[start_i:end_i],
                        reduced_matrix
                    )
                    similarity_matrix[start_i:end_i, :] = chunk_sim
                    
                    if (i + 1) % 5 == 0:
                        print(f"Processed {i+1}/{n_chunks} chunks")
            else:
                print("Computing cosine similarity...")
                similarity_matrix = cosine_similarity(reduced_matrix)
            
            return similarity_matrix.astype(np.float32), svd
        else:
            print("Computing cosine similarity (no dimensionality reduction)...")
            similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
            return similarity_matrix.astype(np.float32), None
    
    def save_model(self, df, similarity_matrix, tfidf_vectorizer, svd_model=None):
        """Save all model artifacts efficiently"""
        print("Saving model artifacts...")
        
        # Save metadata DataFrame (essential columns only)
        metadata_df = df[[
            'id', 'title', 'release_date', 'primary_company', 
            'genres', 'vote_average', 'vote_count', 'popularity',
            'overview', 'imdb_id', 'poster_path'
        ]].copy()
        
        metadata_df.to_parquet(
            self.output_dir / 'movie_metadata.parquet',
            compression='gzip',
            index=True
        )
        
        # Save similarity matrix
        print("Saving similarity matrix...")
        if similarity_matrix.size > 10000000:  # > 10M elements
            # Save as sparse for very large matrices
            sparse_sim = csr_matrix(similarity_matrix)
            save_npz(self.output_dir / 'similarity_matrix.npz', sparse_sim)
            print(f"Saved as sparse matrix (size: {sparse_sim.data.nbytes / 1024**2:.1f} MB)")
        else:
            np.save(self.output_dir / 'similarity_matrix.npy', similarity_matrix)
            print(f"Saved as dense matrix (size: {similarity_matrix.nbytes / 1024**2:.1f} MB)")
        
        # Save title to index mapping
        title_to_idx = pd.Series(df.index, index=df['title']).to_dict()
        with open(self.output_dir / 'title_to_idx.json', 'w') as f:
            json.dump(title_to_idx, f)
        
        # Save TF-IDF vectorizer
        with open(self.output_dir / 'tfidf_vectorizer.pkl', 'wb') as f:
            pickle.dump(tfidf_vectorizer, f)
        
        # Save SVD model if used
        if svd_model:
            with open(self.output_dir / 'svd_model.pkl', 'wb') as f:
                pickle.dump(svd_model, f)
        
        # Save configuration
        config = {
            'n_movies': len(df),
            'use_svd': self.use_svd,
            'n_components': self.n_components if svd_model else None,
            'matrix_shape': similarity_matrix.shape,
            'dataset': 'TMDB 2023 (930K movies)'
        }
        with open(self.output_dir / 'config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Model saved to {self.output_dir}")
        
        # Print summary
        total_size = sum(
            f.stat().st_size 
            for f in self.output_dir.iterdir() 
            if f.is_file()
        ) / 1024**2
        print(f"Total model size: {total_size:.1f} MB")
    
    def train(self, data_path, quality_threshold='medium', max_movies=None):
        """
        Complete training pipeline
        
        Args:
            data_path: Path to CSV file or directory containing it
            quality_threshold: 'low', 'medium', or 'high'
            max_movies: Limit number of movies (None = all)
        """
        print("="*80)
        print("🎬 TMDB Movie Recommendation System Training")
        print("="*80)
        
        # Load data
        df = self.load_data(data_path)
        
        # Feature engineering
        df = self.clean_and_engineer_features(df, quality_threshold)
        
        # Limit dataset if specified
        if max_movies and len(df) > max_movies:
            df = df.head(max_movies)
            print(f"Limited to top {max_movies} movies by quality score")
        
        # Build TF-IDF matrix
        tfidf_matrix, tfidf_vectorizer = self.build_tfidf_matrix(df)
        
        # Compute similarity
        similarity_matrix, svd_model = self.compute_similarity_matrix(tfidf_matrix)
        
        # Save everything
        self.save_model(df, similarity_matrix, tfidf_vectorizer, svd_model)
        
        print("="*80)
        print("✅ Training completed successfully!")
        print("="*80)
        
        return df, similarity_matrix


# Example usage
if __name__ == "__main__":
    
    # Downloaded dataset
    path = "./TMDB  IMDB Movies Dataset.csv"
    
    # Configuration based on your needs:
    
    # For FULL dataset (930K+ movies) - Requires ~16GB RAM
    # trainer = MovieRecommenderTrainer(
    #     output_dir='./models_full',
    #     use_dimensionality_reduction=True,
    #     n_components=400
    # )
    # df, sim_matrix = trainer.train(path, quality_threshold='low')
    
    # For HIGH QUALITY dataset (~100K movies) - Recommended
    trainer = MovieRecommenderTrainer(
        output_dir='./models',
        use_dimensionality_reduction=True,
        n_components=500
    )
    df, sim_matrix = trainer.train(
        path, 
        quality_threshold='medium',  # 50+ votes
        max_movies=50000  # Top 100K by quality
    )
    
    # For MEDIUM dataset (~10K movies) - Fast training
    # trainer = MovieRecommenderTrainer(
    #     output_dir='./models_medium',
    #     use_dimensionality_reduction=False
    # )
    # df, sim_matrix = trainer.train(path, quality_threshold='high', max_movies=10000)
    
    print(f"\n📊 Final Statistics:")
    print(f"   Movies in model: {len(df):,}")
    print(f"   Similarity matrix: {sim_matrix.shape}")
    print(f"   Memory usage: {sim_matrix.nbytes / 1024**2:.1f} MB")

