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

# define function to build folders and empty df
def setup_scrape(shop, folder):
    folder = folder +str(shop)
    try:
        os.mkdir(folder)
    except:
        pass
    #Create empty df
    df = pd.DataFrame(columns = ['ID', 'Shop', 'Clothing Category', 'Brand', 'Category', 'Price', 'Image URL'])
    return folder, df

def append_to_df(id_no, shop, category, brand, product_category, price, src, df):
    # Create a dummy dataframe and append to main df
    df1 = pd.DataFrame({'ID': int(id_no), 
        'Shop':str(shop), 
        'Clothing Category':str(category),
        'Brand':[brand],
        'Category':[product_category], 
        'Price':[price], 
        'Image URL':[src]
        })
    df = df.append(df1)
    return df

def scroll_1(driver):
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            subhtml = driver.page_source
            soup = bs(subhtml, "html.parser")
            break 
        last_height = new_height
    subhtml = driver.page_source
    soup = bs(subhtml, "html.parser")    
    return soup

def scroll_2(driver):
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.25);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.5);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.75);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            subhtml = driver.page_source
            soup = bs(subhtml, "html.parser")
            break    
        last_height = new_height
    subhtml = driver.page_source
    soup = bs(subhtml, "html.parser")
    return soup

def scroll_3(driver):
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.25);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.5);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.75);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            subhtml = driver.page_source
            soup = bs(subhtml, "html.parser")
            break    
        last_height = new_height
    subhtml = driver.page_source
    soup = bs(subhtml, "html.parser")
    return soup

def save_image(shop, id_no, product_category, src, image_type = '.png'):
    image_name = str(shop) + ' ' + str(id_no) + ' ' + str(product_category) + str(image_type) 
    with open(image_name,'wb') as f:
        im = requests.get(src)
        f.write(im.content)
    id_no+=1
    return id_no

#Nike

def run_nike(shop, folder, urls, chromedriver_location):
    #Set up
    folder, df = setup_scrape(shop, folder)
    #Loop through urls
    for category in urls.keys():
        try:
            os.mkdir(os.path.join(folder, str(category)))
            os.chdir(os.path.join(folder, str(category)))
        except:
            os.chdir(os.path.join(folder, str(category)))
            pass
        #Use Selenium to scrape
        url = urls[category]
        driver = webdriver.Chrome(chromedriver_location)
        driver.get(url)
        subhtml = driver.page_source
        soup = bs(subhtml, "html.parser")  
        #Scroll down and rescrape, stop when last_height = new_height, since no new images
        scroll_1(driver)
        #Begin scrape once we have scrolled to the bottom of the page
        id_no = 1
        for product in soup.find_all(class_="product_list_content"):
            try:
                brand = product.find(class_ = 'up').text
                product_category = product.find(class_ = 'down').text
                price = product.find(class_ = 'color666').text
                src = product.find('a').find('img')['lazy_src']
                #Append to df and save image into folder
                df = append_to_df(id_no, shop, category, brand, product_category, price, src, df)
                id_no = save_image(shop, id_no, product_category, src, image_type = '.png')
            except:
                print('Failed')
                id_no+=1
                pass
        print(f'{category} finished')
    os.chdir(folder)
    df.to_csv(str(shop) + '.csv')
    return df


# Adidas
def run_adidas(shop, folder, urls, chromedriver_location):
    #Set up
    folder, df = setup_scrape(shop, folder)
    #Loop through urls
    for category in urls.keys():
        try:
            os.mkdir(os.path.join(folder, str(category)))
            os.chdir(os.path.join(folder, str(category)))
        except:
            os.chdir(os.path.join(folder, str(category)))
            pass
        #Use Selenium to scrape
        url = urls[category]
        driver = webdriver.Chrome(chromedriver_location)
        driver.get(url)
        subhtml = driver.page_source
        soup = bs(subhtml, "html.parser")  
        #Scroll down and rescrape, stop when last_height = new_height, since no new images
        soup = scroll_1(driver)
        #Begin scrape once we have scrolled to the bottom of the page
        id_no = 1
        for product in soup.find_all(class_="thumbnail"):
            try:
                brand = product.find(class_="goods-info").text.strip('\n')
                product_category = product.find(class_="goods-title").text.strip('\n')
                price = product.find(class_='goods-price price-single').text.strip('\n')
                src = 'http:' + product.find('img')['src']
                #Append to df and save image into folder
                df = append_to_df(id_no, shop, category, brand, product_category, price, src, df)
                id_no = save_image(shop, id_no, product_category, src, image_type = '.jpg')
            except:
                print('Failed')
                id_no+=1
                pass
        print(f'{category} finished')
    os.chdir(folder)
    df.to_csv(str(shop) + '.csv')
    return df

