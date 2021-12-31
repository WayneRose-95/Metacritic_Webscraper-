import time 
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
        self.root = "https://www.metacritic.com/game/xbox/halo-combat-evolved"
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
        choose_action_genre = self.driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div[2]/div[2]/div[1]/div/div/div/ul/li[1]/a').get_attribute("href")
        action_genre_url = print(choose_action_genre)
        self.driver.get(choose_action_genre)
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

    def click_next_page(self):
        next_page_element = self.driver.find_elements(By.XPATH, '//li[@class="page_num"]')

        page_list = []

        # This line isn't doing anything. Maybe make it 
        base_url = 'https://www.metacritic.com/browse/games/genre/date/action/all?page=1'

        for element in next_page_element:
            link_to_next_page = element.get_attribute('href')
            page_list.append(link_to_next_page)

        print(page_list)
        
        return page_list
         

    #TODO: work on this method after completing the links 

    def get_information_from_page(self):

        
   
        #TODO: This could be a staticmethod? 
        for key,xpath in self.xpaths_dict.items():
            
            try:
                
                web_element = self.driver.find_element(By.XPATH, xpath) 
                self.information_dict[key] = web_element.text
                

            except:
                
                self.information_dict[key] = 'Null'

        print(self.information_dict)
        return self.information_dict


    #TODO: make a method which makes the scraper go to these links
    # This link should help: 
    # https://pretagteam.com/question/loop-through-links-and-scrape-data-from-resulting-pages-using-selenium-python-duplicate

    def process_page_links(self):
        
    
        for url in self.collect_page_links():
            self.driver.get(url)
           
       

    def sample_scraper(self):
        # Goes to Games > Games Home > 'Search by Genre': Action > Scrapes the first page. 
        self.choose_game_category()
        self.choose_genre()

        for url in self.collect_page_links():
           self.driver.get(url)
           self.get_information_from_page()
        
        
    
        
        
       # new syntax for driver.find_elements(By.XPATH, "xpath string")
      
new_scraper = MetaCriticScraper()
# new_scraper.choose_game_category()
# new_scraper.choose_genre()
# new_scraper.collect_page_links()
new_scraper.get_information_from_page()
# new_scraper.sample_scraper()
# new_scraper.click_next_page()

    
