import os
import pandas as pd
from pymongo import MongoClient

# MongoDB connection details
client = MongoClient('mongodb://localhost:27017/')
db = client['nba_analysis']
state_pci_collection = db['state_PCI']

# Define file path for the Toronto PCI data
csv_dir = r'C:\Users\Jeremy\nba_analysis\data'
toronto_pci_file_path = os.path.join(csv_dir, 'TORONTO_PCI.csv')

def read_toronto_pci(file_path):
    try:
        # Read the first row to get the years
        df = pd.read_csv(file_path, skiprows=12, header=None)
        years = df.iloc[0, 1:].tolist()

        # Read the 19th row to get the PCI data
        pci_values = df.iloc[6, 1:].tolist()

        pci_data = {year: pci for year, pci in zip(years, pci_values)}

        state_pci_collection.insert_one({
            'state': 'Toronto, Ontario',
            'pci': pci_data
        })
        print("Inserted data for Toronto, Ontario")

    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def insert_toronto_pci():
    # Clear existing document for Toronto, Ontario in state_PCI collection
    state_pci_collection.delete_many({'state': 'Toronto, Ontario'})

    # Process Toronto PCI file
    read_toronto_pci(toronto_pci_file_path)

# Execute the function to insert Toronto PCI data
insert_toronto_pci()
