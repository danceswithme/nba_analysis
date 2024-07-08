import pymongo

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["nba_analysis"]
player_movements = db["player_movements"]
tax_rate = db["tax_rate"]


# Function to get tax tier for a given state and year
def get_tax_tier(state, year):
    result = tax_rate.find_one({"state": state, "years": year})
    if result:
        return result["tier"]
    else:
        print(f"No tax tier found for state {state} and year {year}")
        return None

# Update player_movements collection
for player in player_movements.find():
    new_state = player.get("new_city_state")
    prev_state = player.get("prev_city_state")
    year1 = player.get("Year 1")
    year2 = player.get("Year 2")

    if new_state and prev_state and year1 and year2:
        new_state_tier_year1 = get_tax_tier(new_state, year1)
        new_state_tier_year2 = get_tax_tier(new_state, year2)
        prev_state_tier_year1 = get_tax_tier(prev_state, year1)
        prev_state_tier_year2 = get_tax_tier(prev_state, year2)

        update_fields = {
            "new_state_tier_year1": new_state_tier_year1,
            "new_state_tier_year2": new_state_tier_year2,
            "prev_state_tier_year1": prev_state_tier_year1,
            "prev_state_tier_year2": prev_state_tier_year2,
        }

        print(f"Updating document ID: {player['_id']} with data: {update_fields}")
        player_movements.update_one({"_id": player["_id"]}, {"$set": update_fields})

print("Player movements collection updated successfully.")

print("Player movements collection updated successfully.")


