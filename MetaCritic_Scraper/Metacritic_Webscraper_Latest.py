import csv
import time 
from time import perf_counter
import os 
import selenium
import json 
# from selenium import webdriver 
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from urllib3 import Timeout
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import urllib.request
from Scraper import Scraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from alive-progress import alive_bar
import uuid
import sys
import random
# sys.path.append("/media/blair/Fast Partition/My Projects/student_projects/Metacritic_Webscraper-/MetaCritic_Scraper")


class MetaCriticScraper(Scraper): 

    def __init__(self, url):
        super().__init__()
        
       
        try:
            self.driver.set_page_load_timeout(30)
            self.land_first_page(url)
        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))
            self.driver.quit()

        self.page_counter = 0

        #TODO: Adjust the keys of the self.xpaths_dict to take the headings from the pages. 
        self.xpaths_dict = {
            'UUID': "",
            'Title': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/a/h1',
            'Link_to_Page': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/a', 
            'Platform': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/span', 
            'Release_Date': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[3]/ul/li[2]/span[2]',
            'MetaCritic_Score': '//a[@class="metascore_anchor"]/div', 
            'User_Score': '//div[@class="userscore_wrap feature_userscore"]/a/div',
            'Developer': '//li[@class="summary_detail developer"]/span[2]/a', 
            'Description': './/li[@class="summary_detail product_summary"]' } 

        #NEW Category Dict to use in choose_category method? 
        self.category_dict = {
            'Game Xpath': '//*[@id="primary_nav_item_games"]/nav/div/div[1]/div[2]/ul/li[1]/a',
            'Music Xpath': '//*[@id="primary_nav_item_music"]/nav/div[2]/ul/li[1]/a',
            'TV Xpath': '//*[@id="primary_nav_item_tv"]/nav/div/div[1]/div[2]/ul/li[1]/a', 
            'Movie Xpath': '//*[@id="primary_nav_item_movies"]/nav/div/div[1]/div[2]/ul/li[6]/a'}

        self.information_dict =  {}

    def accept_cookies(self, cookies_button_xpath: str):
        return super().accept_cookies(cookies_button_xpath)
        
   
    def choose_category(self, category_selection : str = 'game' or 'music'):

        '''
        Currently works for games and music pages 

        '''
        # Choose the game category from the list
        # TODO: This method should choose a category based on what is passed into the argument of the function 

        # Make a function which goes to the page of a section based on what is passed 
        # Into the argument of the function. 

        # Get a list of hrefs of the pages that you want to go to. 

        # List of hrefs to visit 
        href_list = [
            "https://www.metacritic.com/game",
            "https://www.metacritic.com/music",
            "https://www.metacritic.com/tv", 
            "https://www.metacritic.com/browse/movies/score/metascore/all/filtered?sort=desc"
            

        ]
        if category_selection == 'game':
            try:
                self.driver.get(href_list[0])
            except TimeoutException:
                self.driver.refresh()
                time.sleep(3)
                self.driver.get(href_list[0])
        else:
            try:
                self.driver.get(href_list[1])
            except TimeoutException:
                self.driver.refresh()
                time.sleep(3)
                self.driver.get(href_list[1])
        
        # Game Xpath: '//*[@id="primary_nav_item_games"]/nav/div/div[1]/div[2]/ul/li[1]/a'
      
        print(f'Navigating to: {category_selection}')
        return category_selection 



    def choose_genre(self):

        '''
        Currently works for games, tv and music 

        '''
        genre_container = self.driver.find_elements(By.XPATH, 
            '//ul[@class="genre_nav"]//a')
       

        list_of_genre_links = []
        list_of_genres = []
        for item in genre_container:
            list_of_genre_links.append(item.get_attribute('href'))
            list_of_genres.append(item.text)

        print(list_of_genre_links)
        print(list_of_genres)
        return list_of_genre_links

   

    def click_next_page(self, page):

        #TODO: find a way to generalise this code for all pages on the website. 
        # Maybe make another method to check the last page? 
    
        next_page_element = self.driver.find_element(
            By.XPATH, 
            f'//*[@id="main_content"]/div[1]/div[2]/div/div[1]/div/div[9]/div/div/div[2]/ul/li[{page}]/*'
        )
        # //*[@id="main_content"]/div[1]/div[2]/div/div[1]/div/div[9]/div/div/div[2]/ul/li[7]/a
        next_page_url = next_page_element.get_attribute('href')
       
        self.driver.get(str(next_page_url))
        print(page)
        print(type(page))
        # print(next_page_url)
        print('navigating to next page')
        
        return next_page_url
           
    
    def get_information_from_page(self):   
        
    
        #TODO: This could be a staticmethod? 
        for key,xpath in self.xpaths_dict.items():
         
            
            try:
                # if the key in the dictionary == description. Expand the description text on the page. 
                if key == 'Description':
                    # Look inside the container 
                    web_element = self.driver.find_element(By.XPATH, '//div[@class="summary_wrap"]') 

                    try:
                        # try to find the collapse button inside the container using relative xpath './/'
                        collapse_button = web_element.find_element(By.XPATH, './/span[@class="toggle_expand_collapse toggle_expand"]')
                        if collapse_button:
                            collapse_button.click()
                            expanded_description = web_element.find_element(By.XPATH, './/span[@class="blurb blurb_expanded"]')
                            self.information_dict[key] = expanded_description.text
                    # If there is no expand button inside the description field, set the key of information dict to the 
                    # text of the xpath found. 
                    except:
                        summary = web_element.find_element(By.XPATH, xpath)
                        self.information_dict[key] = summary.text

                   
                else:
                    # Further logic for special cases: UUID and the Link_to_Page.
                    if key == 'UUID':
                        self.information_dict[key] = xpath

                    elif key == 'Link_to_Page':
                        web_element = self.driver.find_element(By.XPATH, xpath).get_attribute('href') 
                        self.information_dict[key] = web_element

                        
                    else:
                        web_element = self.driver.find_element(By.XPATH, xpath) 
                        self.information_dict[key] = web_element.text 

            except:     
                self.information_dict[key] = 'Null'

        

        print(self.information_dict)
        return self.information_dict

        # if conditionA:
            # Code that executes when 'conditionA' is True

            # if conditionB:
                # Code that runs when 'conditionA' and
                # 'conditionB' are both True

    
    def process_page_links(self):
        #TODO: Make this method return a list of links for all pages to visit.
        #TODO: Look at the logic behind click_next_page method.
        self.accept_cookies('//button[@id="onetrust-accept-btn-handler"]') 
        list_of_all_pages_to_visit = []
        
        for url in self.choose_genre():
            list_of_all_pages_to_visit.append(url)
            self.driver.get(url) 
            try:
                page_value = self.collect_number_of_pages(
                    '#main_content > div.browse.new_releases > div.content_after_header > \
                    div > div.next_to_side_col > div > div.marg_top1 > div > div > div.pages > ul > \
                    li.page.last_page > a'
                )
                range_final = page_value + 1
            except:
                #self.driver.implicitly_wait(5)
                self.extract_the_page_links('//a[@class="title"]', 'href')
                range_final = 0
            for i in range(1, range_final):
                with open("list_of_links.txt", 'a+') as file:
                #self.driver.implicitly_wait(5)
                    list_of_all_pages_to_visit.extend(self.extract_the_page_links('//a[@class="title"]', 'href'))
                    while len(list_of_all_pages_to_visit) > 0: 
                        url = list_of_all_pages_to_visit.pop(0)
                        file.write(str(url))
                        file.write('\n')
                    try:
                        (WebDriverWait(self.driver, 1)
                        .until(EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="main_content"]/div[1]/div[2]/div/div[1]/div/div[9]/div/div/div[1]/span[2]/a/span')
                            )
                        )).click()
                        print('navigating to next page')
                    except TimeoutException:
                        if range_final:
                            break
                    #TODO: During this loop, the outputs of the links are stored inside a text file to be called when running the sample_scraper method 
                



    def sample_scraper(self):
        # Goes to Games > Games Home > 'Search by Genre': Fighting > Scrapes 6 pages of content 
        self.accept_cookies('//button[@id="onetrust-accept-btn-handler"]')
        genre_list = self.choose_genre()
        self.driver.get(genre_list[2])
        
        #TODO populate the all_pages_list with hrefs from ALL pages in the 'Games' section of the website. 
        
        all_pages_list = []
        
        # filter_list = self.apply_filter_list(
        # '//ul[@class="dropdown dropdown_open"]//li/a',
        # '//div[@class="mcmenu dropdown style2 genre"]'
    # )

        # Collect the number of pages on the page to use in range function

        page_value = self.collect_number_of_pages(
            '#main_content > div.browse.new_releases > div.content_after_header > \
            div > div.next_to_side_col > div > div.marg_top1 > div > div > div.pages > ul > \
            li.page.last_page > a'
        )
        # Set the final range to +1 more to satisfy the range function

        range_final = page_value + 1
        # for page in range(2,rangefinal):
        for page in range(2,range_final):
            all_pages_list.extend(self.extract_the_page_links('//a[@class="title"]', 'href'))
            time.sleep(1)
            self.click_next_page(page)

        all_pages_list.extend(self.extract_the_page_links('//a[@class="title"]', 'href'))

        for url in all_pages_list:
            time.sleep(1)
            #TODO: use a try and except statement to catch the timeout exception. 
            try:
                self.driver.get(url)
                time.sleep(2)
            except TimeoutException:
                time.sleep(4)
                self.driver.refresh()
                self.driver.get(url) 
                
            self.get_information_from_page()
        
    def scrape_games(self, file_name):
        with open(f"{file_name}.txt") as file:
            number_of_lines = len(file.readlines())

            content_list= []
            image_list = []
           
            with alive_bar(number_of_lines, dual_line=True, title='Progress') as progress_bar: 
                for line in file:
                    
                    self.driver.get(str(line))
                    content_list.append(self.get_information_from_page())

                    image_list.append(self.save_image_links(
                        'image_name',
                        '//*[@id="main"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div/img'
                    ))
                    progress_bar()
                    #TODO: The scraper breaks on random pages when it tries to get images. Why? 

                self.save_json(content_list, 'raw-data')
                self.save_json(image_list, 'image_data')
            # logger.info('Scrape Complete! Exiting..')
            self.driver.quit()
        return content_list

      

        
