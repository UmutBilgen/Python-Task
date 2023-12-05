class News:
    def __init__(self, url, header, summary, text, img_url_list, publish_date, update_date):
        """
        News constructor.

        Parameters:
        - url (str): The URL of the news.
        - header (str): The header or title of the news.
        - summary (str): The summary or excerpt of the news.
        - text (str): The main text content of the news.
        - img_url_list (list): List of image URLs associated with the news.
        - publish_date (str): The date when the news was published.
        - update_date (str): The date when the news was last updated.
        """
        self.url = url
        self.header = header
        self.summary = summary
        self.text = text
        self.img_url_list = img_url_list
        self.publish_date = publish_date
        self.update_date = update_date
