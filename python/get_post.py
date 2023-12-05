import requests
from bs4 import BeautifulSoup
from utils.word_counter import determine_most_used_words 
from mapper.models.news_model import News
from mapper.models.word_frequency_model import WordFrequency
from mapper.news_mapper import NewsMapper
from mapper.word_frequency import WordFrequencyMapper 
from mapper.connection import MongoDBHandler
import os
from dotenv import load_dotenv
from utils.logs import get_logging
load_dotenv()
LINK_PATH = "div.kategori_yazilist div.row article div.haber-post"
POST_PATH = "div.row div.col-12.col-lg-8 div.post_line"
HEADER_TAG = "h1"
HEADER_CLASS = "single_title"
SUMMARY_TAG = "h2"
SUMMARY_CLASS = "single_excerpt"
TIME_TAG_DIV = "div"
TIME_DIV_CLASS = 'yazibio'
TIME_TAG_SPAN = "span"
TIME_SPAN_CLASS = "tarih"
TIME_TAG = "time"
TIME_CLASS = "datetime"
TEXT_TAG = "div"
TEXT_CLASS = "yazi_icerik"
TEXT_PARAGRAF_TAG = 'p'
IMG_TAGS = "img"
IMG_PATH = "data-src"

stats = {
    "fail_count":0,
    "succses_count":0
}



def get_page_link(page_number):
    """
        Parameters:
        - page_number (int): The page number for which the URL is generated.

        Returns:
        str: The URL for the specified page in the news category.
    """

    return f'https://turkishnetworktimes.com/kategori/gundem/page/{page_number}/'