# new syntax for driver.find_elements(By.XPATH, "xpath string")
if __name__ == '__main__':     
    new_scraper = MetaCriticScraper("https://www.metacritic.com/game")
    # new_scraper.choose_genre()
    # new_scraper.collect_page_links()
    # new_scraper.get_information_from_page()
    new_scraper.process_page_links()
    # new_scraper.click_next_page()
    # new_scraper.collect_number_of_pages()
    # new_scraper.click_next_page_3()
    # new_scraper.last_page()
    # new_scraper.process_page_links()
    # new_scraper.choose_category('music')
    # Timing how long it takes to scrape from 100 pages 
    # t1_start = perf_counter()
  
    # new_scraper.sample_scraper()
    # t1_stop = perf_counter()
    # print(f'Total elapsed time {round(t1_stop - t1_start)} seconds')

# Current stats(1/01/2022): 100 pages in 226 seconds (2 minutes, 4 seconds.)
# Current stats(27/01/2022): 500 pages in 2828 seconds (47 minutes, 8 seconds)
# Current stats (3/02/2022): 524 pages in 1742 seconds (29 minutes)
# Current stats (14/02/2022): 500 pages in 3145 seconds (52 minutes, 24 seconds)
# Current stats (15/02/2022): 524 pages in 2481 seconds (41 minutes, 21 seconds)
# Current stats (15/02/2022, 22:46pm): 524 pages in 2697 seconds (44 minutes, 57 seconds)
# Current stats (22/03/2022): 524 pages in 2677 seconds (44 minutes, 37 seconds)

