import requests
import pandas as pd
import csv
from datetime import date
from config import Config


config = Config()

class ApiLoader:
    def __init__(self):
        self.api_key = config.tmdb_api_key
        self.api_url = config.tmdb_api_url
        self.genre_ids_filename = config.genre_ids_filename

    def load_data(self):
        # Get the data
        params = {
            'api_key': self.api_key,
            'include_adult': 'false',
            'sort_by': 'popularity.desc'
        }
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            # Select the data needed
            movies = data['results']
            movie_data = []
            for movie in movies:
                movie_data.append({
                    'id': movie['id'],
                    'title': movie['title'],
                    'release_date': movie['release_date'],
                    'genres': movie['genre_ids']
                })
            df = pd.DataFrame(movie_data)
            # Clean and validate the data
            df_cleaned = self.clean_data(df)
            return df_cleaned

    def clean_data(self, df):
        # Clean the missing values
        df = df.dropna()
        # Converte 'release_date' to date formate
        df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d').dt.date
        # Delete extra spaces in strings
        df['title'] = df['title'].str.strip()
        # Load genre_ids values 
        genre_ids = self.load_genre_ids()
        df['genres'] = df['genres'].apply(lambda ids: self.get_genre_names(genre_ids, ids))
        return df
    
    def load_genre_ids(self):
        genre_ids = {}
        with open(self.genre_ids_filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            for row in reader:
                id, genre_name, genre_value = row
                genre_ids[int(genre_value)] = genre_name
        return genre_ids
    
    def get_genre_names(self, genre_ids, genre_ids_list):
        genre_names = [genre_ids.get(g_id, 'Unknown') for g_id in genre_ids_list]
        return ','.join(genre_names)

    def validate_data(self, df):
        for index, row in df.iterrows():
            # Check if the required keys exist
            if 'title' not in row or 'release_date' not in row or 'genres' not in row:
                return False
            # Validate the type and the length of each field
            if not isinstance(row['title'], str) or not isinstance(row['genres'], str):
                return False
            if len(row['title']) > 255 or len(row['genres']) > 255:
                return False
            # Check the format of release_date
            if not isinstance(row['release_date'], date):
                return False
        return True