import pymongo

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["nba_analysis"]

# Original player_movements collection
player_movements = db["player_movements"]

# New collections
player_movements_tax = db["player_movements_tax"]
player_movements_temp = db["player_movements_temp"]
player_movements_pci = db["player_movements_pci"]

# Clear existing documents in new collections
player_movements_tax.delete_many({})
player_movements_temp.delete_many({})
player_movements_pci.delete_many({})

# Function to get tax tier for a given state and year
def get_tax_tier(state, year):
    result = db["tax_rate"].find_one({"state": state, "years": year})
    if result:
        return result["tier"]
    else:
        print(f"No tax tier found for state {state} and year {year}")
        return None

# Separate the data into different collections
for player in player_movements.find():
    player_id = player["_id"]
    
    # Tax Data
    new_state = player.get("new_city_state")
    prev_state = player.get("prev_city_state")
    year1 = player.get("Year 1")
    year2 = player.get("Year 2")

    if new_state and prev_state and year1 and year2:
        new_state_tier_year1 = get_tax_tier(new_state, year1)
        new_state_tier_year2 = get_tax_tier(new_state, year2)
        prev_state_tier_year1 = get_tax_tier(prev_state, year1)
        prev_state_tier_year2 = get_tax_tier(prev_state, year2)

        tax_data = {
            "_id": player_id,
            "new_state_tier_year1": new_state_tier_year1,
            "new_state_tier_year2": new_state_tier_year2,
            "prev_state_tier_year1": prev_state_tier_year1,
            "prev_state_tier_year2": prev_state_tier_year2,
        }
        player_movements_tax.insert_one(tax_data)

    # Temperature Data
    temp_data = {
        "_id": player_id,
        "prev_city_year1_avg_temp": player.get("prev_city_year1_avg_temp"),
        "prev_city_year2_avg_temp": player.get("prev_city_year2_avg_temp"),
        "new_city_year1_avg_temp": player.get("new_city_year1_avg_temp"),
        "new_city_year2_avg_temp": player.get("new_city_year2_avg_temp")
    }
    player_movements_temp.insert_one(temp_data)

    # PCI Data
    pci_data = {
        "_id": player_id,
        "new_city_pci_year1": player.get("new_city_pci_year1"),
        "new_city_pci_year2": player.get("new_city_pci_year2"),
        "prev_city_pci_year1": player.get("prev_city_pci_year1"),
        "prev_city_pci_year2": player.get("prev_city_pci_year2")
    }
    player_movements_pci.insert_one(pci_data)

print("Separate collections created successfully.")
