#%%
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
# from selenium.webdriver.support.ui import WebDriverWait
import time 



#%%
class Scraper: 
    '''
    A class which houses all generic methods for webscraping 

    '''
    def __init__(self, options=None):

        if options:
            self.driver = Chrome(ChromeDriverManager().install(), options=Options())
        else:
            self.driver = Chrome(ChromeDriverManager().install())
    
    def land_first_page(self, page_url):
        home_page = self.driver.get(page_url)
        return home_page

    def accept_cookies(self, cookies_button_xpath, iframe=None): 
        #TODO: Create a unittest for this method 
        time.sleep(4)
        try: # To find if the accept cookies button is within a frame 
            self.driver.switch_to.frame(iframe)
           
        except NoSuchFrameException: # If it is not within a frame then find the xpath and proceed click it. 
            print('No iframe found')
            accept_cookies = self.driver.find_element(By.XPATH, cookies_button_xpath)
            accept_cookies.click()
        time.sleep(2)
        return True  
    
    def find_search_bar(self, search_bar_xpath):
        try:
            
            search_bar_element = self.driver.find_element(By.XPATH, search_bar_xpath)
            search_bar_element.click()
        except:
            print('no search bar found')
        
        return search_bar_element

       
    def input_something_into_search_bar(self, text):
        search_bar = self.find_search_bar('//input[@class="vector-search-box-input"]')

        if search_bar:
            search_bar.send_keys(text)
            search_bar.send_keys(Keys.ENTER)
        
    def find_container(self, container_xpath):

        try: 
            container = self.driver.find_element(By.XPATH, container_xpath)
            print(container)
        except:
            raise Exception('There was no element')

#%%

if __name__ == "__main__":
    bot = Scraper()    
    bot.land_first_page("https://www.cbr.com/")

#%%

    bot.accept_cookies('/html/body/div[3]/div[1]/div[1]/div/button[2]')
#%%
    # Xpaths from Wikipedia 
    bot.find_search_bar('//input[@class="vector-search-box-input"]', '//div[@class="ConsentManager__Overlay-np32r2-0 gDTHbw"]')
#%%

    bot.input_something_into_search_bar('Rick and Morty')

    
#%% 
    # Xpath from Wikipedia 
    bot.find_container('//div[@id="bodyContent"]')
 


# %%
