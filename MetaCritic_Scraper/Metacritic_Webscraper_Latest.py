import csv
import time 
from time import perf_counter
import os 
import selenium
import json 
# from selenium import webdriver 
from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib3 import Timeout
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import urllib.request
from Scraper import Scraper


class MetaCriticScraper(Scraper): 

    def __init__(self, url):
        super().__init__()
       
        try:
            self.driver.set_page_load_timeout(30)
            self.land_first_page(url)
        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))
            self.driver.quit()

        self.accept_cookies('//button[@id="onetrust-accept-btn-handler"]')
        self.page_counter = 0

        #TODO: Adjust the keys of the self.xpaths_dict to take the headings from the pages. 
        self.xpaths_dict = {
                    'Title': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/a/h1', 
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
        print(genre_container)
        print(len(genre_container))

        list_of_genres = []
        for item in genre_container:
            list_of_genres.append(item.get_attribute('href'))

        print(list_of_genres)
        return list_of_genres

   

    def click_next_page(self, page):

        #TODO: find a way to generalise this code for all pages on the website. Maybe make another method to check the last page? 
    
        next_page_element = self.driver.find_element(
            By.XPATH, 
        f'//*[@id="main_content"]/div[1]/div[2]/div/div[1]/div/div[9]/div/div/div[2]/ul/li[{page}]/*'
        )
        next_page_url = next_page_element.get_attribute('href')
        self.driver.get(next_page_url)
        print(next_page_url)
        print('navigating to next page')
        
        return next_page_url
           
    
    def get_information_from_page(self):   
        
    
        #TODO: This could be a staticmethod? 
        for key,xpath in self.xpaths_dict.items():
         
            
            try:
                if key == 'Description':
                    web_element = self.driver.find_element(By.XPATH, '//div[@class="summary_wrap"]') 

                    try:
                        
                        collapse_button = web_element.find_element(By.XPATH, './/span[@class="toggle_expand_collapse toggle_expand"]')
                        if collapse_button:
                            collapse_button.click()
                            expanded_description = web_element.find_element(By.XPATH, './/span[@class="blurb blurb_expanded"]')
                            self.information_dict[key] = expanded_description.text

                    except:
                           summary = web_element.find_element(By.XPATH, xpath)
                           self.information_dict[key] = summary.text

                   
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


    def sample_scraper(self):
        # Goes to Games > Games Home > 'Search by Genre': Fighting > Scrapes 6 pages of content 
        self.choose_genre()
        
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
        
        


        
# new syntax for driver.find_elements(By.XPATH, "xpath string")
if __name__ == '__main__':     
    new_scraper = MetaCriticScraper("https://www.metacritic.com")
    # new_scraper.choose_genre()
    # new_scraper.collect_page_links()
    # new_scraper.get_information_from_page()
    # new_scraper.click_next_page()
    # new_scraper.collect_number_of_pages()
    # new_scraper.click_next_page_3()
    # new_scraper.last_page()
    # new_scraper.process_page_links()

    # Timing how long it takes to scrape from 100 pages 
    # t1_start = perf_counter()
    new_scraper.choose_category('music')
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

