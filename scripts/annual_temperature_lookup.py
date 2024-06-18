import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry
from pymongo import MongoClient
import time
from tqdm import tqdm
from openmeteo_sdk.Variable import Variable

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
om = openmeteo_requests.Client(session=retry_session)

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
    headers = {'User-Agent': 'YourAppName/1.0'}  # Add a User-Agent header
    response = requests.get(url, headers=headers)
    
    # Handle HTTP errors and rate limiting
    try:
        response.raise_for_status()  # Raise HTTPError for bad responses
        if response.text.strip():
            data = response.json()
            if data:
                latitude = float(data[0]['lat'])
                longitude = float(data[0]['lon'])
                return latitude, longitude
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

def get_average_temperature(lat, lon, start_date, end_date):
    """
    Get the average temperature for a given location and date range using the Open-Meteo API.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_mean"]
    }
    responses = om.weather_api("https://archive-api.open-meteo.com/v1/archive", params=params)
    
    try:
        response = responses[0]
        daily = response.Daily()
        temperatures = daily.Variables(0).ValuesAsNumpy()
        if temperatures.size > 0:
            return temperatures.mean()  # Calculate the average temperature
        return None
    except IndexError:
        print("No response data found")
        return None
    except Exception as e:
        print(f"Error processing weather data: {e}")
        return None

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['nba_analysis']
collection = db['player_movements']

# Fetch all players from MongoDB
players = list(collection.find())

# Iterate through the players and get coordinates and temperatures for each city
for player in tqdm(players, total=len(players), desc="Processing players"):
    prev_city = player.get('Former City')
    new_city = player.get('New City')
    
    if prev_city:
        prev_lat, prev_lon = get_coordinates(prev_city)
        player['prev_city_latitude'] = prev_lat
        player['prev_city_longitude'] = prev_lon
    
    if new_city:
        new_lat, new_lon = get_coordinates(new_city)
        player['new_city_latitude'] = new_lat
        player['new_city_longitude'] = new_lon
    
    if prev_lat and prev_lon:
        player['year1_avg_temp'] = get_average_temperature(prev_lat, prev_lon, f"{player['Year 1']}-01-01", f"{player['Year 1']}-12-31")
        player['year2_avg_temp'] = get_average_temperature(prev_lat, prev_lon, f"{player['Year 2']}-01-01", f"{player['Year 2']}-12-31")
    
    # Update the MongoDB document
    collection.update_one({'_id': player['_id']}, {'$set': player})
    
    time.sleep(1)  # Rate limit: sleep for 1 second between API calls

print("Data processing complete. MongoDB collection 'player_movements' updated.")
