from django.shortcuts import render
import pandas as pd
import pyarrow as pa

movies_data = pd.read_parquet("static/top_2k_movie_data.parquet")
titles = movies_data['title']
titles_list = titles.to_list()

def get_recommendations(movie_id_from_db,movie_db):

    try:
        sim_scores = list(enumerate(movie_db[movie_id_from_db]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:15] ## get top 15 Recommendations
        
        movie_indices = [i[0] for i in sim_scores]
        output = movies_data.iloc[movie_indices]
        output.reset_index(inplace=True, drop=True)

        response = []
        for i in range(len(output)):
            response.append({
                'movie_title':output['title'].iloc[i],
                'movie_release_date':output['release_date'].iloc[i],
                'movie_director':output['main_director'].iloc[i],
                'google_link':"https://www.google.com/search?q=" + '+'.join(output['title'].iloc[i].strip().split()) + " (" + output['release_date'].iloc[i].split("-")[0]+")"
            })
        return response
    except Exception as e:
        print("error: ",e)
        return []


def main(request):

    global titles_list, model

    if request.method == 'GET':
        return render(
                request,
                'recommender/index.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'',
                    'movie_found':'',
                    'recomendation_found':'',
                    'recommended_movies':[],
                    'input_movie_name':''
                }
            )

    if request.method == 'POST':

        data = request.POST
        movie_name = data.get('movie_name') ## get movie name from the frontend input field

        if movie_name in titles_list:
            idx = titles_list.index(movie_name)
        else:
            return render(
                request,
                'recommender/index.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'',
                    'recomendation_found':'',
                    'recommended_movies':[],
                    'input_movie_name':movie_name
                }
            )

        model = pa.parquet.read_table('static/demo_model.parquet').to_pandas()
        final_recommendations = get_recommendations(idx,model)
        if final_recommendations:
            return render(
                request,
                'recommender/result.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'yes',
                    'recomendation_found':'yes',
                    'recommended_movies':final_recommendations,
                    'input_movie_name':movie_name
                }
            )
        else:
            return render(
                request,
                'recommender/index.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'',
                    'recomendation_found':'',
                    'recommended_movies':[],
                    'input_movie_name':movie_name
                }
            )

