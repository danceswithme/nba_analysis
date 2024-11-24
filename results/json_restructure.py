import json

# Input and output file paths
input_file = "player_movements.json"  # Replace with your raw JSON file name
output_file = "player_movements_cleaned.json"  # Output file name

# Helper function to clean numeric fields
def clean_numeric(value):
    if isinstance(value, str):
        return float(value.replace(",", ""))
    return float(value)

# Function to reformat a single record
def reformat_record(record):
    return {
        "Name": record["Name"],
        "Former City": record["Former City"],
        "New City": record["New City"],
        "Year 1": record["Year 1"],
        "Year 2": record["Year 2"],
        "Prev City Latitude": record["prev_city_latitude"],
        "Prev City Longitude": record["prev_city_longitude"],
        "New City Latitude": record["new_city_latitude"],
        "New City Longitude": record["new_city_longitude"],
        "Prev City Year 1 Avg Temp": record["prev_city_year1_avg_temp"],
        "Prev City Year 2 Avg Temp": record["prev_city_year2_avg_temp"],
        "New City Year 1 Avg Temp": record["new_city_year1_avg_temp"],
        "New City Year 2 Avg Temp": record["new_city_year2_avg_temp"],
        "New City State": record["new_city_state"],
        "Prev City State": record["prev_city_state"],
        "New City PCI Year 1": clean_numeric(record["new_city_pci_year1"]),
        "New City PCI Year 2": clean_numeric(record["new_city_pci_year2"]),
        "Prev City PCI Year 1": clean_numeric(record["prev_city_pci_year1"]),
        "Prev City PCI Year 2": clean_numeric(record["prev_city_pci_year2"]),
        "New State Tier Year 1": record["new_state_tier_year1"],
        "New State Tier Year 2": record["new_state_tier_year2"],
        "Prev State Tier Year 1": record["prev_state_tier_year1"],
        "Prev State Tier Year 2": record["prev_state_tier_year2"],
    }

# Read raw JSON data
with open(input_file, "r") as infile:
    raw_data = [json.loads(line) for line in infile]

# Process and reformat each record
cleaned_data = [reformat_record(record) for record in raw_data]

# Write cleaned data to the output file
with open(output_file, "w") as outfile:
    json.dump(cleaned_data, outfile, indent=4)

print(f"Cleaned data written to {output_file}")