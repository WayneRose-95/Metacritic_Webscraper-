from setuptools import setup
from setuptools import find_packages

setup(
    name='Fighting_Games_Metacritic_Webscraper', ## This will be the name your package will be published with
    version='0.0.1', 
    description='Scrape all fighting games from metacritic.com',
    url='https://github.com/WayneRose-95/Metacritic_Webscraper-/tree/scrape_fighting_games_demo', # Add the URL of your github repo if published 
                                                                   # in GitHub
    author='Wayne Rose', # Your name
    # license='MIT',
    packages=find_packages(), # Find folders with an __init__.py inside it. 
    install_requires=['webdriver_manager', 'selenium'], #  Using  external libraries
                                                     # Make sure to include all external libraries in this argument
)