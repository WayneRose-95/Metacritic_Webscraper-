import unittest 
from Metacritic_Webscraper_Latest import MetaCriticScraper
import time 


class ASOS_Webscraper_Tests(unittest.TestCase):

    def setUp(self):
        self.scraper = MetaCriticScraper("https://www.metacritic.com/")
        time.sleep(5)
    
    def test_get_information_from_page(self):
        '''
        Unittset to ensure that information is being collected 
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


    def test_collect_number_of_pages(self):

        test_page = "https://www.metacritic.com/browse/games/genre/date/fighting/all"

        self.scraper.driver.get(test_page)
        expected_output = 6
        test_input = self.scraper.collect_number_of_pages()
        self.assertEqual(expected_output, test_input)

unittest.main(argv=[''], verbosity=2, exit=False)