def get_soup(url):
    """
    Retrieves the BeautifulSoup object for a given URL.

    Parameters:
    - url (str): The URL to fetch and parse.

    Returns:
    BeautifulSoup: The BeautifulSoup object representing the parsed HTML content.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return soup
    except Exception as e:
        stats['fail_count'] += 1
        get_logging().error(f"An error occurred in the 'get_soup' function {str(e)}")


def fetch_news_links(soup):
    """
        Extracts and returns the news links from the provided BeautifulSoup object.

        Parameters:
        - soup (BeautifulSoup): The BeautifulSoup object representing the parsed HTML content.

        Returns:
        list: A list of news links.
    """
    try:
        post_links = soup.select(LINK_PATH)
        post_href = [item.find('a').get('href') for item in post_links]
        return post_href
    except Exception as e:
        stats['fail_count'] += 1
        get_logging().error(f"An error occurred in the 'fetch_news_links' function {str(e)}")


def get_headers(page):
    """
        Extracts and returns the header from the provided BeautifulSoup page.

        Parameters:
        - page (BeautifulSoup): The BeautifulSoup object representing the parsed HTML content.

        Returns:
        str: The header text.
    """
    try:
        headers = page.find(HEADER_TAG,class_=HEADER_CLASS).text
        return headers
    except Exception as e:
        stats['fail_count'] += 1
        get_logging().error(f"An error occurred in the 'get_headers' function {str(e)}")


def get_times(page):
    """
        Extracts and returns the publish and update date from the provided BeautifulSoup page.

        Parameters:
        - page (BeautifulSoup): The BeautifulSoup object representing the parsed HTML content.

        Returns:
        tuple: A tuple containing the publish date and update date as strings.
    """
    try:
        times = page.find(TIME_TAG_DIV, class_=TIME_DIV_CLASS).find_all(TIME_TAG_SPAN, class_=TIME_SPAN_CLASS)
        time_publish, time_update = [time.find(TIME_TAG).get(TIME_CLASS) for time in times]

        return time_publish,time_update
    except Exception as e:
        stats['fail_count'] += 1
        get_logging().error(f"An error occurred in the 'get_times' function {str(e)}")


def get_summary(page):
    """
        Extracts and returns the summary text from the provided BeautifulSoup page.

        Parameters:
        - page (BeautifulSoup): The BeautifulSoup object representing the parsed HTML content.

        Returns:
        str: The summary text stripped of leading and trailing whitespaces.
    """
    try:
        return page.find(SUMMARY_TAG,class_=SUMMARY_CLASS).text.strip()
    except Exception as e:
        stats['fail_count'] += 1
        get_logging().error(f"An error occurred in the 'get_summary' function {str(e)}")


def get_text(page):
    try:
        text = page.find(TEXT_TAG,class_ = TEXT_CLASS).find_all(TEXT_PARAGRAF_TAG)
        return "".join(item.text.strip() for item in text if item.text)
    except Exception as e:
        stats['fail_count'] += 1
        get_logging().error(f"An error occurred in the 'get_text' function {str(e)}")


def get_image_url(page):
    try:
        return [item.get(IMG_PATH) for item in page.find_all(IMG_TAGS)] 
    except Exception as e:
        stats['fail_count'] += 1
        get_logging().error(f"An error occurred in the 'get_image_url' function {str(e)}")


def simple_process(haber_url):
    """
    Extracts and returns the text content from the provided BeautifulSoup page.

    Parameters:
    - page (BeautifulSoup): The BeautifulSoup object representing the parsed HTML content.

    Returns:
    str: The concatenated text content from all paragraphs, stripped of leading and trailing whitespaces.
    """
    try:
        # print(stats,haber_url)
        soup = get_soup(haber_url)
        page = soup.select(POST_PATH)[0]
        publish_date, update_date = get_times(page)
        header = get_headers(page)
        summary = get_summary(page)
        text = get_text(page)
        img_url_list = get_image_url(page)

        words = determine_most_used_words(text,10)
        news_obj = create_news_object(haber_url, header, summary, text, img_url_list, publish_date, update_date)

        # Transform words into WordFrequency objects
        word_list = transform_class_words(words)

        return news_obj, word_list,words
    
    except Exception as e:
        stats['fail_count'] += 1
        get_logging().error(f"An error occurred in the 'process' function {str(e)}")


def create_news_object(url, header, summary, text, img_url_list, publish_date, update_date):
    """
        Creates and returns a News object with the provided information.

        Parameters:
        - url (str): The URL of the news.
        - header (str): The header/title of the news.
        - summary (str): The summary or excerpt of the news.
        - text (str): The full text content of the news.
        - img_url_list (list): A list of image URLs associated with the news.
        - publish_date (str): The publish date of the news.
        - update_date (str): The last update date of the news.

        Returns:
        News: The News object created with the provided information.
    """
    try:
        return News(url=url, header=header, summary=summary, text=text,
                    img_url_list=img_url_list, publish_date=publish_date, update_date=update_date)
    except Exception as e:
        get_logging().error(f"An error occurred in the 'create_news_object' function {str(e)}")


def transform_class_words(words):
    """
        Transforms a list of words and their counts into a list of WordFrequency objects.

        Parameters:
        - words (list): A list of tuples where each tuple contains a word and its count.

        Returns:
        list: A list of WordFrequency objects created from the provided words.
    """
    try:
        word_list = []
        for word, count in words:
            # print(word,count)
            word_frequency = WordFrequency(word, count)
            word_list.append(word_frequency)
        return word_list
    except Exception as e:
        get_logging().error(f"An error occurred in the 'transform_class_words' function {str(e)}")


def connect_db():
    """
        Establishes a connection to the MongoDB database.

        Returns:
        MongoDBHandler: A MongoDBHandler instance representing the database connection.
    """
    try:
        connection = MongoDBHandler(
                host=os.environ.get("ME_CONFIG_MONGODB_URL"),
                database=os.environ.get("MONGODB_DATABASE_NAME")
            )
        get_logging().info("Connections started successfully.")
        return connection
    except Exception as e:
        get_logging().error(str(e))


def threading_process(haber_url,total_stats):
    """
        Process news data using multithreading.

        Parameters:
        - haber_url (str): The URL of the news to be processed.
        - total_stats (dict): Dictionary to store success and failure counts.

        Returns:
        tuple: A tuple containing words, news URL, and updated total_stats.
    """
    try:
        stats = total_stats
        stats['succses_count'] +=1
        news,word_list,words = simple_process(haber_url)
        client = connect_db()
        db = client.connect()
        NewsMapper(db).create_news(news)
        WordFrequencyMapper(db).create_word_frequency(word_list)
        client.disconnect()
        return words,haber_url,stats
    except Exception as e:
        stats['fail_count'] += 1
        get_logging().error(f"An error occurred in the 'process' function {str(e)}")




