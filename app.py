from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from tabulate import tabulate

# Create a Flask app
app = Flask(__name__)

# Read your movie data
dataset = pd.read_csv("movies.csv")
selected_features = ['genres', 'cast', 'director', 'keywords', 'tagline']
for i in selected_features:
    dataset[i] = dataset[i].fillna(' ')

# Combine features
combine_features = dataset['genres'] + ' ' + dataset['cast'] + ' ' + dataset['director'] + ' ' + dataset['keywords'] + ' ' + dataset['tagline']

# Define routes
@app.route('/')
def home():
    return "Welcome to the movie recommendation app! Enter a movie name."

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form['movie_name']

    # Your recommendation code here
    list_of_movies = list(dataset['title'])
    find_close_match = difflib.get_close_matches(movie_name, list_of_movies)

    for index, title in enumerate(dataset['title']):
        if title == find_close_match[0]:
            break

    index = index
    similarity_score = list(enumerate(similarity[index]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    i = 1
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

    return render_template('results.html', table=table)

if __name__ == '__main__':
    app.run(debug=True)
