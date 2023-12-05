from utils.logs import get_logging

class BaseMapper:
    def __init__(self, database, collection_name):
        """
        BaseMapper constructor.

        Parameters:
        - database (pymongo.database.Database): MongoDB database object.
        - collection_name (str): Name of the MongoDB collection.
        """
        self.collection = database[collection_name]
        
    def create_item(self, data):
        """
        Create a new document in the MongoDB collection.

        Parameters:
        - data (dict): Dictionary containing document data.

        Returns:
        ObjectId: The inserted document's ObjectId.
        """
        try:
            result = self.collection.insert_one(data)
            get_logging().info("Insert process successfully")
            return result.inserted_id
        except Exception as e:
            get_logging().error(str(e))
