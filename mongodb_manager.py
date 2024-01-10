import time

from flask import jsonify
from pymongo import MongoClient


class MongoDBManager:
    def __init__(self):
        self.client = MongoClient("mongodb://mongodb:27017/")
        self.db = self.client["webapp"]
        self.collection = self.db["contact_infos"]

    def store_data(self, name, email, message):
        try:
            # Get the count of existing documents
            count = self.collection.count_documents({})

            # #to make mongodb_error
            # temp_collection = self.collection
            # self.collection = ""

            # Insert the new document with additional fields
            entry_data = {
                "name": name,
                "email": email,
                "message": message,
                "timestamp": time.time(),
                "entry_number": count + 1,  # Increment count for the new entry
                "entry_date": time.strftime("%Y-%m-%d %H:%M:%S"),  # Add entry date
            }

            self.collection.insert_one(entry_data)

            print(
                f"Data stored in MongoDB successfully. Entry Number: {count + 1}, Entry Date: {entry_data['entry_date']}"
            )
            return jsonify({"success": "Data stored in MongoDB successfully"}), 200
        except Exception as e:
            # Hata durumunda istemciye uygun hata mesajını gönder
            return (
                jsonify(
                    {
                        "error": f"An error occurred while storing data in MongoDB: {str(e)}"
                    }
                ),
                500,
            )
