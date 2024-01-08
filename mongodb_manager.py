from pymongo import MongoClient
import time


class MongoDBManager:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['webapp']
        self.collection = self.db['contact_infos']

    def store_data(self, name, email, message):
        try:
            # Get the count of existing documents
            count = self.collection.count_documents({})

            # Insert the new document with additional fields
            entry_data = {
                'name': name,
                'email': email,
                'message': message,
                'timestamp': time.time(),
                'entry_number': count + 1,  # Increment count for the new entry
                'entry_date': time.strftime("%Y-%m-%d %H:%M:%S")  # Add entry date
            }

            self.collection.insert_one(entry_data)

            print(
                f"Data stored in MongoDB successfully. Entry Number: {count + 1}, Entry Date: {entry_data['entry_date']}")
        except Exception as e:
            print(f"An error occurred while storing data in MongoDB: {e}")
