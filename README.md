# NBA Analysis Project

## Setup Instructions

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/danceswithme/nba_analysis.git
   cd nba_analysis

2. **Create a Virtual Environment**
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install Requirements**
pip install -r requirements.txt

4. **Run Jupyter Notebook**
jupyter notebook

5. **MongoDB Setup:**

Ensure MongoDB is installed and running.
Update MongoDB connection settings in your script if necessary.

**Project Structure**
nba_analysis/
├── data/
│   └── Players that fit Query.csv
├── scripts/
│   ├── save_csv_to_mongodb.py
│   └── setup_environment.sh  # Example shell script
├── arduino/
│   └── nba_analysis.ino      # Example Arduino sketch
├── notebooks/
│   └── analysis.ipynb
├── README.md
├── requirements.txt
└── .gitignore

**To save CSV data to MongoDB:**

sh
Copy code
python scripts/save_csv_to_mongodb.py

