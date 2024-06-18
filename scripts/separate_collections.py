from pymongo import MongoClient
from tqdm import tqdm

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['nba_analysis']
player_movements = db['player_movements']
temperature_data = db['temperature_data']
cost_of_living_data = db['cost_of_living_data']
state_tax_data = db['state_tax_data']

def process_player_movements():
    players = list(player_movements.find())
    
    for player in tqdm(players, desc="Processing players"):
        player_id = player['_id']
        for city, latitude, longitude, year_1, year_2 in [
            (player['former_city'], player['prev_city_latitude'], player['prev_city_longitude'], player['year_1'], player['year_2']),
            (player['new_city'], player['new_city_latitude'], player['new_city_longitude'], player['year_1'], player['year_2'])
        ]:
            if city:
                # Populate temperature data
                temp_data = {
                    "player_id": player_id,
                    "city": city,
                    "year_1": year_1,
                    "year_1_avg_temperature": None,  # Placeholder for actual temperature
                    "year_2": year_2,
                    "year_2_avg_temperature": None   # Placeholder for actual temperature
                }
                temperature_data.insert_one(temp_data)
                
                # Populate cost of living data
                cost_data = {
                    "player_id": player_id,
                    "city": city,
                    "year_1": year_1,
                    "year_1_cost_of_living": None,  # Placeholder for actual cost of living
                    "year_2": year_2,
                    "year_2_cost_of_living": None   # Placeholder for actual cost of living
                }
                cost_of_living_data.insert_one(cost_data)

                # Populate state tax data
                tax_data = {
                    "player_id": player_id,
                    "city": city,
                    "year_1": year_1,
                    "year_1_state_tax": None,  # Placeholder for actual state tax
                    "year_2": year_2,
                    "year_2_state_tax": None   # Placeholder for actual state tax
                }
                state_tax_data.insert_one(tax_data)

if __name__ == "__main__":
    process_player_movements()
    client.close()
