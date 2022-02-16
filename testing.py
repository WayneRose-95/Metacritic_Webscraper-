
import unittest 
import time 
from Metacritic_Webscraper_Latest import MetaCriticScraper

'''
Sample Unittest Suite for Metacritic_Webscraper_Latest. 
Main code was last edited on (15/02/2022)
Please update the tests if any logic in the main code changes

GOALS: 

1. Implement the Hypothesis module to thoroughly test methods 
2. Make a Python script with constants, which can be imported into this unittest script.
3. Add if __name__ == __main__: to the bottom of Metacritic_Webscraper_Latest.py
''' 
class MetaCriticScaper_Tests(unittest.TestCase):

    def setUp(self):
        self.scraper = MetaCriticScraper()
        time.sleep(4)
    
    # TESTING METHODS GOES HERE
    # Methods to test: 
    #TODO: add if __name__ == __main__: to the bottom of the code before running test suite

    # 1. test_collect_page_links(self):

    def test_collect_page_links(self):
        test_url = "https://www.metacritic.com/browse/games/genre/date/action/all"
        self.scraper.driver.get(test_url)
        list_of_links = self.scraper.collect_page_links()
        self.assertIsInstance = (list_of_links, list)


    # 2. test_collect_number_of_pages(self):

    def test_collect_number_of_pages(self):
        test_url = "https://www.metacritic.com/browse/albums/genre/date/jazz"
        self.scraper.driver.get(test_url)
        test_value = self.scraper.collect_number_of_pages()
        expected_value = 5
        self.assertEqual(expected_value, test_value)

    # 3. test_get_information_from_page(self, webpage):

    def test_get_information_from_page(self):
        test_url = "https://www.metacritic.com/game/pc/mortal-kombat-komplete-edition"
        self.scraper.driver.get(test_url)
        output_dictionary = self.scraper.get_information_from_page()
        self.assertIsInstance(output_dictionary, dict)



    # 4. test_click_next_page(self):

    def test_click_next_page(self):
        test_url = "https://www.metacritic.com/browse/games/genre/date/action/all"
        self.scraper.driver.get(test_url)
        test_output = self.scraper.click_next_page(4)
        expected_output = "https://www.metacritic.com/browse/games/genre/date/action/all?page=3"
        self.assertEqual(test_output, expected_output)
        
    #TODO: Implement save_to_(file_format) method in main code
    # 5. test_save_to_(file_format)(self):


    # 6. test_choose_game_category(self):
    def test_choose_game_category(self):
        test_url = "https://www.metacritic.com"
        self.scraper.driver.get(test_url)
        test_output = self.scraper.choose_game_category()
        self.assertIsInstance(test_output, str)


    # 7. test_choose_genre(self):

    def test_choose_genre(self):
        test_url = "https://www.metacritic.com/game"
        self.scraper.driver.get(test_url)
        test_output = self.scraper.choose_genre()
        self.assertIsInstance(test_output, str)

    #TODO: Improve the robustness of click_accept_cookies method in main code
    # 8. test_click_accept_cookies(self):

    def tearDown(self):
        self.scraper.driver.quit()

unittest.main(argv=[''], verbosity=2, exit=False)