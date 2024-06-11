# NBA Analysis Project

## Setup Instructions

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/danceswithme/nba_analysis.git
   cd nba_analysis

2. **Create a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install Requirements**
   ```sh
   pip install -r requirements.txt

5. **Run Jupyter Notebook**
   ```sh
   jupyter notebook

7. **MongoDB Setup:**

   Ensure MongoDB is installed and running.
   Update MongoDB connection settings in your script if necessary.


**To save CSV data to MongoDB:**

```sh
Copy code
python scripts/save_csv_to_mongodb.py

