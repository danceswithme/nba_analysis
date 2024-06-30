import os
import pandas as pd
from pymongo import MongoClient

# MongoDB connection details
client = MongoClient('mongodb://localhost:27017/')
db = client['nba_analysis']
state_pci_collection = db['state_PCI']

# Define file paths
csv_dir = r'C:\Users\Jeremy\nba_analysis\data'
state_csv_dir = os.path.join(csv_dir, 'state_csvs')

# List of US states and D.C.
states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
    "Connecticut", "Delaware", "D.C.", "Florida", "Georgia", "Hawaii", 
    "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", 
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", 
    "New Hampshire", "New Jersey", "New Mexico", "New York", 
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", 
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
    "West Virginia", "Wisconsin", "Wyoming"
]

def read_state_pci_csv(directory):
    for idx, file in enumerate(sorted(os.listdir(directory))):
        if file.startswith("0_") and file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            try:
                # Read the first row to get the years
                years = pd.read_csv(file_path, nrows=1).columns[1:].tolist()
                # Read the 20th row to get the PCI data
                df = pd.read_csv(file_path, skiprows=19, header=None)
                pci_values = df.iloc[0, 1:].tolist()
                
                state = states[idx]  # Get the state name based on the index
                pci_data = {year: pci for year, pci in zip(years, pci_values)}

                state_pci_collection.insert_one({
                    'state': state,
                    'pci': pci_data
                })
                print(f"Inserted data for state: {state}")

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

def read_toronto_pci(file_path):
    try:
        df = pd.read_csv(file_path, skiprows=12)
        years = df.columns[1:].tolist()
        pci_values = df.loc[df[0] == 'Average income (excluding zeros)', df.columns[1:]].values.flatten().tolist()

        pci_data = {year: pci for year, pci in zip(years, pci_values)}

        state_pci_collection.insert_one({
            'state': 'Toronto, Ontario',
            'pci': pci_data
        })
        print("Inserted data for Toronto, Ontario")

    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def insert_pci_data():
    # Clear existing documents in state_PCI collection
    state_pci_collection.delete_many({})

    # Process state CSV files for US states
    read_state_pci_csv(state_csv_dir)

    # Process Toronto PCI file
    toronto_pci_file_path = os.path.join(csv_dir, 'TORONTO_PCI.csv')
    read_toronto_pci(toronto_pci_file_path)

# Execute the function to insert PCI data
insert_pci_data()
