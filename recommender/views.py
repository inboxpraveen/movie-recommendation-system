from django.shortcuts import render
import pandas as pd
import pyarrow as pa

movies_data = pd.read_parquet("static/movie_db.parquet")
titles = movies_data['title']
indices = pd.Series(movies_data.index, index=movies_data['title'])


def get_recommendations(idx,df):
    sim_scores = list(enumerate(df[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    output = titles.iloc[movie_indices]
    output.reset_index(inplace=True, drop=True)
    return output


def main(request):
 
    if request.method == 'GET':
        return render(request, 'recommender/index.html', {})
    
    if request.method == 'POST':

        data = request.POST
        movie_name = data.get('movie_name').title()

        final_recommendations = []
        if movie_name in titles:
            idx = titles.index(movie_name)
            if idx < 15000:
                df = pa.parquet.read_table('static/model_01.parquet').to_pandas()
                print("loaded model 1")
            elif idx > 15000 and idx < 30000:
                df = pa.parquet.read_table('static/model_02.parquet').to_pandas()
                print("loaded model 2")
            elif idx > 30000:
                df = pa.parquet.read_table('static/model_03.parquet').to_pandas()
                print("loaded model 3")

            final_recommendations.append(get_recommendations(idx,df))
        else:
            print("movie name not found in dbbbbbbbbbbbbbbbbbbbbbb")

        print("final recommendations: ",final_recommendations)
            
        return render(request, 'recommender/result.html',{'movie_details':final_recommendations,'search_name':movie_name})
