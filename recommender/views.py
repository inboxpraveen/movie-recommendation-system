from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from .utils import *


def main(request):
 
    df = pd.read_csv('static/data.csv')    
    
    if request.method == 'GET':
        print(df.head())
        return render(request, 'recommender/index.html', {})
    
    if request.method == 'POST':
        print("inside post method")
        data = request.POST
        mn = data.get('movie_name').title()

        all_titles = [df2['title'][i] for i in range(len(df2['title']))]        
        if mn not in all_titles:
            return render(request, 'recommender/negative.html', {'movie_name': mn})

        count_matrix = CountVectorizer(stop_words='english').fit_transform(df2['soup'])
        df2 = df2.reset_index()
        indices = pd.Series(df2.index, index=df2['title'])
        
        result_final = get_recommendations(mn,count_matrix,indices,df2)
        names = []
        dates = []
        for i in range(len(result_final)):
            names.append(result_final.iloc[i][0])
            dates.append(result_final.iloc[i][1])

        return render(request, 'recommender/positive.html',{'movie_names':names,'movie_date':dates,'search_name':mn})
