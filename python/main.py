import os
from dotenv import load_dotenv
from utils.logs import get_logging
from concurrent.futures import ThreadPoolExecutor
import time 
from datetime import datetime
from utils.draw_graph import word_graph_draw
from get_post import (
    get_page_link,
    get_soup,
    threading_process,
    fetch_news_links,
    connect_db,
)
from mapper.models.stats_model import Stats
from mapper.base_mapper import BaseMapper

load_dotenv()
get_logging().info("Program started successfully.")

start_time = time.time()
PAGE_NUMBER = 50

for page_number in range(1, PAGE_NUMBER):
    urls = get_page_link(page_number)
    soup = get_soup(urls)
    post_urls = fetch_news_links(soup)

    with ThreadPoolExecutor() as executor:
        total_stats = {
            "total_suc": 0,
            "total_fail": 0,
            "total_count": 0,
        }
        futures = []
        for posts in post_urls:
            tempts = {
                "fail_count": 0,
                "succses_count": 0,
            }
            futures.append(executor.submit(threading_process, posts, tempts))

        for future in futures:
            words, posts, stats = future.result()
            word_graph_draw(words, posts)
            total_stats["total_suc"] += stats["succses_count"]
            total_stats["total_fail"] += stats["fail_count"]

        total_stats["total_count"] = total_stats["total_suc"] + total_stats["total_fail"]
        stop_time = time.time()
        now = datetime.now()
        now_formated = now.strftime("%Y-%m-%d %H:%M")
        passing_time = stop_time - start_time
        stats = {
            "elapsed_time": passing_time,
            "count": total_stats["total_count"],
            "date": now_formated,
            "success_count": total_stats["total_count"],
            "fail_count": total_stats["total_fail"],
        }
        client = connect_db()
        db = client.connect()
        
        BaseMapper(db, "stats").create_item(stats)
        client.disconnect()
