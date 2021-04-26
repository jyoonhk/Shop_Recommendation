#Import libraries
import requests
from bs4 import BeautifulSoup as bs
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import numpy as np
import time
import os

import webscrape_app
from webscrape_app import run_nike, run_adidas, run_maxco, run_maxmara, run_muji, run_ck_men, run_ck_women, run_ck_performance

# DEFINE GLOBAL VARIABLES
folder = 'C:/Users/danie/Documents/FTDS/Capstone/1. Webscraping/Output/'
chromedriver_location = 'C:/Program Files (x86)/chromedriver_win32/chromedriver.exe'

# Nike
nike_shop = 'Nike'
nike_urls = {
    'Mens Shorts': 'https://www.nike.com.hk/man/apparel/shorttrousers/list.htm?locale=en-gb',
    'Mens Hoodies & Pullovers': 'https://www.nike.com.hk/man/apparel/hoodies_and_pullovers/list.htm?locale=en-gb',
    'Mens Pants & Tights':'https://www.nike.com.hk/man/apparel/pants_and_tights/list.htm?locale=en-gb',
    'Mens Jackets & Vests':'https://www.nike.com.hk/man/apparel/jackets_and_vests/list.htm?locale=en-gb',
    'Mens Tops & T-shirts':'https://www.nike.com.hk/man/apparel/top_and_shirt/list.htm?locale=en-gb',
    'Womens Shorts': 'https://www.nike.com.hk/woman/apparel/shorttrousers/list.htm?locale=en-gb',
    'Womens Hoodies & Pullovers': 'https://www.nike.com.hk/woman/apparel/hoodies_and_pullovers/list.htm?locale=en-gb',
    'Womens Pants & Tights':'https://www.nike.com.hk/woman/apparel/pants_and_tights/list.htm?locale=en-gb',
    'Womens Jackets & Vests':'https://www.nike.com.hk/woman/apparel/jackets_and_vests/list.htm?locale=en-gb',
    'Womens Tops & T-shirts':'https://www.nike.com.hk/woman/apparel/top_and_shirt/list.htm?locale=en-gb',
    'Womens Skirts':'https://www.nike.com.hk/woman/skirt/list.htm?locale=en-gb'}

# Adidas
adidas_shop = 'Adidas'
adidas_urls = {
    'Mens T-Shirts': 'https://www.adidas.com.hk/men/clothing/tshirts?locale=en_GB',
    'Mens Polos': 'https://www.adidas.com.hk/men/clothing/polos?locale=en_GB',
    'Mens Sweatshirts & Hoodies':'https://www.adidas.com.hk/men/clothing/sweatshirtshoodies?locale=en_GB',
    'Mens Jackets':'https://www.adidas.com.hk/men/clothing/jackets?locale=en_GB',
    'Mens Pants': 'https://www.adidas.com.hk/men/clothing/pants?locale=en_GB',
    'Mens Shorts':'https://www.adidas.com.hk/men/clothing/shorts?locale=en_GB',
    'Mens Jerseys': 'https://www.adidas.com.hk/men/clothing/jerseys?locale=en_GB',
    'Mens Tights': 'https://www.adidas.com.hk/men/clothing/tights?locale=en_GB',
    'Mens Tracksuits':'https://www.adidas.com.hk/men/clothing/tracksuits?locale=en_GB',
    'Womens T-Shirts': 'https://www.adidas.com.hk/women/clothing/tshirts?locale=en_GB',
    'Womens Polos': 'https://www.adidas.com.hk/women/clothing/polos?locale=en_GB',
    'Womens Sweatshirts & Hoodies':'https://www.adidas.com.hk/women/clothing/sweatshirtshoodies?locale=en_GB',
    'Womens Jackets':'https://www.adidas.com.hk/women/clothing/jackets?locale=en_GB',
    'Womens Pants': 'https://www.adidas.com.hk/women/clothing/pants?locale=en_GB',
    'Womens Shorts':'https://www.adidas.com.hk/women/clothing/shorts?locale=en_GB',
    'Womens Jerseys': 'https://www.adidas.com.hk/women/clothing/jerseys?locale=en_GB',
    'Womens Tights': 'https://www.adidas.com.hk/women/clothing/tights?locale=en_GB',
    'Womens Tracksuits':'https://www.adidas.com.hk/women/clothing/tracksuits?locale=en_GB',
    'Womens Dresses':'https://www.adidas.com.hk/women/clothing/dresses?locale=en_GB',
    'Womens Skirts':'https://www.adidas.com.hk/women/clothing/skirts?locale=en_GB'
    }

