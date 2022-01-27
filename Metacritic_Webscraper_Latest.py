import time 
from time import perf_counter
import selenium
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

#TODO: Go for a sample scrape on a webpage. Output a dictionary. 

class MetaCriticScraper: 

    def __init__(self, driver = webdriver.Chrome()):
        self.driver = driver 
        # Temporary change in root to debug collecting information from the page. Original root =  "https://www.metacritic.com/"
        # Good game root = "https://www.metacritic.com/game/xbox/halo-combat-evolved"
        # Bad game root = "https://www.metacritic.com/game/gamecube/charlies-angels"
        # Mixed game root = "https://www.metacritic.com/game/pc/white-shadows"
        # Sample page root = "https://www.metacritic.com/browse/games/genre/date/fighting/all"
        # Sample page root short description = "https://www.metacritic.com/game/ios/the-king-of-fighters-97"
        self.root = "https://www.metacritic.com/"
        driver.get(self.root)
        self.accept_cookies()
        self.page_counter = 0

        self.xpaths_dict = {'Title': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/a/h1', 
                   'Platform': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/span', 
                   'Release_Date': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[3]/ul/li[2]/span[2]',
                   'MetaCritic_Score': '//a[@class="metascore_anchor"]/div', 
                   'User_Score': '//div[@class="userscore_wrap feature_userscore"]/a/div',
                   'Developer': '//li[@class="summary_detail developer"]/span[2]/a', 
                   'Description': '//li[@class="summary_detail product_summary"]' } 

        self.information_dict =  {}
        

    def accept_cookies(self): 
        time.sleep(4)
        accept_cookies = self.driver.find_element_by_xpath('//button[@id="onetrust-accept-btn-handler"]')
        accept_cookies.click()
    
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
        action_genre_url = print(choose_fighting_genre)
        self.driver.get(choose_fighting_genre)
        return action_genre_url
        
    #TODO: make a method which collects the links from each of the items on the page. 

    
    def collect_page_links(self):
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

        # iterate over pages 2 to 7.
        #TODO: find a way to generalise this code for all pages on the website. Maybe make another method to check the last page? 
    
        next_page_element = self.driver.find_element(By.XPATH, f'//*[@id="main_content"]/div[1]/div[2]/div/div[1]/div/div[9]/div/div/div[2]/ul/li[{page}]/a')
        next_page_url = next_page_element.get_attribute('href')
        self.driver.get(next_page_url)
        print(next_page_url)
        print('navigating to next page')

        return next_page_url
         
    def last_page(self):
        last_page_element = self.driver.find_element(By.XPATH, '//li[@class="page last_page"]/a' )
        # '//*[@id="main_content"]/div[1]/div[2]/div/div[1]/div/div[9]/div/div/div[2]/ul/li[6]'
        last_page_url = last_page_element.get_attribute('href')
        self.driver.get(last_page_url)
        return last_page_url 

    

    def get_information_from_page(self):   
        
    
        #TODO: This could be a staticmethod? 
        for key,xpath in self.xpaths_dict.items():
           
            try:
                if key == 'Description':
                    collapse_button = self.driver.find_element(By.XPATH, '//span[@class="toggle_expand_collapse toggle_expand"]')
                    if collapse_button:
                        collapse_button.click()
                        expanded_description = self.driver.find_element(By.XPATH, '//span[@class="blurb blurb_expanded"]')
                        self.information_dict[key] = expanded_description.text
                    else:
                         web_element = self.driver.find_element(By.XPATH, xpath) 
                         self.information_dict[key] = web_element.text
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

    def process_page_links(self):
        

        for url in self.collect_page_links():
            self.driver.get(url)
         
       

    def sample_scraper(self):
        # Goes to Games > Games Home > 'Search by Genre': Fighting > Scrapes the first page. 
        self.choose_game_category()
        self.choose_genre()

        root_page = "https://www.metacritic.com/game"

        all_pages_list = []

        for page in range(2,7):
            all_pages_list.extend(self.collect_page_links())
            time.sleep(1)
            self.click_next_page(page)


        for url in all_pages_list:
           self.driver.get(url)
           time.sleep(2)
           self.get_information_from_page()
        
        
        


        
       # new syntax for driver.find_elements(By.XPATH, "xpath string")
      
new_scraper = MetaCriticScraper()
# new_scraper.choose_game_category()
# new_scraper.choose_genre()
# new_scraper.collect_page_links()
# new_scraper.get_information_from_page()
# new_scraper.click_next_page()
# new_scraper.last_page()
# new_scraper.process_page_links()

# Timing how long it takes to scrape from 100 pages 
t1_start = perf_counter()
new_scraper.sample_scraper()
t1_stop = perf_counter()
print(f'Total elapsed time {round(t1_stop - t1_start)} seconds')

# Current stats(1/01/2022): 100 pages in 226 seconds (2 minutes, 4 seconds.)
# Current stats(27/01/2022): 500 pages in 2828 seconds (47 minutes, 8 seconds)
