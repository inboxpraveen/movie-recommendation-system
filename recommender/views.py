from django.shortcuts import render
import pandas as pd

def index(request):
    df = pd.read_csv('static/data.csv')
    if request.method == 'GET':
        print(df.head())
        return render(request, 'recommender/index.html', {})
    
    if request.method == 'POST':
        print("inside post method")
        return render(request, 'recommender/positive.html')

