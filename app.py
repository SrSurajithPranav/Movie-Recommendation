import numpy as np
import pandas as pd
from matplotlib import pyplot as plot
from tabulate import tabulate
dataset=pd.read_csv("movies.csv")
selected_features=['genres','cast','director','keywords','tagline']
for i in selected_features:
    dataset[i]=dataset[i].fillna(' ')
combine_features=dataset['genres']+' '+dataset['cast']+' '+dataset['director']+' '+dataset['keywords']+' '+dataset['tagline']
from sklearn.feature_extraction.text import TfidfVectorizer
feature_extraction=TfidfVectorizer()
feature_vector=feature_extraction.fit_transform(combine_features)
from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(feature_vector)
import difflib
movie_name=input("Enter the movie name:")
list_of_movies=list(dataset['title'])
find_close_match=difflib.get_close_matches(movie_name,list_of_movies)
for index,title in enumerate(dataset['title']):
    if(title==find_close_match[0]):
        break
index=index
similarity_score=list(enumerate(similarity[index]))
sorted_similar_movies=sorted(similarity_score,key=lambda x:x[1],reverse=True)
i=1
movie_data = []
for i, movie in enumerate(sorted_similar_movies):
    index = movie[0]
    title_index = dataset.loc[index, 'title']
    vote_average = dataset.loc[index, 'vote_average']
    director = dataset.loc[index, 'director']
    cast = dataset.loc[index, 'cast']
    budget = dataset.loc[index, 'budget']

    if i < 30:
        movie_data.append([i, title_index, budget, director, vote_average, cast])

headers = ["#", "Title", "Budget", "Director", "Rating", "Cast"]
table = tabulate(movie_data, headers, tablefmt="grid")

print("The suggested movies are:")
print(table)
