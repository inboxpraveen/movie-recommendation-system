from django.shortcuts import render
import pandas as pd

def main(request):
    df = pd.read_csv('static/data.csv')
    if request.method == 'GET':
        print(df.head())
        return render(request, 'recommender/index.html', {})
    
    if request.method == 'POST':
        print("inside post method")
        data = request.POST
        mn = data.get('movie_name')
        if mn == 'positive':
            return render(request, 'recommender/positive.html',{'movie_name':mn})
        else:
            return render(request, 'recommender/negative.html',{'movie_name':mn})

