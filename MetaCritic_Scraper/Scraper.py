#%%
from xmlrpc.client import Boolean
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import SSLError
from typing import Optional
import time
import urllib.request
import boto3
import tempfile
import os 
import shutil 
import uuid
import json
from json import JSONEncoder
import itertools 
import requests
import certifi


#%%
class Scraper: 

    '''
    A class which houses all generic methods for webscraping 

    Methods to Add: 

    1. Upload_to_S3 


    '''
    
    increasing_id = itertools.count()
    def __init__(self):

        chrome_options = ChromeOptions()
        #chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        self.driver = Chrome(options=chrome_options)  
        self.id = next(self.increasing_id)   
    
    def land_first_page(self, page_url : str):
        home_page = self.driver.get(page_url)
        return home_page

    def accept_cookies(self, cookies_button_xpath : str, iframe: Optional[str]=None): 
         
        time.sleep(4)
        try:
            if iframe: # To find if the accept cookies button is within a frame
                cookies_iframe = self.driver.find_element(By.ID, iframe) 
                self.driver.switch_to.frame(cookies_iframe)
                accept_cookies_button = (
                WebDriverWait(self.driver, 0.5)
                .until(EC.presence_of_element_located((
                    By.XPATH, cookies_button_xpath))
                )
            )
                accept_cookies_button.click()
            else:
                accept_cookies_button = (
                WebDriverWait(self.driver, 0.5)
                .until(EC.presence_of_element_located((
                    By.XPATH, cookies_button_xpath))
                )
            )
            accept_cookies_button.click()
            print('The accept cookies button has been clicked')

        except NoSuchFrameException: # If it is not within a frame then find the xpath and proceed click it. 
            print('No iframe found')
            accept_cookies = self.driver.find_element(By.XPATH, cookies_button_xpath)
            accept_cookies.click()
            print('The accept cookies button has been clicked')
        return True  
    
    def manipulate_search_bar(self, search_bar_xpath : str, text : str):

        # Find the element corresponding to the search bar
        try:
            search_bar_element = (
                WebDriverWait(self.driver, 0.5)
                .until(EC.presence_of_element_located(
                    (By.XPATH, search_bar_xpath)
                    )
                )
            )
        # Click on the element for the search bar 
            search_bar_element.click()
        except:
            # If it is not present, close the window. 
            print('no search bar found')
            self.driver.quit()

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


    def extract_the_page_links(
        self, 
        container_xpath : str, 
        attribute : str = 'href' or 'src' or 'alt'
    ):
        
        temp = True 
        while temp is True:
            try:
        # find the container with the links
                page_container = (
                    WebDriverWait(self.driver, 0.5)
                    .until(EC.presence_of_all_elements_located(
                        (By.XPATH, container_xpath)
                        )
                    )
                )
                temp = False 
            except Exception:
                print('entered exception')
                continue
  
        page_links_list = []
        page_counter = 0 
        
        # iterate through these links 
        for url in page_container:
            link_to_page = url.get_attribute(attribute)
            page_links_list.append(link_to_page)
            page_counter += 1

        # For a sanity check, print the list of links and the number of pages 

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
     
    def download_image(self, image_xpath, sub_category_name: str):
        image_category = sub_category_name
        image_name = f'{sub_category_name}-image'
        src_list = self.extract_the_page_links(image_xpath,'src')
        # //*[@id="product-gallery"]/div[2]/div[2]/div[2]/img
        
        
        try:
            image_path = f'images/{image_category}'
            if not os.path.exists(image_path):
                os.makedirs(image_path)         
            for i,src in enumerate(src_list):   
                urllib.request.urlretrieve(src, f'{image_path}/{image_name}.{i}.jpg') 
                
        except SSLError:
            for url in src_list:
                url.replace("https", "http")
                image_path = f'images/{image_category}'
            if not os.path.exists(image_path):
                os.makedirs(image_path)         
            for i,src in enumerate(src_list):   
                urllib.request.urlretrieve(src, f'{image_path}/{image_name}.{i}.jpg') 



    def set_s3_connection(self):
        """
        Method to create service client connection to the S3 AWS services.
        Returns:
            self.s3_client: variable name for the s3 client connection 
        """
        self.s3_client = boto3.client('s3')
        return self.s3_client

    #TODO: Scraper only saves one image without a directory.
    # Refactor this so that the image saves within a directory 
    # Then refactor it to save multiple images inside a directory. 

    def save_image_links(self, image_name_xpath, image_src_xpath):
        '''
        Method to save image srcs inside a dictionary with unique IDs. 

        Returns:
        self.image_dict = A Dictionary which contains data on the image. 
        '''
        self.image_dict = {
            'ID': [],
            'Friendly_ID': [],
            'Image_Name': [],
            'Image_Link': []
        }

        # Find all of the srcs and alt tags from the page 
        image_names = self.extract_the_page_links(image_name_xpath, 'alt')
        image_links = self.extract_the_page_links(image_src_xpath, 'src')

        #TODO: How to split elements from a list? 
        
        # Append the split src urls to a new list to populate Friendly_ID field 
            

        self.image_xpath_dict = {
            'ID': str(uuid.uuid4()),
            'Friendly_ID': f"{self.increasing_id}",
            'Image_Name': f'{image_names}',
            'Image_Link' :f'{image_links}'
        }
       
    
        for key,value in self.image_xpath_dict.items():
            try:   
                self.image_dict[key] = value
            except:
                self.image_dict[key] = 'Null'
        

        if not os.path.exists('images'):
            os.makedirs('images')
            try:
                for i,link in enumerate(image_names):
                    with open(f'images/{link}_{i}.jpg', "wb") as file:
                        img = self.driver.find_element(By.XPATH, image_src_xpath)
                        time.sleep(3)
                        file.write(img.screenshot_as_png)
                        time.sleep(3)
            except:
                print('There was an error')
       
       
        print(self.image_dict)
        return self.image_dict

    def save_json(self, all_products_dictionary, sub_category_name):
        file_to_convert = all_products_dictionary
        file_name = f'{sub_category_name}-details.json'

        if not os.path.exists('json-files'):
            os.makedirs('json-files')
        with open(f'json-files/{file_name}', mode='a+', encoding='utf-8-sig') as f:
            json.dump(file_to_convert, f, indent=4, ensure_ascii=False) 
            f.write('\n')
        return True
     
                 
    

#%%

if __name__ == "__main__":
    bot = Scraper()

