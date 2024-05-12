import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(layout="wide")


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c41af3823c9e59a61777f9f18239b624&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movie_list[movie_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movie_list.iloc[i[0]].movie_id
        recommended_movies.append(movie_list.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters


movie_list = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_titles = movie_list['title'].values

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select Movie',(movie_titles))

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    num_recommendations = min(len(names), 5)  # Ensure we have at most 5 recommendations
    cols = st.columns(num_recommendations)

    for i in range(num_recommendations):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

