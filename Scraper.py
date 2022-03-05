#%%
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait

#%%
class Scraper: 
    '''
    A class which houses all generic methods for webscraping 

    '''
    def __init__(self, options=None):

        if options:
            self.driver = Chrome(ChromeDriverManager().install(), options=Options)
        else:
            self.driver = Chrome(ChromeDriverManager().install())
    
    def land_first_page(self, page_url):
        home_page = self.driver.get(page_url)
        return home_page
    
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
    bot.land_first_page("https://en.wikipedia.org/wiki/Main_Page")

#%%
    bot.find_search_bar('//input[@class="vector-search-box-input"]')
#%%
    bot.input_something_into_search_bar('Rick and Morty')

    
#%%    
    bot.find_container('//div[@id="bodyContent"]')
 


# %%
