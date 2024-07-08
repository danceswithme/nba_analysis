import pymongo

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["nba_analysis"]
tax_rate = db["tax_rate"]

# Clear existing documents in tax_rate collection
tax_rate.delete_many({})

# Define the tax rate data with the structure you mentioned
tax_data = {
    "No Tax": {
        "states": ["FL", "NV", "SD", "TX", "WA", "WY", "ON"],
        "years": list(range(1948, 2025))
    },
    "Low": {
        "states": ["AZ", "CO", "IN", "PA", "UT", "IL", "OH", "GA"],
        "years": list(range(1948, 2025))
    },
    "Moderate": {
        "states": ["IL", "MI", "NC", "VA", "WI", "LA", "MA", "GA", "DC", "OH", "OK", "MD", "KY"],
        "years": list(range(1948, 2025))
    },
    "High": {
        "states": ["CA", "NY", "NJ", "TN", "OR", "MN"],
        "years": list(range(1948, 2025))
    },
    "Specific": {
        "LA": {1976: "Moderate", 1977: "Moderate", 2018: "High", 2019: "High", 2020: "High"},
        "MA": {2016: "Moderate", 2017: "Moderate", 1988: "Moderate", 1989: "Moderate", 2019: "Moderate", 2020: "Moderate", 2021: "Moderate", 2022: "Moderate"},
        "GA": {2016: "Moderate", 2017: "Moderate", 1970: "Low", 1971: "Low", 1992: "Moderate", 1993: "Moderate"},
        "DC": {1977: "Moderate", 1978: "Moderate"},
        "OH": {1969: "Low", 1970: "Low", 2022: "Moderate", 2023: "Moderate"},
        "OK": {2021: "Moderate", 2022: "Moderate"},
        "TN": {2014: "High", 2015: "High", 2017: "High", 2018: "High"},
        "OR": {2023: "High", 2024: "High"},
        "MD": {1967: "Moderate", 1968: "Moderate", 1947: "Moderate"},
        "KY": {1967: "Moderate", 1968: "Moderate"},
        "MN": {2018: "Moderate", 2019: "Moderate", 1967: "Moderate", 1968: "Moderate", 1948: "Moderate", 1949: "Moderate", 1969: "Moderate", 1970: "Moderate", 2000: "Moderate", 2001: "Moderate", 2002: "Moderate", 2003: "Moderate", 2007: "Moderate", 2008: "Moderate", 2015: "Moderate", 2016: "Moderate"},
        "MO": {1967: "Moderate", 1968: "Moderate"},
        "NY": {1947: "High"}
    }
}

# Insert the tax data into the tax_rate collection
for tier, data in tax_data.items():
    if tier == "Specific":
        specific_data = {}
        for state, years in data.items():
            for year, specific_tier in years.items():
                if (state, specific_tier) not in specific_data:
                    specific_data[(state, specific_tier)] = []
                specific_data[(state, specific_tier)].append(year)
        for (state, specific_tier), years in specific_data.items():
            tax_rate.insert_one({
                "state": state,
                "tier": specific_tier,
                "years": years
            })
    else:
        for state in data["states"]:
            tax_rate.insert_one({
                "state": state,
                "tier": tier,
                "years": data["years"]
            })

print("Tax rate collection created successfully.")

# Verify the data
for doc in tax_rate.find():
    print(doc)
