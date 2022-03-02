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
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import urllib.request

'''
Main Class Code things to do (22/02/2022)

1. Add a method to save the image(s) on the page 

2. DONE: Add a method to save the outputs to a .json format. 
   (if possible, extend this to other formats)

3. Add a method (or seperate class) to interact 
   with the filters on pages

'''

class MetaCriticScraper: 

    def __init__(self, url, options=None):
        if options:
            self.driver = Chrome(ChromeDriverManager().install(), options=options)
        else:
            self.driver = Chrome(ChromeDriverManager().install())

        
        # Temporary change in root to debug collecting information from the page. 
        # Original root =  "https://www.metacritic.com/"
        # Good game root = "https://www.metacritic.com/game/xbox/halo-combat-evolved"
        # Bad game root = "https://www.metacritic.com/game/gamecube/charlies-angels"
        # Mixed game root = "https://www.metacritic.com/game/pc/white-shadows"
        # Sample page root = "https://www.metacritic.com/browse/games/genre/date/fighting/all"
        # Sample page root short description = "https://www.metacritic.com/game/playstation-3/divekick"
        # Sample page root long description = "https://www.metacritic.com/game/pc/mortal-kombat-komplete-edition"
        self.root = "https://www.metacritic.com/"

        #TODO: Implement Headless Mode into the main code and test it out  
        try:
            self.driver.set_page_load_timeout(30)
            self.driver.get(url)
        except TimeoutException as ex:
            isrunning = 0
            print("Exception has been thrown. " + str(ex))
            self.driver.quit()

        
        # driver.get(self.root)
        self.accept_cookies('//button[@id="onetrust-accept-btn-handler"]')
        self.page_counter = 0

        self.xpaths_dict = {'Title': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/a/h1', 
                   'Platform': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/span', 
                   'Release_Date': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[3]/ul/li[2]/span[2]',
                   'MetaCritic_Score': '//a[@class="metascore_anchor"]/div', 
                   'User_Score': '//div[@class="userscore_wrap feature_userscore"]/a/div',
                   'Developer': '//li[@class="summary_detail developer"]/span[2]/a', 
                   'Description': './/li[@class="summary_detail product_summary"]' } 

        self.information_dict =  {}
        

    def accept_cookies(self, cookies_button_xpath, iframe=None): 
        #TODO: Create a unittest for this method 
        time.sleep(4)
        try: # To find if the accept cookies button is within a frame 
            self.driver.switch_to.frame(iframe)
            accept_cookies = self.driver.find_element(By.XPATH, cookies_button_xpath)
            accept_cookies.click()
        except NoSuchElementException: # If it is not within a frame then find the xpath and proceed click it. 
            print('No iframe found')
            accept_cookies = self.driver.find_element(By.XPATH, cookies_button_xpath)
            accept_cookies.click()
        time.sleep(2)
        return True 


        
    
    def choose_game_category(self):
        # Choose the game category from the list
        # TODO: Iterate over the game category list  
        category_selection_games = self.driver.find_element(By.XPATH,'//*[@id="primary_nav_item_games"]/nav/div/div[1]/div[2]/ul/li[1]/a').get_attribute("href")
        game_url = print(category_selection_games)
        self.driver.get(category_selection_games)
        return game_url


    # TODO: make a method which chooses the genre from the homepage. 

    def choose_genre(self):
        choose_fighting_genre = self.driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div[2]/div[2]/div[1]/div/div/div/ul/li[3]/a').get_attribute("href")
        fighting_genre_url = print(choose_fighting_genre)
        self.driver.get(choose_fighting_genre)
        return fighting_genre_url
        
    #TODO: make a method which collects the links from each of the items on the page. 

    
    def collect_page_links(self):
        #TODO: Try find_elements(By.CSS_SELECTOR)
        page_container = self.driver.find_elements(By.XPATH, '//a[@class="title"]')
        page_links_list = []

        for url in page_container:
            link_to_page = url.get_attribute('href')
            page_links_list.append(link_to_page)
            self.page_counter += 1
       
        print(page_links_list)
        print(len(page_links_list))
        print(f'Pages visited: {self.page_counter}')
        return page_links_list
    
    
    
    # TODO: Make the scraper click the next page and take the links from there. 
    # Try these links out: 
    # https://stackoverflow.com/questions/56019749/python-web-scraping-how-to-loop-all-pages-next-page
    # https://stackoverflow.com/questions/55005839/python-web-scraping-using-selenium-clicking-on-next-page
    # https://www.google.com/search?q=python+selenium+scrape+next+pages&rlz=1C1VDKB_en-GBGB964GB964&oq=python+selenium+scrape+next+pages+&aqs=chrome..69i57j33i22i29i30l3.5678j1j7&sourceid=chrome&ie=UTF-8

    def click_next_page(self, page):

        #TODO: find a way to generalise this code for all pages on the website. Maybe make another method to check the last page? 
    
        next_page_element = self.driver.find_element(By.XPATH, f'//*[@id="main_content"]/div[1]/div[2]/div/div[1]/div/div[9]/div/div/div[2]/ul/li[{page}]/*')
        next_page_url = next_page_element.get_attribute('href')
        self.driver.get(next_page_url)
        print(next_page_url)
        print('navigating to next page')
        
        return next_page_url

    def collect_number_of_pages(self):
        #TODO: Generalise the CSS_Selector. It's too long and specific to only the fighting games page?  
        last_page_number_element = (self.driver.find_element(By.CSS_SELECTOR, 
        '#main_content > div.browse.new_releases > div.content_after_header > \
        div > div.next_to_side_col > div > div.marg_top1 > div > div > div.pages > ul > \
        li.page.last_page > a' ).text)
        print(last_page_number_element)
        print(f"Processing page {last_page_number_element}..")
        last_page_number = int(last_page_number_element)

            # try:
            #     next_page_link = self.driver.find_element(By.XPATH, f'.//li[span = "{current_page_number + 1}"]')
            #     next_page_link.click()
            # except NoSuchElementException:
            #     print(f"Exiting. Last page: {current_page_number}.")
            #     break
        return last_page_number
           
    
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

    #TODO: make a method which makes the scraper go to these links
    # This link should help: 
    # https://pretagteam.com/question/loop-through-links-and-scrape-data-from-resulting-pages-using-selenium-python-duplicate

    def save_json(self, all_products_dictionary, sub_category_name):
        #TODO: Run a unittest on this method to check that a json file is created
        file_to_convert = all_products_dictionary
        file_name = f'{sub_category_name}-details.json'

        if not os.path.exists('json-files'):
            os.makedirs('json-files')
        with open(f'json-files/{file_name}', mode='a+', encoding='utf-8-sig') as f:
            json.dump(file_to_convert, f, indent=4, ensure_ascii=False) 
            f.write('\n')
        return True     


    def sample_scraper(self):
        # Goes to Games > Games Home > 'Search by Genre': Fighting > Scrapes 6 pages of content 
        self.choose_game_category()
        self.choose_genre()

        root_page = "https://www.metacritic.com/game"

        all_pages_list = []

        #TODO: steps for future 
        #range needs to be set dynamically instead of hardcoded
        page_value = self.collect_number_of_pages()
        range_final = page_value + 1
        # for page in range(2,rangefinal):
        for page in range(2,range_final):
            all_pages_list.extend(self.collect_page_links())
            time.sleep(1)
            self.click_next_page(page)

        all_pages_list.extend(self.collect_page_links())

        for url in all_pages_list:
           time.sleep(1)
           #TODO: use a try and except statement to catch the timeout exception. 
           try:
               self.driver.get(url)
               time.sleep(2)
           except TimeoutException:
               time.sleep(4)
               self.driver.get(url) 
               
           self.get_information_from_page()
        
        


        
       # new syntax for driver.find_elements(By.XPATH, "xpath string")
