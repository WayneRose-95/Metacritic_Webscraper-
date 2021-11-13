from pprint import pprint
import time
import selenium
from selenium import webdriver

class MetaCriticScraper:
    def __init__ (self, game_urls, driver = webdriver.Chrome(), webpage = "https://www.metacritic.com/browse/games/genre/date/fighting/all"):
        self.driver = driver
        self.webpage = webpage
        self.game_urls = game_urls
        driver.get(self.webpage)
    
    
   

    def accept_cookies(self): 
        time.sleep(4)
        # cookies_iframe = self.driver.find_element_by_id("onetrust-button-group")
        # self.driver.switch_to.frame(cookies_iframe)
        accept_cookies = self.driver.find_element_by_xpath('//button[@id="onetrust-accept-btn-handler"]')
        accept_cookies.click()
        # self.driver.switch_to.default_content()

   
    def game_list_urls(self,xpath_to_get_links): 
        game_container = self.driver.find_elements_by_xpath(xpath_to_get_links)
        # game_list = game_container.find_elements_by_xpath('//a')
        self.game_urls = []

        for item in game_container:
            link = item.get_attribute('href')
            self.game_urls.append(link)
        print(self.game_urls)

      
    #TODO: Do the keys need to go into a list???
    def game_details(self):
        game_details_dict_list = []
        url_counter = 0
        for url in self.game_urls:
            self.driver.get(url)
            url_counter += 1
            game_details_dict = {f'Game{url_counter}':{'Title' : [], 'Platform' : [], 'Release Date' : [], 'MetaCritic Score' : [], 'Description' : []}}

            #TODO: Compact this code, it's doing the same thing too many times. 
            #TODO: Generic function takes xpath and the dictionary key, maybe the 'no details' text, 
            #      and the element 
            try: 
                title_elem = self.driver.find_element_by_xpath('//*[@class="hover_none"]')
                game_details_dict[f'Game{url_counter}']['Title'].append(title_elem.text)
            except:
                game_details_dict[f'Game{url_counter}']['Title'].append("No Title Found")
              
            try: 
                platform_elem = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/span') #class="css-8rvu8h-AttributeLabel ep4jli0"
                game_details_dict[f'Game{url_counter}']['Platform'].append(platform_elem.text)
            except:
                game_details_dict[f'Game{url_counter}']['Platform'].append("Null")
            
            try: 
                release_date_elem = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/div[1]/div[1]/div[3]/ul/li[2]/span[2]') #Release Date Xpath class = "data"
                game_details_dict[f'Game{url_counter}']['Release Date'].append(release_date_elem.text)
            except:
                game_details_dict[f'Game{url_counter}']['Release Date'].append("Null")
            

            try: 
                Metacritic_Score_Elem = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/a/div') # class = metascore_w 
                game_details_dict[f'Game{url_counter}']['MetaCritic Score'].append(Metacritic_Score_Elem.text)
            except: 
                game_details_dict[f'Game{url_counter}']['MetaCritic Score'].append("Null")

            try: 
                description_elem = self.driver.find_element_by_xpath('//li[@class="summary_detail product_summary"]')
                game_details_dict[f'Game{url_counter}']['Description'].append(description_elem.text)
            except:
                game_details_dict[f'Game{url_counter}']['Description'].append("No description found")
            

        
            game_details_dict_list.append(game_details_dict)
        print(f'urls_visited:{url_counter}')
        print(game_details_dict_list,sep="\n")
            


game_search = MetaCriticScraper('//a[@class="title"]')
game_search.accept_cookies()
game_search.game_list_urls('//a[@class="title"]') 
# game_search.click_into_url()
game_search.game_details()
# Xpath for links:  '//a[@class="title"]'