# MaxCo
def run_maxco(shop, folder, urls, chromedriver_location):
    #Set up
    folder, df = setup_scrape(shop, folder)
    #Loop through urls
    for category in urls.keys():
        try:
            os.mkdir(os.path.join(folder, str(category)))
            os.chdir(os.path.join(folder, str(category)))
        except:
            os.chdir(os.path.join(folder, str(category)))
            pass
        #Use Selenium to scrape
        url = urls[category]
        driver = webdriver.Chrome(chromedriver_location)
        driver.get(url)
        subhtml = driver.page_source
        soup = bs(subhtml, "html.parser")  
        #Scroll down and rescrape, stop when last_height = new_height, since no new images
        soup = scroll_2(driver)
        #Begin scrape once we have scrolled to the bottom of the page
        id_no = 1
        for product in soup.find_all(class_="main-product-image lazyloaded"):
            try:
                brand = np.nan
                product_category = product['title']
                price = np.nan
                src = product['src']
                #Append to df and save image into folder
                df = append_to_df(id_no, shop, category, brand, product_category, price, src, df)
                id_no = save_image(shop, id_no, product_category, src, image_type = '.jpg')
            except:
                print('Failed')
                id_no+=1
                pass
        print(f'{category} finished')
    os.chdir(folder)
    df.to_csv(str(shop) + '.csv')
    return df


# MaxMara
def run_maxmara(shop, folder, urls, chromedriver_location):
    #Set up
    folder, df = setup_scrape(shop, folder)
    #Loop through urls
    for category in urls.keys():
        try:
            os.mkdir(os.path.join(folder, str(category)))
            os.chdir(os.path.join(folder, str(category)))
        except:
            os.chdir(os.path.join(folder, str(category)))
            pass
        #Use Selenium to scrape
        url = urls[category]
        driver = webdriver.Chrome(chromedriver_location)
        driver.get(url)
        subhtml = driver.page_source
        soup = bs(subhtml, "html.parser")  
        #Scroll down and rescrape, stop when last_height = new_height, since no new images
        soup = scroll_2(driver)
        #Begin scrape once we have scrolled to the bottom of the page
        id_no = 1
        for product in soup.find_all(class_='product-card'):
            try:
                brand = np.nan
                product_category = product.find(class_ = 'short-description').text.strip('\n').strip()
                price = np.nan
                src = product.find(class_ = 'media lazyloaded')['src']
                #Append to df and save image into folder
                df = append_to_df(id_no, shop, category, brand, product_category, price, src, df)
                id_no = save_image(shop, id_no, product_category, src, image_type = '.jpg')
            except:
                print('Failed')
                id_no+=1
                pass
        print(f'{category} finished')
    os.chdir(folder)
    df.to_csv(str(shop) + '.csv')
    return df

# Muji
def run_muji(shop, folder, urls, chromedriver_location):
    #Set up
    folder, df = setup_scrape(shop, folder)
    #Loop through urls
    for category in urls.keys():
        try:
            os.mkdir(os.path.join(folder, str(category)))
            os.chdir(os.path.join(folder, str(category)))
        except:
            os.chdir(os.path.join(folder, str(category)))
            pass
        #Use Selenium to scrape
        url = urls[category]
        driver = webdriver.Chrome(chromedriver_location)
        driver.get(url)
        subhtml = driver.page_source
        soup = bs(subhtml, "html.parser")  
        #Scroll down and rescrape, stop when last_height = new_height, since no new images
        soup = scroll_1(driver)
        #Begin scrape once we have scrolled to the bottom of the page
        id_no = 1
        for product_list in soup.find_all(class_='listView'):
            for product in product_list.find_all(class_ = 'item'):
                try:
                    brand = np.nan
                    product_category = product.find(class_ = 'name').text.strip('\n')
                    price = product.find(class_ = 'num').text.strip('\n').strip()
                    src = 'http:' + product.find(class_ = 'thumb').find('img')['src']
                    #Append to df and save image into folder
                    df = append_to_df(id_no, shop, category, brand, product_category, price, src, df)
                    id_no = save_image(shop, id_no, product_category, src, image_type = '.jpg')
                except:
                    print('Failed')
                    id_no+=1
                    pass
        print(f'{category} finished')
    os.chdir(folder)
    df.to_csv(str(shop) + '.csv')
    return df


