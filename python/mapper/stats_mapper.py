from .base_mapper import BaseMapper

class StatsMapper(BaseMapper):
    def __init__(self, database):
        """
        StatsMapper constructor.

        Parameters:
        - database (pymongo.database.Database): MongoDB database object.
        """
        super().__init__(database, 'stats')

    def create_stats(self, stats):
        """
        Create a new stats document in the 'stats' collection.

        Parameters:
        - stats (dict): Dictionary containing stats information.

        Returns:
        ObjectId: The inserted document's ObjectId.
        """
        data = {
            "elapsed_time": stats.elapsed_time,
            "count": stats.count,
            "date": stats.date,
            "success_count": stats.success_count,
            "fail_count": stats.fail_count,
        }
        return self.create_item(data)
