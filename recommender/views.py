from django.shortcuts import render
import pandas as pd
import pyarrow as pa

movies_data = pd.read_parquet("static/movie_db.parquet")
titles = movies_data['title']
indices = pd.Series(movies_data.index, index=movies_data['title'])

def main(request):
 
    if request.method == 'GET':
        return render(request, 'recommender/index.html', {})
    
    if request.method == 'POST':

        data = request.POST
        movie_name = data.get('movie_name').title()

        final_recommendations = []
        word_set = first_substring(all_titles,movie_name)
        print("word_set: ",word_set)
        distances, indices = knn_model.kneighbors(features.iloc[word_set,:].values.reshape(1,-1),n_neighbors=11)

        for i in range(0, len(distances.flatten())):
            final_recommendations.append(features.index[indices.flatten()[i]])

        print(final_recommendations)

        return render(request, 'recommender/result.html',{'movie_details':final_recommendations,'search_name':movie_name})