#MaxCo
maxco_shop = 'Max&Co'
maxco_urls = {
    'Womens Dresses': 'https://cn.maxandco.com/clothing/womens-dresses',
    'Womens Jumpsuits':'https://cn.maxandco.com/clothing/elegant-jumpsuits',
    'Womens Sweaters & Cardigans': 'https://cn.maxandco.com/clothing/womens-sweaters-cardigans',
    'Womens Shirts Blouses & Tops': 'https://cn.maxandco.com/clothing/womens-shirts-tops',
    'Womens Sweatshirts & T-Shirts': 'https://cn.maxandco.com/clothing/sweatshirts-and-t-shirts',
    'Womens Trousers' :'https://cn.maxandco.com/clothing/womens-trousers',
    'Womens Skirts':'https://cn.maxandco.com/clothing/skirts',
    'Womens Jeans and Denim':'https://cn.maxandco.com/clothing/jeans-womens-denim',
    'Womens Coats':'https://cn.maxandco.com/clothing/womens-coat-parka',
    'Womens Jackets & Blazers':'https://cn.maxandco.com/clothing/womens-jacket-blazers'
    }

#MaxMara
maxmara_shop = 'MaxMara'
maxmara_urls = {
    'Womens Dresses': 'https://cn.maxmara.com/clothing/womens-dresses',
    'Womens Jumpsuits':'https://cn.maxmara.com/clothing/elegant-womens-jumpsuits',
    'Womens Sweaters & Cardigans': 'https://cn.maxmara.com/clothing/womens-knitwear-sweaters',
    'Womens Suits': 'https://cn.maxmara.com/clothing/womens-suits',
    'Womens Tops & T-Shirts': 'https://cn.maxmara.com/clothing/womens-tops-and-t-shirts',
    'Womens Skirts':'https://cn.maxmara.com/clothing/skirts',
    'Womens Trousers & Jeans':'https://cn.maxmara.com/clothing/womens-trousers-and-jeans',
    }

# Muji
muji_shop = 'Muji'
muji_urls = {
    'Mens Shirts':'https://www.muji.com.hk/en/sub-category.php?dept=101&id=009&c=001',
    'Mens Knitwear':'https://www.muji.com.hk/en/sub-category.php?dept=101&id=117&c=001',
    'Mens Trousers':'https://www.muji.com.hk/en/sub-category.php?dept=101&id=011&c=001',
    'Mens Jackets':'https://www.muji.com.hk/en/sub-category.php?dept=101&id=004&c=001',
    'Womens Shirts':'https://www.muji.com.hk/en/sub-category.php?dept=102&id=009&c=001',
    'Womens Knitwear':'https://www.muji.com.hk/en/sub-category.php?dept=102&id=007&c=001',
    'Womens Trousers':'https://www.muji.com.hk/en/sub-category.php?dept=102&id=011&c=001',
    'Womens Jackets':'https://www.muji.com.hk/en/sub-category.php?dept=102&id=004&c=001'
    }

