import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=475cd503f2e7c81659655de2a1e23ad9&language=en-US')
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"

def fetch_overview(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=475cd503f2e7c81659655de2a1e23ad9&language=en-US')
    data = response.json()
    return data['overview']

def recommend(movie, num_recommendations):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:num_recommendations+1]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_overviews = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_overviews.append(fetch_overview(movie_id))
    return recommended_movies, recommended_movies_posters, recommended_movies_overviews

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("🎬 MOVIE RECOMM SYSTEM 🍿")

st.markdown(
    """
    <style>
    .title {
        font-size: 24px;
        font-weight: bold;
        color: #ff6347;
    }
    .dropdown {
        font-size: 16px;
        color: #4682b4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">✨ Discover Your Next Favorite Movie! 🎬</div>', unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    'Ready to Discover Your Next Favorite Film? Choose a Movie and Let the Magic Begin! 🍿',
    movies['title'].values,
    format_func=lambda x: f"🎥 {x}"
)

num_recommendations = st.slider(
    'How many recommendations would you like? 🎯',
    min_value=1,
    max_value=10,
    value=5
)

if st.button('Get Recommendations! 🎉'):
    with st.spinner('Fetching recommendations...'):
        names, posters, overviews = recommend(selected_movie_name, num_recommendations)

        cols = st.columns(num_recommendations)
        for i, col in enumerate(cols):
            with col:
                st.image(posters[i], use_column_width=True)
                st.text(names[i])
                st.write(overviews[i])
