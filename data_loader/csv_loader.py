import pandas as pd
from datetime import date
from config import Config


config = Config()

class CsvLoader:
    def __init__(self):
        self.csv_filename = config.csv_filename

    def load_data(self):
        # CSV reading
        df = pd.read_csv(self.csv_filename)
        # transform and validate the data
        df_cleaned = self.clean_data(df)
        return df_cleaned

    def clean_data(self, df):
        # Clean the missing values
        df = df.dropna()
        # Converte 'release_date' to date formate
        df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d').dt.date
        # Delete extra spaces in strings
        df['title'] = df['title'].str.strip()
        df['genres'] = df['genres'].str.strip()
        # Delete 'runtime'
        df = df.drop(['runtime'], axis=1)
        return df

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
