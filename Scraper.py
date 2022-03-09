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
import os 
import urllib.request



#%%
class Scraper: 
    '''
    A class which houses all generic methods for webscraping 

    Methods to Add: 

    1. Save_Json 

    2. Collect Page Links 

    3. Collect Number of Pages 

    4. Manipulate Filters Method (if applicable)

    5. Click Next Page? 


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
            cookies_iframe = self.driver.find_element(By.ID, iframe) 
            self.driver.switch_to.frame(cookies_iframe)
            accept_cookies = self.driver.find_element(By.XPATH, cookies_button_xpath)
            accept_cookies.click()
           
        except NoSuchFrameException: # If it is not within a frame then find the xpath and proceed click it. 
            print('No iframe found')
            accept_cookies = self.driver.find_element(By.XPATH, cookies_button_xpath)
            accept_cookies.click()
            print('The accept cookies button has been clicked')
        time.sleep(2)
        return True  
    
    def find_search_bar_then_pass_input_into_search_bar(self, search_bar_xpath, text):
        try:
            
            search_bar_element = self.driver.find_element(By.XPATH, search_bar_xpath)
            search_bar_element.click()
        except:
            print('no search bar found')


        if search_bar_element:
            search_bar_element.send_keys(text)
            search_bar_element.send_keys(Keys.ENTER)
        else:
            raise Exception('Text failed')
        
            
        return search_bar_element, text

    def infinite_scroll_down_page(self):

        SCROLL_PAUSE_TIME = 5

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    def collect_page_links(self, container_xpath : str, attribute = 'href' or 'src'):
        #TODO: Try find_elements(By.CSS_SELECTOR)
        page_container = self.driver.find_elements(By.XPATH, container_xpath)
        page_links_list = []

        page_counter = 0 
    
        for url in page_container:
            link_to_page = url.get_attribute(attribute)
            page_links_list.append(link_to_page)
            page_counter += 1
       
        print(page_links_list)
        print(f'Pages visited: {len(page_links_list)}')
        return page_links_list
        
        
    def find_container(self, container_xpath):

        try: 
            container = self.driver.find_element(By.XPATH, container_xpath)
            print(container)
        except:
            raise Exception('There was no element')

    

    def _save_image(self, sub_category_name: str, image_xpath):
        """
        Method to download every product image (jpg format) to local and/or s3_bucket locations.
    
        Parameters: 
            sub_category_name (str): parameter determined within the get_product_information method.
        """
        image_category = sub_category_name
        image_name = f'{sub_category_name}-image'
        src_list = self.driver.find_elements(By.XPATH, image_xpath).text()
        # //*[@id="product-gallery"]/div[2]/div[2]/div[2]/img
        
        image_path = f'images/{image_category}'
        if not os.path.exists(image_path):
            os.makedirs(image_path)         
        for i,src in enumerate(src_list[:-1],1):   
            urllib.request.urlretrieve(src, f'{image_path}/{image_name}.{i}.jpg')

#%%

if __name__ == "__main__":
    bot = Scraper()
    # zoopla page = "https://www.zoopla.co.uk/"    
    bot.land_first_page("https://www.metacritic.com")

#%%
    # Xpaths from cbr.com
    # '/html/body/div[3]/div[1]/div[1]/div/button[2]', 
    # '//div[@class="ConsentManager__Overlay-np32r2-0 gDTHbw"]'

    # Xpaths from zoopla.co.uk

    bot.accept_cookies('//button[@id="save"]', 
                        'gdpr-consent-notice')
#%%
    bot.find_search_bar_then_pass_input_into_search_bar(
        '//*[@id="header-location"]',
        'London'
    )
#%%
    bot.collect_page_links('//a[@class="title"]', 'href')

#%%
    
#%%
    bot.infinite_scroll_down_page()    
#%% 
    # Xpath from Wikipedia 
    bot.find_container('//div[@id="bodyContent"]')
 

# %%
    #TODO: Solve the error with the _save_image method. 
    # Directory is created, but images are not saved inside. 

    bot.find_container('//div[@class="css-p1r19z-Primary e16evaer17"]')
    bot._save_image('Londonerry Houses', '//li[@class="css-1dqywv5-Slide e16xseoz1"]')
# %%
