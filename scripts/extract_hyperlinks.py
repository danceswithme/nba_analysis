import openpyxl
import csv

def extract_hyperlinks_from_excel(excel_file, sheet_name):
    workbook = openpyxl.load_workbook(excel_file, data_only=True)
    sheet = workbook[sheet_name]
    
    hyperlinks = []
    seen_players = set()  # Set to track players already processed
    
    for row in sheet.iter_rows(min_row=2, max_col=1, values_only=False):
        cell = row[0]
        if cell.hyperlink:
            player_name = cell.value
            
            # Check if player_name has already been seen
            if player_name in seen_players:
                continue
            
            # If not seen, add to seen_players and extract hyperlink
            seen_players.add(player_name)
            hyperlink = cell.hyperlink.target
            hyperlinks.append({'Name': player_name, 'Basketball-Reference URL': hyperlink})
    
    return hyperlinks

# Paths to the Excel file and sheet name
excel_file = 'C:/Users/Jeremy/nba_analysis/data/Players_that_fit_Query.xlsx'
sheet_name = 'Final List'

# Extract hyperlinks from the Excel file
hyperlinks = extract_hyperlinks_from_excel(excel_file, sheet_name)

# Path to the CSV output file
csv_file = 'C:/Users/Jeremy/nba_analysis/data/extracted_hyperlinks.csv'

# Write hyperlinks to a CSV file
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Name', 'Basketball-Reference URL']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(hyperlinks)

print(f"Extracted hyperlinks saved to: {csv_file}")
