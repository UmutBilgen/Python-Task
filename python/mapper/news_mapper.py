from .base_mapper import BaseMapper

class NewsMapper(BaseMapper):
    def __init__(self, database):
        """
        NewsMapper constructor.

        Parameters:
        - database: The MongoDB database connection.
        """
        super().__init__(database, 'news')

    def create_news(self, news):
        """
        Create a news item in the database.

        Parameters:
        - news: An instance of the News class.

        Returns:
        - str: The ID of the inserted news item.
        """
        data = {
            'url': news.url,
            'header': news.header,
            'summary': news.summary,
            'text': news.text,
            'img_url_list': news.img_url_list,
            'publish_date': news.publish_date,
            'update_date': news.update_date
        }
        return self.create_item(data)
