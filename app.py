import pandas as pd
import ast
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Streamlit Config

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# Reading data

@st.cache_data
def load_data():
    movies=pd.read_csv("tmdb_5000_movies.csv")
    credits=pd.read_csv("tmdb_5000_credits.csv")
    details=pd.read_csv("movie_details.csv")
    movies=movies.merge(credits, on="title")
    movies=movies[
        [
            "id",
            "title",
            "genres",
            "keywords",
            "overview",
            "tagline"
        ]
    ]
    movies=movies.merge(
        details,
        on="id",
        how="left"
    )
    movies["overview"]=movies["overview"].fillna("")
    movies["tagline"]=movies["tagline"].fillna("")
    movies["genres"]=movies["genres"].fillna("[]")
    movies["keywords"]=movies["keywords"].fillna("[]")
    return movies

movies=load_data()

# Extracting genres

def extract_names(text):
    names=[]
    try:
        for item in ast.literal_eval(text):
            names.append(item["name"])
    except:
        pass
    return " ".join(names)

movies["genres"]=movies["genres"].apply(extract_names)
movies["keywords"]=movies["keywords"].apply(extract_names)

# Data Featuring

movies["tags"]=(
    movies["genres"]+" "+
    movies["keywords"]+" "+
    movies["overview"]+" "+
    movies["tagline"]
)
movies["tags"]=movies["tags"].str.lower()

# TF-IDF Vectorizer

@st.cache_resource
def create_similarity_matrix(tags):
    tfidf=TfidfVectorizer(stop_words="english")
    vectors=tfidf.fit_transform(tags)
    similarity=cosine_similarity(vectors)
    return similarity

similarity=create_similarity_matrix(movies["tags"])

# Movie Recommendation Function

def recommend(movie_name):
    movie_name=movie_name.lower()
    matching_movies=movies[
        movies["title"].str.lower()==movie_name
    ]
    if matching_movies.empty:
        return None, []
    movie_index=matching_movies.index[0]
    selected_movie_id=(
        movies.iloc[movie_index]["id"]
    )
    distances=similarity[movie_index]

    movie_list=sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations=[]

    for movie in movie_list:
        index=movie[0]
        recommendations.append(
            {
                "title": movies.iloc[index]["title"],
                "id": movies.iloc[index]["id"]
            }
        )
    return selected_movie_id, recommendations

# Streamlit GUI

st.title("🎬 Movie Recommendation System")
st.write(
    "Get movie recommendations based on genres, keywords, overview, and tagline"
)
movie_name=st.text_input(
    "Enter your favourite Movie"
)
if st.button("Recommend"):
    if movie_name.strip()=="":
        st.warning(
            "Please enter a movie name"
        )
    else:
        selected_movie_id,recommendations=recommend(
            movie_name
        )
        if selected_movie_id is None:
            st.error(
                "Check the spelling...If correct then the Movie is not found in dataset."
            )
        else:
            # Selecte Movie details
            st.markdown("---")
            st.subheader("🎬 Selected Movie")
            selected_movie=movies[
                movies["id"]==selected_movie_id
            ].iloc[0]

            poster=selected_movie["poster_url"]
            rating=selected_movie["rating"]
            year=selected_movie["year"]

            col1,col2=st.columns([1, 2])

            with col1:
                if pd.notna(poster) and poster != "":
                    st.image(
                        poster,
                        width="stretch"
                    )
                else:
                    st.image(
                        "https://via.placeholder.com/500x750?text=No+Poster",
                        width="stretch"
                    )

            with col2:
                st.markdown(
                    f"### {movie_name.title()}"
                )
                st.markdown(
                    f"⭐ Rating: **{rating}**"
                )
                st.markdown(
                    f"📅 Release Year: **{year}**"
                )
            # Recommended movie details

            st.markdown("---")
            st.subheader(
                "🎯 Recommended Movies"
            )
            cols = st.columns(5)

            for idx, movie in enumerate(
                recommendations
            ):

                movie_data = movies[
                     movies["id"]==movie["id"]
                ].iloc[0]
                poster=movie_data["poster_url"]
                rating=movie_data["rating"]
                year=movie_data["year"]

                with cols[idx]:

                    if pd.notna(poster) and poster != "":
                         st.image(
                              poster,
                              width="stretch"
                            )
                    else:
                        st.image(
                            "https://via.placeholder.com/500x750?text=No+Poster",
                            width="stretch"
                            )
                    st.markdown(
                        f"**{movie['title']}**"
                    )
                    st.markdown(
                        f"⭐ {rating}"
                    )
                    st.markdown(
                        f"📅 {year}"
                    )