if __name__ == '__main__':     
    new_scraper = MetaCriticScraper("https://www.metacritic.com/")
    # new_scraper.choose_game_category()
    # new_scraper.choose_genre()
    # new_scraper.collect_page_links()
    # new_scraper.get_information_from_page()
    # new_scraper.click_next_page()
    # new_scraper.collect_number_of_pages()
    # new_scraper.click_next_page_3()
    # new_scraper.last_page()
    # new_scraper.process_page_links()

    # Timing how long it takes to scrape from 100 pages 
    t1_start = perf_counter()
    new_scraper.sample_scraper()
    t1_stop = perf_counter()
    print(f'Total elapsed time {round(t1_stop - t1_start)} seconds')

# Current stats(1/01/2022): 100 pages in 226 seconds (2 minutes, 4 seconds.)
# Current stats(27/01/2022): 500 pages in 2828 seconds (47 minutes, 8 seconds)
# Current stats (3/02/2022): 524 pages in 1742 seconds (29 minutes)
# Current stats (14/02/2022): 500 pages in 3145 seconds (52 minutes, 24 seconds)
# Current stats (15/02/2022): 524 pages in 2481 seconds (41 minutes, 21 seconds)
# Current stats (15/02/2022, 22:46pm): 524 pages in 2697 seconds (44 minutes, 57 seconds)

