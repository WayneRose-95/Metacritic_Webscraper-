import urllib.request
import time 
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class MetaCriticScraper: 

    def __init__(self, driver = webdriver.Chrome()):
        self.driver = driver 
        self.root = "https://www.metacritic.com/"
        driver.get(self.root)
        self.accept_cookies()


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

    # def collect_page_links(self):
    #     page_links_list = []

    #     for url in page_links_list:
    #         self.driver.find_elements(By.XPATH, '')


    #TODO:  make a method which collects the information from the page

    #TODO: collect xpaths from the pages. Store in the init? 
    # xpaths dict = {'Title': '//*[@class="hover_none"]', 
    #                'Platform': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/span', 
    #                'Release_Date': '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[3]/ul/li[2]/span[2]',
    #                'MetaCritic_Score': '//*[@id="main"]/div/div[1]/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/a/div',
    #                'User_Score': '//*[@id="main"]/div/div[1]/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/a/div'
    #                'Description': ''//li[@class="summary_detail product_summary"]'' } 

    # new syntax for driver.find_elements(By.XPATH, "xpath string")
      
new_scraper = MetaCriticScraper()
new_scraper.choose_game_category()
new_scraper.choose_genre()


    
