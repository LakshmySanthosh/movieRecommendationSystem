import streamlit as st
import pickle
import requests
import gdown

@st.cache_data
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=411d1ff8a6dcc6cf92d677d137184da2&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

@st.cache_data
def download_files():
    # Google Drive file IDs
    movies_url = 'https://drive.google.com/uc?id=15sP5W00ko4120H0wnOFsfnAegCdLLiA3'
    similarity_url = 'https://drive.google.com/uc?id=1VuXzCnE95nr2d-Qx4yvspBMP15Dk4rMl'

    # Download files
    gdown.download(movies_url, 'movies.pkl', quiet=False)
    gdown.download(similarity_url, 'similarity.pkl', quiet=False)

@st.cache_data
def load_data():
    with open('movies.pkl', 'rb') as f:
        movies = pickle.load(f)
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
    return movies, similarity

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

def main():
    st.title('Movie Recommendation System')

    # Download files if they are not already downloaded
    download_files()

    # Load the data
    global movies, similarity
    movies, similarity = load_data()
    movies_list = movies['title'].values

    selected_movie = st.selectbox('Enter the movie', movies_list)

    if st.button('Show similar movies'):
        names, posters = recommend(selected_movie)
        mov1, mov2, mov3, mov4, mov5 = st.columns(5)

        with mov1:
            st.image(posters[0])
            st.markdown('<h3 style="font-size: 14px;">{}</h3>'.format(names[0]), unsafe_allow_html=True)

        with mov2:
            st.image(posters[1])
            st.markdown('<h3 style="font-size: 14px;">{}</h3>'.format(names[1]), unsafe_allow_html=True)

        with mov3:
            st.image(posters[2])
            st.markdown('<h3 style="font-size: 14px;">{}</h3>'.format(names[2]), unsafe_allow_html=True)

        with mov4:
            st.image(posters[3])
            st.markdown('<h3 style="font-size: 14px;">{}</h3>'.format(names[3]), unsafe_allow_html=True)

        with mov5:
            st.image(posters[4])
            st.markdown('<h3 style="font-size: 14px;">{}</h3>'.format(names[4]), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
