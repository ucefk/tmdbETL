import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template
from config import Config

config = Config()

class DataAnalysis:
    def __init__(self):
        self.conn = None        
        self.db_host = config.db_host
        self.db_port = config.db_port
        self.db_name = config.db_name
        self.db_user = config.db_user
        self.db_password = config.db_password

    def connect_to_database(self):
        try:
            self.conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            print("Connected to the database successfully.")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

    def fetch_data_from_tables(self):
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM tmdb JOIN movies_csv ON tmdb.title = movies_csv.title;"
            cursor.execute(query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(data, columns=columns)
            return df
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from tables:", error)

    def perform_data_analysis(self):
        self.connect_to_database()
        df = self.fetch_data_from_tables()

        total_movies = df.shape[0]
        
        genre_counts = df['genres'].value_counts(normalize=True) * 100
        plt.bar(genre_counts.index, genre_counts.values)
        plt.xlabel('Genres')
        plt.ylabel('Percentage')
        plt.title('Number of Movies by Genre')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/images/genre_chart.png')
        plt.clf()
        
        df['release_year'] = pd.to_datetime(df['release_date']).dt.year
        year_counts = df['release_year'].value_counts().sort_index()
        plt.bar(year_counts.index, year_counts.values)
        plt.xlabel('Year')
        plt.ylabel('Count')
        plt.title('Number of Movies by Year')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/year_chart.png')
        plt.clf()
        
        print("Data analysis completed successfully.")

    def run_flask_server(self):
        app = Flask(__name__)

        @app.route('/')
        def index():
            return render_template('index.html')

        app.run(host='0.0.0.0', port=5000)
