import unittest

from Metacritic_Webscraper_Update import MetaCriticScraper

class ASOS_Webscraper_Tests(unittest.TestCase):
    
    def setUp(self):
        self.scraper = MetaCriticScraper('//a[@class="title"]', "browse/games/genre/date/fighting/all")


    def test_accept_cookies(self):
        URL = "https://www.metacritic.com/browse/games/genre/date/fighting/all"
        self.scraper.driver.get(URL)
        click_accept_cookies = self.scraper.accept_cookies('//button[@id="onetrust-accept-btn-handler"]')

        self.assertTrue(click_accept_cookies)

    def tearDown(self):
        self.scraper.driver.quit()

unittest.main(argv=[''], verbosity=2, exit=False)