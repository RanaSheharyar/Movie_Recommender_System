import pickle
import streamlit as st
import requests
import gdown

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        /* Add your CSS styling here */
        body {
            font-family: Arial, sans-serif;
            background-color: red;
        }

        .st-title {
            font-size: 2.5rem;
            color: #333;
            margin-bottom: 1rem;
        }
        .st-subheader {
            font-size: 1.5rem;
            color: #555;
            margin-bottom: 1.5rem;
        }

        /* Add border to st.file_uploader */
        .css-qnt3a9 {
            border: 2px solid #fff;
            border-radius: 5px;
            padding: 10px;
        }


    .css-1l269bu {
        align-self: center;
        width: calc(16.6667% - 1rem);
        flex: 1 1 calc(16.6667% - 1rem);
        }
        /* Add more styling rules as needed */
    </style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


st.header('Movie Recommender')
m_url = 'https://drive.google.com/file/d/1-QPs8hv7SmVzrUdIrlyBVwm6dOYdNgmZ/view?usp=sharing'
s_url = 'https://drive.google.com/file/d/1YW_Lg1sQrCpFkk0O0YaqpLi4_yuGqtae/view?usp=sharing'
output = 'movie.pkl'
output2 = 'similarity.pkl'
model = gdown.download(m_url, output, quiet=False, fuzzy=True)
model2 = gdown.download(s_url, output2, quiet=False, fuzzy=True)
movies = pickle.load(open('movie.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Recommend Me!'):
    recommended_movie_names, recommended_movie_posters = recommend(
        selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
