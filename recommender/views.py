from django.shortcuts import render
import pandas as pd
import pyarrow as pa

movies_data = pd.read_parquet("static/movie_db.parquet")
titles = movies_data['title']
indices = pd.Series(movies_data.index, index=movies_data['title'])


def get_recommendations(title,df):
    idx = indices[title]
    sim_scores = list(enumerate(df[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]


def main(request):
 
    if request.method == 'GET':
        return render(request, 'recommender/index.html', {})
    
    if request.method == 'POST':

        data = request.POST
        movie_name = data.get('movie_name').title()

        final_recommendations = []

        return render(request, 'recommender/result.html',{'movie_details':final_recommendations,'search_name':movie_name})
