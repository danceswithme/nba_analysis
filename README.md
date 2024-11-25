# NBA Data Analysis

Conducted a comprehensive analysis of NBA player movements, examining tax rates, per capita income, and average temperature, including frequency, trend, and regression analyses, comparisons between bins of years, and identifying the most common destinations.

## Project Structure

nba_analysis/

├── data/

├── notebooks/

├── QGIS/

├── reports/

├── results/

├── scripts/

├── venv/

├── .gitignore

├── README.md

├── requirements.txt



## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine.

```sh
git clone https://github.com/danceswithme/nba_analysis.git
cd nba_analysis
```

2. Create and Activate a Virtual Environment
On Windows
Create the Virtual Environment:

```sh
python -m venv venv
```

Activate the Virtual Environment:
```
venv\Scripts\activate
```

3. Install Required Packages
With the virtual environment activated, install the necessary packages:
```sh
pip install -r requirements.txt
```

4. Install MongoDB
Follow the instructions to install MongoDB from the official MongoDB website.

5. Install QGIS
Follow the instructions to install QGIS from the official QGIS website.


6. Ensure MongoDB is Running
Make sure MongoDB is running. You can start the MongoDB service by typing:
```sh
net start MongoDB
```

7. Using QGIS
Open the QGIS project file located in the 'qgis' directory within QGIS.


=======

# NBA Player Movement Analysis

This repository contains scripts and notebooks for analyzing the movement of NBA players between cities, focusing on various factors such as tax rates, per capita income (PCI), and annual temperatures.

## Getting Started

To get started, clone the repository and follow the instructions in each script and notebook. Ensure you have the necessary dependencies installed, which can be found in the `requirements.txt` file.

## Data Sources

- **Player Movement Data**: Retrieved from basketball-reference.com based on specific criteria lsted in the firsat sheet of players_that_fit_query.xlsx.
- **Temperature Data**: Retrieved from Open-Meteo.
- **PCI Data**: Collected from various sources for US States and Ontario. REAP Project for US and StatCan.gc.ca for Ontario.
- **Tax Rate Data**: Obtained from the Tax Foundation.

## Dependencies

- Python 3.x
- pymongo
- MongoDB
- QGIS
- Jupyter
- pandas
- matplotlib
- seaborn

Ensure you have these dependencies installed to successfully run the scripts and notebooks in this project.

## File Descriptions

### Initial Dataset
- **players_that_fit_query.xlsx**: Excel file containing detailed criteria and the list of players who meet those criteria sourced from basketball-reference.com.
- **players_data.csv**: CSV file with aggregated statistics of players meeting the specified criteria.

### Data Files
- **results/player_movements.json**: JSON file containing player movements data.
- **results/player_movements_tax.json**: JSON file containing player movements with tax data.
- **results/player_movements_pci.json**: JSON file containing player movements with PCI data.
- **results/player_movements_temp.json**: JSON file containing temporary player movements data.

## Python Scripts

### City and State Updates
- **update_city_state.py**: Adds state abbreviations to city data.

### Annual Temperature Data
- **annual_temperature_lookup.py**: Searches Open-Meteo for average temperature of cities and their given years.
- **finish_temperature.py**: Completes temperature data retrieval.

### Cost of Living
- **insert_pci_data.py**: Collects per capita income (PCI) for all US states and adds it to MongoDB.
- **insert_toronto_pci.py**: Collects PCI for Toronto and adds it to MongoDB.
- **update_pci_data.py**: Updates the player_movements collection with PCI for the states in the player documents.

### Tax Rate Data
- **tax_rate.py**: Sets tax rate tiers and years for US states and Ontario, obtained from Tax Foundation.
- **add_tax_player_movement.py**: Fills out documents in player_movements according to the tax_rate.py.

### Data Separation
- **separate_collections.py**: Creates new collections in MongoDB that only contain documents with either annual temperature, cost of living (PCI), or tax rate.

## Jupyter Notebooks

### Regression Analysis
- **regression1.ipynb**: Performs regression analysis on the dataset to determine the impact of different factors on player movements.

### Graphing
- **graphing.ipynb**: Generates various bar charts and visualizations to illustrate the data, including PCI, tax tiers, and temperature differences. PCI graphs are incorrectly titled and should be for states and provinces.
- **trend mapping.ipynb**: Creates trend maps that divides based on time periods.
- **plotbinnedfreq.ipynb**: Creates frequency bar charts for the most popular destinations and city-to-city movements, divided into different periods.

### Geographical Mapping

- **QGIS Project**: 
  - **Purpose**: Maps player movements geographically, displaying paths from former cities to new cities.
  - **Features**:
    - **Heatmaps**: Illustrate the popularity of destinations.
    - **Paths**: Show movements with varying transparency based on frequency.
    - **Graduated Layers**: Display average temperature, tax rates, and PCI.
  - **Base Map**: Includes a detailed map of North America.
  
- **Instructions**:
  1. Open the QGIS project file located in the `QGIS` folder.
  2. Ensure all required layers are loaded and visible.
  3. Turn on the relevant layers to visualize different aspects of the data (e.g., paths, heatmaps).
  4. Adjust transparency and other settings as needed to better understand the data.

This section provides users with a clear understanding of what the QGIS project includes and how to use it effectively.


## Notes
Ensure that the Excel file is named Players that fit Query.xls and the sheet is named Final List.
Make sure the CSV file is named Players that fit Query - Final List.csv.
Adjust the file paths in the script if your directory structure differs.

## Data
The data files are located in the 'nba_analysis/data' directory.

## Scripts
The Python script files are located in the 'nba_analysis/scripts' directory.

## Notebooks
Jupyter and other notebooks used for data analysis, along with output files are located in the 'nba_analysis/notebooks' directory.

## Results
Analysis results are saved in the 'nba_analysis/results' directory

## Reports
Reports summarizing journal entries along with an academic review of the resarch are in the 'nba_analysis/reports' directory

=======

## Contributing 
Feel free to submit issues or pull requests if you have any improvements or fixes.

## License
This project is licensed under the MIT License.

## Acknowledgements
A small list of the wonderful resources that aided in this project include MongoDB, basketball-reference.com, taxfoundation.org, REAP Project, open-meteo.com for historical weather API.
