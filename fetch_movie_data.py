import pandas as pd
import requests
import time

# ==========================================
# TMDB TOKEN
# ==========================================

TMDB_BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMTZlODM5ZWE5ZjZkMTllMDZkY2ZjNTlhZTM5OWU4NiIsIm5iZiI6MTc4MTg1MDA2NC42ODIsInN1YiI6IjZhMzRkZmQwNTBmODNiZDk3ZDRiYWFjNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.hdOAYMdivbLl2xrCxGnN-XvtEwtA4MzgMzKF73KQB_M"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_BEARER_TOKEN}"
}

session = requests.Session()

# ==========================================
# LOAD MOVIES
# ==========================================

movies = pd.read_csv("tmdb_5000_movies.csv")

# ==========================================
# FETCH DETAILS
# ==========================================

movie_details = []

for index, row in movies.iterrows():

    movie_id = int(row["id"])

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    try:

        response = session.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        poster_url = (
            f"https://image.tmdb.org/t/p/w500{poster_path}"
            if poster_path
            else None
        )

        rating = data.get("vote_average")

        release_date = data.get("release_date", "")

        year = (
            release_date[:4]
            if release_date
            else None
        )

        movie_details.append({
            "id": movie_id,
            "poster_url": poster_url,
            "rating": rating,
            "year": year
        })

        print(
            f"{index+1}/{len(movies)} : "
            f"{row['title']}"
        )

    except Exception as e:

        print(
            f"FAILED -> {row['title']} : {e}"
        )

        movie_details.append({
            "id": movie_id,
            "poster_url": None,
            "rating": None,
            "year": None
        })

    # avoid rate limits
    time.sleep(0.1)

# ==========================================
# SAVE CSV
# ==========================================

details_df = pd.DataFrame(movie_details)

details_df.to_csv(
    "movie_details.csv",
    index=False
)

print("\nmovie_details.csv created successfully!")