#from config import Config
from api_loader import ApiLoader
from csv_loader import CsvLoader
from data_loader.sql_queries import SqlQueries


api_loader = ApiLoader()
csv_loader = CsvLoader()
sql_queries = SqlQueries()

def main():
    # Loading and transformation of data from the API and CSV files
    api_data = api_loader.load_data()
    print(api_data.head())
    csv_data = csv_loader.load_data()
    print(csv_data.head())

    # Data validation
    if not api_loader.validate_data(api_data):
        print("Data validation from API is failed. Stopping the process.")
        return
    if not csv_loader.validate_data(csv_data):
        print("Data validation from CSV file is failed. Stopping the process.")
        return

    # Create tmdb and movies_csv tables in the database
    sql_queries.drop_table('tmdb')
    sql_queries.create_table('tmdb')
    sql_queries.drop_table('movies_csv')
    sql_queries.create_table('movies_csv')

    # Data insertion in the database
    sql_queries.insert_data('tmdb', api_data)
    sql_queries.insert_data('movies_csv', csv_data)

if __name__ == "__main__":
    main()
