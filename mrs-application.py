import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=1ac83753d0e16d7830e89c76ea9f7a90&language=en-US'.format(movie_id)) #random-api-key
    data = response.json()
    print(data)  # Print the response to inspect its structure
    poster_path = data.get('poster_path')  # Use .get() method to avoid KeyError
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id  # Using DataFrame index as movie ID
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        poster = fetch_poster(movie_id)
        recommended_movies_posters.append(poster)

    return recommended_movies, recommended_movies_posters

movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "select movie",
    movies['title'].values)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.subheader(recommendations[0])
        if posters[0]:
            st.image(posters[0])

    with col2:
        st.subheader(recommendations[1])
        if posters[1]:
            st.image(posters[1])

    with col3:
        st.subheader(recommendations[2])
        if posters[2]:
            st.image(posters[2])

    with col4:
        st.subheader(recommendations[3])
        if posters[3]:
            st.image(posters[3])

    with col5:
        st.subheader(recommendations[4])
        if posters[4]:
            st.image(posters[4])
