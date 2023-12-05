from .base_mapper import BaseMapper

class WordFrequencyMapper(BaseMapper):
    def __init__(self, database):
        """
        WordFrequencyMapper constructor.

        Parameters:
        - database: The MongoDB database connection.
        """
        super().__init__(database, 'word_frequency')

    def create_word_frequency(self, word_frequency):
        """
        Create word frequency items in the database.

        Parameters:
        - word_frequency: A list of WordFrequency instances.

        Returns:
        - None
        """
        for instance in word_frequency:
            data = {
                'word': instance.word,
                'count': instance.count,
            }
            self.create_item(data)
