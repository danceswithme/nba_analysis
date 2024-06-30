import os
import pandas as pd
from pymongo import MongoClient

# MongoDB connection details
client = MongoClient('mongodb://localhost:27017/')
db = client['nba_analysis']
state_pci_collection = db['state_PCI']
player_movements_collection = db['player_movements']

# Define state code to state name mapping
state_code_to_name = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "D.C.",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
    "ON": "Toronto, Ontario"
}

def get_pci(state, year):
    try:
        if state == "DC":
            state_name = "D.C."
        else:
            state_name = state_code_to_name.get(state)
        
        if not state_name:
            raise ValueError(f"State code {state} not found in mapping.")
        
        state_data = state_pci_collection.find_one({"state": state_name})
        if not state_data:
            raise ValueError(f"No PCI data found for state {state_name}.")
        
        pci = state_data.get("pci", {}).get(str(year), 0)
        return pci
    
    except Exception as e:
        print(f"Error retrieving PCI value for state {state} and year {year}: {e}")
        return 0

def update_pci_data():
    for doc in player_movements_collection.find():
        try:
            prev_city_state = doc.get('prev_city_state')
            new_city_state = doc.get('new_city_state')
            year1 = doc.get('Year 1')
            year2 = doc.get('Year 2', 0)  # Year 2 may be optional

            pci_year1_prev = get_pci(prev_city_state, year1)
            pci_year2_prev = get_pci(prev_city_state, year2) if year2 else 0
            pci_year1_new = get_pci(new_city_state, year1)
            pci_year2_new = get_pci(new_city_state, year2) if year2 else 0

            player_movements_collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {
                    "prev_city_pci_year1": pci_year1_prev,
                    "prev_city_pci_year2": pci_year2_prev,
                    "new_city_pci_year1": pci_year1_new,
                    "new_city_pci_year2": pci_year2_new
                },
                "$unset": {
                    "former_city_pci_year1": "",
                    "former_city_pci_year2": ""
                }}
            )
            print(f"Updated PCI data for document {doc['_id']}")

        except Exception as e:
            print(f"Error updating PCI data for document {doc['_id']}: {e}")

# Execute the function to update PCI data
update_pci_data()
