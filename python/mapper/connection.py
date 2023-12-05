
from pymongo import MongoClient
from utils.logs import get_logging

from pymongo import MongoClient
from utils.logs import get_logging

class MongoDBHandler:
    def __init__(self, host, database):
        """
        MongoDBHandler constructor.

        Parameters:
        - host (str): MongoDB server host.
        - database (str): Database name.
        """
        self.host = host
        self.database = database
        self.client = None

    def connect(self):
        """
        Establish a connection to MongoDB.

        Returns:
        pymongo.database.Database: MongoDB database object.
        """
        try:
            self.client = MongoClient(self.host)
            return self.client[self.database]
        except Exception as e:
            get_logging().error(f"An error occurred in the 'connect' method: {str(e)}")
            return None

    def disconnect(self):
        """
        Disconnect from MongoDB.
        """
        if self.client:
            self.client.close()
            # print("MongoDB Connection Closed.")

