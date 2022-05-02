import os 
import logging
from Metacritic_Webscraper_Latest import MetaCriticScraper
from time import perf_counter

log_filename = "logs/main.log"
if not os.path.exists(log_filename):
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)

logger = logging.getLogger(__name__)

# Set the default level as DEBUG 
logger.setLevel(logging.DEBUG)

# Format the logs by time, filename, function_name, level_name and the message
format = logging.Formatter(
    '%(asctime)s:%(filename)s:%(funcName)s:%(levelname)s:%(message)s'
)
file_handler = logging.FileHandler(log_filename)

# Set the formatter to the variable format

file_handler.setFormatter(format)

logger.addHandler(file_handler)


new_scraper = MetaCriticScraper("https://www.metacritic.com")
start_time = perf_counter()
new_scraper.sample_scraper('list_of_fighting_links')
stop_time = perf_counter()
logger.info(f'Total elapsed time {stop_time - start_time} seconds')