import pandas as pd
from pymongo import MongoClient

def save_csv_to_mongodb(csv_file_path, db_name, collection_name, mongo_uri='mongodb://localhost:27017/'):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Convert DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')
    
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    
    # Insert data into MongoDB
    collection.insert_many(data)
    print(f'Data successfully inserted into {db_name}.{collection_name}')

if __name__ == "__main__":
    # Define file path and MongoDB details
    csv_file_path = r'C:\Users\Jeremy\nba_analysis\data\Players that fit Query.csv'
    db_name = 'nba_analysis'
    collection_name = 'players'
    
    # Call the function to save CSV to MongoDB
    save_csv_to_mongodb(csv_file_path, db_name, collection_name)