#CalvinKleinMen
ck_men_shop = 'CalvinKleinMen'
calvin_klein_men_urls = {
    'Mens Jackets':'https://www.calvinklein.com/hk/en/men-apparel-jackets',
    'Mens T-Shirts': 'https://www.calvinklein.com/hk/en/men-apparel-t-shirts/',
    'Mens Hoodies':'https://www.calvinklein.com/hk/en/men-apparel-sweatshirts-hoodies/',
    'Mens Sweaters':'https://www.calvinklein.com/hk/en/men-apparel-sweaters/',
    'Mens Shirts':'https://www.calvinklein.com/hk/en/men-apparel-shirts/',
    'Mens Jeans':'https://www.calvinklein.com/hk/en/men-apparel-denim-jeans/',
    'Mens Trousers': 'https://www.calvinklein.com/hk/en/men-apparel-pants-shorts/'
    }

#CalvinKleinWomen
ck_women_shop = 'CalvinKleinWomen'
calvin_klein_women_urls = {
    'Womens Jackets':'https://www.calvinklein.com/hk/en/women-apparel-jackets',
    'Womens T-Shirts': 'https://www.calvinklein.com/hk/en/women-apparel-t-shirts/',
    'Womens Hoodies':'https://www.calvinklein.com/hk/en/women-apparel-sweatshirts-hoodies/',
    'Womens Sweaters':'https://www.calvinklein.com/hk/en/women-apparel-sweaters-cardigans/',
    'Womens Tops':'https://www.calvinklein.com/hk/en/women-apparel-tops/',
    'Womens Dresses':'https://www.calvinklein.com/hk/en/women-apparel-dresses/',
    'Womens Skirts':'https://www.calvinklein.com/hk/en/women-apparel-skirts/',
    'Womens Jeans':'https://www.calvinklein.com/hk/en/women-apparel-denim-jeans/',
    'Womens Trousers': 'https://www.calvinklein.com/hk/en/women-apparel-pants-shorts/'
    }

#CalvinKleinPerformance
ck_perfomance_shop = 'CalvinKleinPerformance'
calvin_klein_performance_urls = {
    'Mens Jackets':'https://www.calvinklein.com/hk/en/performance-mens-apparel-windbreakers-sweat-jackets/',
    'Mens T-Shirts': 'https://www.calvinklein.com/hk/en/performance-mens-apparel-t-shirts/',
    'Mens Hoodies':'https://www.calvinklein.com/hk/en/performance-mens-apparel-sweatshirts-hoodies/',
    'Mens Shorts': 'https://www.calvinklein.com/hk/en/performance-mens-apparel-pants-shorts/',
    'Womens Leggings':'https://www.calvinklein.com/hk/en/performance-womens-apparel-leggings/',
    'Womens Jackets':'https://www.calvinklein.com/hk/en/performance-womens-apparel-windbreakers-sweat-jackets/',
    'Womens T-Shirts':'https://www.calvinklein.com/hk/en/performance-womens-apparel-t-shirts/',
    'Womens Hoodies':'https://www.calvinklein.com/hk/en/performance-womens-apparel-sweatshirts-hoodies/',
    'Womens Dresses':'https://www.calvinklein.com/hk/en/performance-womens-apparel-dresses/',
    'Womens Shorts': 'https://www.calvinklein.com/hk/en/performance-womens-apparel-pants-shorts/',
    'Womens Skirts': 'https://www.calvinklein.com/hk/en/performance-womens-apparel-skirts/'
    }

# Run functions
run_nike(nike_shop, folder, nike_urls, chromedriver_location)
run_adidas(adidas_shop, folder, adidas_urls, chromedriver_location)
run_maxco(maxco_shop, folder, maxco_urls, chromedriver_location)
run_maxmara(maxmara_shop, folder, maxmara_urls, chromedriver_location)
run_muji(muji_shop, folder, muji_urls, chromedriver_location)
run_ck_men(ck_men_shop, folder, calvin_klein_men_urls, chromedriver_location)
run_ck_women(ck_women_shop, folder, calvin_klein_women_urls, chromedriver_location)
run_ck_performance(ck_perfomance_shop, folder, calvin_klein_performance_urls, chromedriver_location)