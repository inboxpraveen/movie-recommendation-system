from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from .utils import *

df = pd.read_csv('static/data.csv')
count_matrix = CountVectorizer(stop_words='english').fit_transform(df['soup'])
df = df.reset_index()
all_titles = df["title"].to_list()
indices = pd.Series(df.index, index=df['title'])


def main(request):
 
    if request.method == 'GET':
        return render(request, 'recommender/index.html', {})
    
    if request.method == 'POST':

        data = request.POST
        mn = data.get('movie_name').title()
        
        unable_to_find = False
        if mn not in all_titles:
            unable_to_find = True
        
        if unable_to_find:
            ...
        result_final = get_recommendations(mn,count_matrix,indices,df)
        res = {}
        for i in range(len(result_final)):
            res.update({
                result_final.iloc[i][0]:result_final.iloc[i][1]
            })

        return render(request, 'recommender/result.html',{'movie_details':res,'search_name':mn})
