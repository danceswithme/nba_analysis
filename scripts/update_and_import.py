import pandas as pd
import requests
from pymongo import MongoClient
import time

def get_coordinates(city_name):
    """
    Get the latitude and longitude of a city using the OpenStreetMap Nominatim API.
    Assumes cities are in the US unless it's Toronto.
    """
    if city_name.lower() == 'toronto':
        country = 'Canada'
    else:
        country = 'USA'
        
    url = f"https://nominatim.openstreetmap.org/search?city={city_name}&country={country}&format=json"
    headers = {'User-Agent': 'YourAppName/1.0'}  # Adjust YourAppName
    response = requests.get(url, headers=headers)
    
    try:
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        
        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return latitude, longitude
        else:
            return None, None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None, None
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return None, None
    except ValueError as val_err:
        print(f"Value error occurred: {val_err}")
        return None, None

# Read the existing CSV file
csv_file = '../data/players_data.csv'  # Adjust path as necessary
df = pd.read_csv(csv_file)

# Create new columns for latitude and longitude of former and new cities
df['prev_city_latitude'] = None
df['prev_city_longitude'] = None
df['new_city_latitude'] = None
df['new_city_longitude'] = None

# Iterate through the DataFrame and get coordinates for each city
for index, row in df.iterrows():
    prev_city = row['Former City']  # Adjust column names as per your CSV
    new_city = row['New City']      # Adjust column names as per your CSV
    
    if prev_city:
        prev_lat, prev_lon = get_coordinates(prev_city)
        df.at[index, 'prev_city_latitude'] = prev_lat
        df.at[index, 'prev_city_longitude'] = prev_lon
    
    if new_city:
        new_lat, new_lon = get_coordinates(new_city)
        df.at[index, 'new_city_latitude'] = new_lat
        df.at[index, 'new_city_longitude'] = new_lon
    
    time.sleep(1)  # Rate limit: sleep for 1 second between API calls

# Save the updated DataFrame to a new CSV file
updated_csv_file = '../data/updated_players_data.csv'  # Adjust path as necessary
df.to_csv(updated_csv_file, index=False)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['nba_analysis']
collection = db['player_movements']

# Convert DataFrame to dictionary and insert into MongoDB
records = df.to_dict(orient='records')
collection.insert_many(records)

print(f"Updated CSV file saved as {updated_csv_file}")
print("Data inserted into MongoDB collection 'player_movements'")
