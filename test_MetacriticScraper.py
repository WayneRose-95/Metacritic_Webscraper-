import unittest 
from Metacritic_Webscraper_Latest import MetaCriticScraper
import time 
import tracemalloc 

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

    def tearDown(self):
        self.scraper.driver.quit()
        
unittest.main(argv=[''], verbosity=2, exit=False)