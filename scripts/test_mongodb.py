from pymongo import MongoClient

def test_mongo_connection():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client.test_database
        collection = db.test_collection
        test_document = {"name": "test"}
        collection.insert_one(test_document)
        print("Connection successful and document inserted.")
        client.drop_database('test_database')  # Clean up after test
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_mongo_connection()