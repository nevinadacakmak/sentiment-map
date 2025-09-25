from pymongo import MongoClient
import os
import pandas as pd


class MongoDBClient:
    def __init__(self, uri: str = None, db_name: str = None):
        # Allow passing uri and db_name directly, or fall back to env
        self.uri = uri or os.getenv('MONGODB_URI')
        if not self.uri:
            raise ValueError('MongoDB URI must be provided via argument or MONGODB_URI env var')

        self.client = MongoClient(self.uri)
        if not db_name:
            raise ValueError('db_name must be provided')
        self.db = self.client[db_name]

    def insert_data(self, collection_name: str, data: list):
        collection = self.db[collection_name]
        if not data:
            return []
        # Expect list of dicts or DataFrame
        if isinstance(data, pd.DataFrame):
            records = data.to_dict(orient='records')
        else:
            records = data
        result = collection.insert_many(records)
        return result.inserted_ids

    def store_data(self, collection_name: str, data):
        """Compat wrapper used by main: accepts DataFrame or list of dicts."""
        return self.insert_data(collection_name, data)

    def update_data(self, collection_name: str, query: dict, update: dict):
        collection = self.db[collection_name]
        result = collection.update_many(query, update)
        return result.modified_count

    def retrieve_data(self, collection_name: str, query: dict = None):
        collection = self.db[collection_name]
        query = query or {}
        return list(collection.find(query))

    def get_sentiment_data(self, collection_name: str):
        # Convenience function used by dashboard
        records = self.retrieve_data(collection_name, {})
        return records

    def close_connection(self):
        self.client.close()