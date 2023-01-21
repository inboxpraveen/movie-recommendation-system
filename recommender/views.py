from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from .utils import *

df = pd.read_csv('static/data.csv')
count_matrix = CountVectorizer(stop_words='english').fit_transform(df['soup'])
df = df.reset_index()
all_titles = [df['title'][i] for i in range(len(df['title']))]
indices = pd.Series(df.index, index=df['title'])


def main(request):
 
    if request.method == 'GET':
        return render(request, 'recommender/index.html', {})
    
    if request.method == 'POST':
        print("inside post method")
        data = request.POST
        mn = data.get('movie_name').title()
        
        if mn not in all_titles:
            return render(request, 'recommender/negative.html', {'movie_name': mn})
        
        result_final = get_recommendations(mn,count_matrix,indices,df)
        res = {}
        for i in range(len(result_final)):
            res.update({
                result_final.iloc[i][0]:result_final.iloc[i][1]
            })

        return render(request, 'recommender/positive.html',{'movie_details':res,'search_name':mn})
