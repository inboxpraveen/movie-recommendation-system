from django.shortcuts import render
import pandas as pd
import pyarrow as pa

movies_data = pd.read_parquet("static/top_10k_movie_data.parquet")
titles = movies_data['title']
titles_list = titles.to_list()


def get_recommendations(idx,df,offset=0):
    sim_scores = list(enumerate(df[idx+offset]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:25]
    movie_indices = [i[0] for i in sim_scores]
    output = titles.iloc[movie_indices]
    output.reset_index(inplace=True, drop=True)
    return output


def main(request):
    global titles_list
    if request.method == 'GET':
        return render(request, 'recommender/index.html', {'all_movie_names':titles_list})
    
    if request.method == 'POST':

        data = request.POST
        movie_name = data.get('movie_name')
        final_recommendations = []

        if movie_name in titles_list:
            idx = titles_list.index(movie_name)
            offset = 0
            df = pa.parquet.read_table('static/demo_model.parquet').to_pandas()
            final_recommendations.extend(get_recommendations(idx,df,offset).to_list())

        if final_recommendations:
            return render(request, 'recommender/result.html',{'movie_details':final_recommendations,'search_name':movie_name,'empty':''})
        else:
            return render(request, 'recommender/result.html',{'movie_details':final_recommendations,'search_name':movie_name,'empty':'yes'})
