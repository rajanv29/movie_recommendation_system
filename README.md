# 🎬 Movie Recommendation System

## 🚀 Live Demo
Try the application here: https://movie-recommendation-system-ur29.streamlit.app/

A content-based Movie Recommendation System built using Python, Scikit-Learn, and Streamlit.
The application recommends **5 similar movies** based on the selected movie and displays their posters for a better user experience.

## Features

* Recommend 5 similar movies which you may prefer watching
* Display movie posters alongside recommendations
* Interactive Streamlit web interface
* Content-based filtering using movie metadata
* Preprocessed dataset for faster recommendations

## Dataset

The project uses:

* `tmdb_5000_movies.csv`
* `tmdb_5000_credits.csv`

Movie information and poster url is processed and stored in `movie_details.csv`.

## Poster Integration

Movie posters are fetched using TMDB data through the `fetch_movie_data.py` script.

The script generates a dataset containing poster URLs, which are then used by the Streamlit application to display movie posters along with recommendations.

## Technologies Used

* Python
* Pandas
* Scikit-Learn
* Streamlit
* TMDB API
* TMDB Movie Datasets

## Run Locally

1. Clone the repository
```bash
git clone https://github.com/rajanv29/movie_recommendation_system.git
```
2. Navigate to the project directory
```bash
cd movie_recommendation_system
```
3. Install the required dependencies
```bash
pip install -r requirements.txt
```
4. Run the Streamlit application
```bash
streamlit run app.py
```
5. Open in your browser
   Streamlit will automatically open the application. If not, visit:
```text
http://localhost:8501
```

## Author

Rajarajan V
If you found this project useful, feel free to star the repository and connect with me on LinkedIn.
