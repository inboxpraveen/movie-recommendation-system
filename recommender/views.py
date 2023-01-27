from django.shortcuts import render
import pandas as pd
import pickle
import re

features = pd.read_parquet("static/features.parquet")
print("loaded par")
knn_model = pickle.load(open('static/model.pkl', 'rb'))
print("loadded model")
all_titles = set(features.index.values.tolist())

def preprocess_all_titles(one):
    output = re.sub("([0-9][0-9][0-9][0-9])","",one).replace("()","").replace(",","").replace(".","").replace("'","")
    new_output = " ".join([word.strip().title() for word in output.split()])
    return new_output.strip()

all_titles = set(features.index.map(preprocess_all_titles).values.tolist())

def first_substring(substring):
    for i, title in enumerate(all_titles):
        if substring in title or set(substring.split())==set(title.split()):
            return i
    return None

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
