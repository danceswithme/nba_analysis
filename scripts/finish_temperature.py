import requests_cache
import pandas as pd
from retry_requests import retry
from pymongo import MongoClient
from tqdm import tqdm
import requests
from datetime import datetime

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['nba_analysis']
collection = db['player_movements']

def get_temperature(latitude, longitude, start_date, end_date):
    """
    Get the average temperature for a given latitude, longitude, and date range.
    """
    try:
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "temperature_2m_mean"
        }
        response = retry_session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        temperatures = data.get('daily', {}).get('temperature_2m_mean', [])
        valid_temperatures = [temp for temp in temperatures if temp is not None]
        if valid_temperatures:
            avg_temperature = sum(valid_temperatures) / len(valid_temperatures)
            return avg_temperature
        else:
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return None

def is_valid_year(year):
    """
    Check if the year is valid (not in the future).
    """
    current_year = pd.Timestamp.now().year
    return 1900 <= year <= current_year

def get_end_date(year):
    """
    Get the end date for the given year, adjusted if it's the current year or the previous year.
    """
    current_date = datetime.now()
    if year == current_date.year or year == current_date.year - 1:
        return current_date.strftime('%Y-%m-%d')
    else:
        return f"{year}-12-31"

def main():
    # Process each document in the MongoDB collection
    players = list(collection.find())

    for player in tqdm(players, desc="Processing players"):
        update_needed = False
        unset_fields = {}

        # Remove incorrect temperature fields if they exist
        if 'year1_avg_temp' in player:
            unset_fields['year1_avg_temp'] = ""
        if 'year2_avg_temp' in player:
            unset_fields['year2_avg_temp'] = ""

        # Check and update former city temperature for year 1 and year 2 if necessary
        if player.get("prev_city_latitude") and player.get("prev_city_longitude"):
            if player.get("prev_city_year1_avg_temp") is None and is_valid_year(player['Year 1']):
                end_date = get_end_date(player['Year 1'])
                temp = get_temperature(player["prev_city_latitude"], player["prev_city_longitude"], f"{player['Year 1']}-01-01", end_date)
                if temp is not None:
                    player["prev_city_year1_avg_temp"] = temp
                    update_needed = True

            if player.get("prev_city_year2_avg_temp") is None and is_valid_year(player['Year 2']):
                end_date = get_end_date(player['Year 2'])
                temp = get_temperature(player["prev_city_latitude"], player["prev_city_longitude"], f"{player['Year 2']}-01-01", end_date)
                if temp is not None:
                    player["prev_city_year2_avg_temp"] = temp
                    update_needed = True

        # Check and update new city temperature for year 1 and year 2 if necessary
        if player.get("new_city_latitude") and player.get("new_city_longitude"):
            if player.get("new_city_year1_avg_temp") is None and is_valid_year(player['Year 1']):
                end_date = get_end_date(player['Year 1'])
                temp = get_temperature(player["new_city_latitude"], player["new_city_longitude"], f"{player['Year 1']}-01-01", end_date)
                if temp is not None:
                    player["new_city_year1_avg_temp"] = temp
                    update_needed = True

            if player.get("new_city_year2_avg_temp") is None and is_valid_year(player['Year 2']):
                end_date = get_end_date(player['Year 2'])
                temp = get_temperature(player["new_city_latitude"], player["new_city_longitude"], f"{player['Year 2']}-01-01", end_date)
                if temp is not None:
                    player["new_city_year2_avg_temp"] = temp
                    update_needed = True

        if update_needed or unset_fields:
            update_query = {}
            if update_needed:
                update_query["$set"] = player
            if unset_fields:
                update_query["$unset"] = unset_fields
            collection.update_one({"_id": player["_id"]}, update_query)

if __name__ == "__main__":
    main()
    client.close()
