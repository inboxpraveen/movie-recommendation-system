from django.shortcuts import render
import pandas as pd
import pickle

features = pd.read_parquet("/static/features.parquet")
knn_model = pickle.load(open('/static/model.pkl', 'rb'))

def main(request):
 
    if request.method == 'GET':
        return render(request, 'recommender/index.html', {})
    
    if request.method == 'POST':

        data = request.POST
        movie_name = data.get('movie_name').title()
        final_recommendations = []
        
        
        
        res = {}
        for i in range(len(result_final)):
            res.update({
                result_final.iloc[i][0]:result_final.iloc[i][1]
            })

        return render(request, 'recommender/result.html',{'movie_details':res,'search_name':mn})
