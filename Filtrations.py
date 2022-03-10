# This file will include a class 
# This class will be responsibile to interact with the filters of a website
# The filtration class will be applied to the Scraper/Metacritic Class
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import NoSuchFrameException
from Scraper import Scraper
import time 


class WebsiteFiltration(Scraper):
    '''
    A class which applies filters to the website being scraped. 
    To be updated with future methods? 

    '''
    def __init__(self, options=None):
        
        super().__init__(
            options
        )

        if options:
            self.driver = Chrome(ChromeDriverManager().install(), options=Options())
        else:
            self.driver = Chrome(ChromeDriverManager().install())

    def apply_filter_list(self):
        filter_button = self.driver.find_element(By.XPATH, '//div[@[@class="mcmenu dropdown style2 genre"]/button')
        filter_button.click()

        filter_list_container = self.driver.find_element(By.XPATH, '//ul[@class="dropdown dropdown_open"]')
        list_of_elements = filter_list_container.find_elements(By.XPATH, '//li[*]').get_attribute('href')

        print(list_of_elements)


        return list_of_elements    

           

 


