import csv
from io import TextIOWrapper
import unittest
from xmlrpc.client import Boolean 
from Metacritic_Webscraper_Latest import MetaCriticScraper
import time 
import tracemalloc 

'''
Unittest Suite: 

Sample Unittest Suite for the current version 
of the Metacritic_Webscraper_Latest.py file (22/02/2022)

Things to add (22/02/2022):

Some of the things to add do NOT have methods associated with them yet

1. Add a test to determine the file format for the scraper outputs. 
   

2. Add a test to determine the robustness of the accept_cookies method

3. Add a test to see if the save_image method works as intended 
   

4. Add a test to determine the validity of the images saved. 
   This can be done using the ImageHash library 
   

'''
tracemalloc.start()

class ASOS_Webscraper_Tests(unittest.TestCase):

    def setUp(self):
        self.scraper = MetaCriticScraper("https://www.metacritic.com/")
        time.sleep(5)
    
    def test_get_information_from_page(self):
        '''
        Unittest to ensure that information is being collected 
        from variety of pages 

        Returns: An instance of a dict if True

        Types of pages tested: 
        Pages within the Games section of the website
        Pages with an 'expand' button under their descriptions 
        Pages with varying Metascores: good, average and bad

        '''
        # Good game root = "https://www.metacritic.com/game/xbox/halo-combat-evolved"
        # Bad game root = "https://www.metacritic.com/game/gamecube/charlies-angels"
        # Mixed game root = "https://www.metacritic.com/game/pc/white-shadows
        test_urls = ["https://www.metacritic.com/game/gamecube/charlies-angels",
                    "https://www.metacritic.com/game/xbox/halo-combat-evolved",
                    "https://www.metacritic.com/game/pc/white-shadows"]

        # Iterate through each url in the list 
        # to see if it generates a dictionary output          
        for url in test_urls:
            self.scraper.driver.get(url)
            time.sleep(2)
            test_input = self.scraper.get_information_from_page()
            self.assertIsInstance(test_input, dict)

    tracemalloc.reset_peak()

    def test_collect_number_of_pages(self):
        '''
        Unittest to determine the maximum number of pages in 
        each section of the website 

        Returns:
        An Integer to be as a value in iterating through each of the
        pages on the website. 

        The test uses the method on a page with page numbers on the website, 
        and tries to match the expected_output variable with the variable 
        that the method returns. 
        '''
        #TODO: find a way to pass in multiple urls to test the method

        test_page = "https://www.metacritic.com/browse/games/genre/date/racing/all"
        
        self.scraper.driver.get(test_page)
        test_input = self.scraper.collect_number_of_pages()
      
        expected_output = 17
        
        self.assertEqual(expected_output, test_input)

    tracemalloc.reset_peak()

    def test_collect_page_links(self):
        test_page = "https://www.metacritic.com/browse/albums/genre/date/electronic"
        self.scraper.driver.get(test_page)
        test_input = self.scraper.collect_page_links()

        self.assertIsInstance(test_input, list)
        self.assertEqual(len(test_input), 100)
    
    # def test_accept_cookies(self):
        #TODO: Write a unittest for this method 
        pass

    def test_save_json(self):
        #TODO: Debug this error: 
        # TypeError: Object of type TextIOWrapper is not JSON serializable
        with open("test_scraper_output.txt", 'r', encoding='utf-8-sig') as test_file:
            content_dict = []
            contents = test_file.readlines()
            for content in contents: 
                content_dict.append(eval(content))
            print(content[:5])
            print(type(content))
            test_json = self.scraper.save_json(content_dict, sub_category_name='fighting_games')
            
            print(test_json)
            self.assertTrue(test_json, True)
    
    # def test_save_csv(self):
    # #TODO: Debug this error: 
   
    #     with open("test_scraper_output.txt", 'r') as test_file:
    #         print(type(test_file))
    #         headers = ['Title', 
    #                        'Platform', 
    #                        'Release Date', 
    #                        'Metacritic Score', 
    #                        'User Score', 
    #                        'Description']
    #         test_csv = self.scraper._save_csv(test_file,  headers, sub_category_name='fighting_games')
            

    #         self.assertIsInstance(test_csv, TextIOWrapper)

    def tearDown(self):
        self.scraper.driver.quit()
        
unittest.main(argv=[''], verbosity=2, exit=False)