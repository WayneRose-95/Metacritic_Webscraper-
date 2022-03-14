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

    2. Manipulate Filters Method (if applicable)

    3. Click Next Page? 

    4. Debug the Save Images Error


    '''
    def __init__(self, options=None):

        if options:
            self.driver = Chrome(ChromeDriverManager().install(), options=Options())
        else:
            self.driver = Chrome(ChromeDriverManager().install())
    
    def land_first_page(self, page_url : str):
        home_page = self.driver.get(page_url)
        return home_page

    def accept_cookies(self, cookies_button_xpath : str, iframe=None): 
         
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
    
    def find_search_bar_then_pass_input_into_search_bar(self, search_bar_xpath : str, text : str):
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


    def extract_the_page_links(self, container_xpath : str, attribute : str = 'href' or 'src'):
        # find the container with the links
        page_container = self.driver.find_elements(By.XPATH, container_xpath)
        page_links_list = []

        page_counter = 0 
        
        # iterate through these links 
        for url in page_container:
            link_to_page = url.get_attribute(attribute)
            page_links_list.append(link_to_page)
            page_counter += 1

        # For a sanity check, print the list of links and the number of pages 

        print(page_links_list)
        print(f'Pages visited: {len(page_links_list)}')
        return page_links_list


    def collect_number_of_pages(self, last_page_number : str ):
        try:

            last_page_number_element = (self.driver.find_element(By.CSS_SELECTOR, last_page_number).text)
            print(last_page_number_element)
            print(f"Max Page = {last_page_number_element}..")
            last_page_number = int(last_page_number_element)

        except NoSuchElementException:
            print('Element not found. Exiting...')

        return last_page_number
               
        
    def find_container(self, container_xpath : str):

        try: 
            container = self.driver.find_element(By.XPATH, container_xpath)
            print(container)
        except:
            raise Exception('There was no element')

    def apply_filter_list(self, filter_container_xpath : str , filter_button=None):

        if filter_button:
            filter_button = self.driver.find_element(By.XPATH, filter_button)
            filter_button.click()

             # filter_container = self.extract_the_page_links('//ul[@class="dropdown dropdown_open"]//li/a', 'href')
            filter_container = self.driver.find_elements(By.XPATH, filter_container_xpath)
            filter_container_list = []

            for url in filter_container:
                link_to_page = url.get_attribute('href')
                filter_container_list.append(link_to_page)
            print(filter_container_list)
        else:
        
            # filter_container = self.extract_the_page_links('//ul[@class="dropdown dropdown_open"]//li/a', 'href')
            filter_container = self.driver.find_elements(By.XPATH, filter_container_xpath)
            filter_container_list = []

            for url in filter_container:
                link_to_page = url.get_attribute('href')
                filter_container_list.append(link_to_page)

            print(filter_container_list) 
            return filter_container_list
     
    


    def _save_image(self, sub_category_name: str, image_xpath : str):
        """
        Method to download every product image (jpg format) to local and/or s3_bucket locations.
    
        Parameters: 
            sub_category_name (str): parameter determined within the get_product_information method.
        """
        image_category = sub_category_name
        image_name = f'{sub_category_name}-image'
        src_list = self.driver.find_elements(By.XPATH, image_xpath)
        print(src_list)
        # //*[@id="product-gallery"]/div[2]/div[2]/div[2]/img
        
        image_path = f'images/{image_category}'
        if not os.path.exists(image_path):
            os.makedirs(image_path)         
        for i,src in enumerate(src_list[:-1],1):
            print(src)   
            urllib.request.urlretrieve(src, f'{image_path}/{image_name}.{i}.jpg')

    #TODO: Making another method to debug how to save an image. 
    # Need to test it out without getting an Attribute Error....
    # def download_image(self):

    #     image_name = self.driver.find_element(By.XPATH, '//img[@class="product_image large_image"]')
    #     src_image_name = image_name.get_attribute('src')
    #     alt_image_name = image_name.get_attribute('alt')
    #     print(src_image_name)
    #     print(alt_image_name)

#%%

if __name__ == "__main__":
    bot = Scraper()

