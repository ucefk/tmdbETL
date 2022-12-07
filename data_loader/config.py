import os


class Config:

    tmdb_api_key = ''
    tmdb_api_url = 'https://api.themoviedb.org/3/movie/popular'
    #self.tmdb_api_url = 'https://api.themoviedb.org/3/discover/movie'
    
    genre_ids_filename = 'data/genre_ids.csv'
    csv_filename = 'data/movies.csv'

    db_host = 'tmdb'
    db_port = 5432
    db_name = 'movies_db'
    db_user = 'user'
    db_password = 'password'