# Calvin Klein Men
def run_ck_men(shop, folder, urls, chromedriver_location):
    #Set up
    folder, df = setup_scrape(shop, folder)
    #Loop through urls
    for category in urls.keys():
        try:
            os.mkdir(os.path.join(folder, str(category)))
            os.chdir(os.path.join(folder, str(category)))
        except:
            os.chdir(os.path.join(folder, str(category)))
            pass
        #Use Selenium to scrape
        url = urls[category]
        driver = webdriver.Chrome(chromedriver_location)
        driver.get(url)
        subhtml = driver.page_source
        soup = bs(subhtml, "html.parser")  
        #Scroll down and rescrape, stop when last_height = new_height, since no new images
        soup = scroll_3(driver)
        #Begin scrape once we have scrolled to the bottom of the page
        id_no = 1
        for product in soup.find_all(class_='product-tile men'):
            try:
                brand = np.nan
                product_category = product.find(class_ = 'product-name').text.strip('\n')
                price = product.find(class_ = 'product-sales-price').text.strip('\n')
                src = product.find('img')['src']
                #Append to df and save image into folder
                df = append_to_df(id_no, shop, category, brand, product_category, price, src, df)
                id_no = save_image(shop, id_no, product_category, src, image_type = '.png')
            except:
                print('Failed')
                id_no+=1
                pass
        print(f'{category} finished')
    os.chdir(folder)
    df.to_csv(str(shop) + '.csv')
    return df

# Calvin Klein Women
def run_ck_women(shop, folder, urls, chromedriver_location):
    #Set up
    folder, df = setup_scrape(shop, folder)
    #Loop through urls
    for category in urls.keys():
        try:
            os.mkdir(os.path.join(folder, str(category)))
            os.chdir(os.path.join(folder, str(category)))
        except:
            os.chdir(os.path.join(folder, str(category)))
            pass
        #Use Selenium to scrape
        url = urls[category]
        driver = webdriver.Chrome(chromedriver_location)
        driver.get(url)
        subhtml = driver.page_source
        soup = bs(subhtml, "html.parser")  
        #Scroll down and rescrape, stop when last_height = new_height, since no new images
        soup = scroll_3(driver)
        #Begin scrape once we have scrolled to the bottom of the page
        id_no = 1
        for product in soup.find_all(class_='product-tile women'):
            try:
                brand = np.nan
                product_category = product.find(class_ = 'product-name').text.strip('\n')
                price = product.find(class_ = 'product-sales-price').text.strip('\n')
                src = product.find('img')['src']
                #Append to df and save image into folder
                df = append_to_df(id_no, shop, category, brand, product_category, price, src, df)
                id_no = save_image(shop, id_no, product_category, src, image_type = '.png')
            except:
                print('Failed')
                id_no+=1
                pass
        print(f'{category} finished')
    os.chdir(folder)
    df.to_csv(str(shop) + '.csv')
    return df

# Calvin Klein Performance
def run_ck_performance(shop, folder, urls, chromedriver_location):
    #Set up
    folder, df = setup_scrape(shop, folder)
    #Loop through urls
    for category in urls.keys():
        try:
            os.mkdir(os.path.join(folder, str(category)))
            os.chdir(os.path.join(folder, str(category)))
        except:
            os.chdir(os.path.join(folder, str(category)))
            pass
        #Use Selenium to scrape
        url = urls[category]
        driver = webdriver.Chrome(chromedriver_location)
        driver.get(url)
        subhtml = driver.page_source
        soup = bs(subhtml, "html.parser")  
        #Scroll down and rescrape, stop when last_height = new_height, since no new images
        soup = scroll_3(driver)
        #Begin scrape once we have scrolled to the bottom of the page
        id_no = 1
        for product in soup.find_all(class_='product-tile performance'):
            try:
                brand = np.nan
                product_category = product.find(class_ = 'product-name').text.strip('\n')
                price = product.find(class_ = 'product-sales-price').text.strip('\n')
                src = product.find('img')['src']
                #Append to df and save image into folder
                df = append_to_df(id_no, shop, category, brand, product_category, price, src, df)
                id_no = save_image(shop, id_no, product_category, src, image_type = '.png')
            except:
                print('Failed')
                id_no+=1
                pass
        print(f'{category} finished')
    os.chdir(folder)
    df.to_csv(str(shop) + '.csv')
    return df


