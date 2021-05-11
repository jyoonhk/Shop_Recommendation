import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import requests
import random
import io
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
import math
import streamlit as st
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
folder = 'C:/Users/danie/Documents/GitHub/Shop_Recommendation/4. Deployment/Test/'
image_folder = 'Data/'

product_list = {
    'Mens': ['Jackets & Coats', 'Jeans', 'Jumpers', 'Polos', 'Shirts', 'Shorts', 'Suits', 'Trousers', 'T-Shirts'],
    'Womens': ['Blouse', 'Dresses', 'Skirts', 'Jackets & Coats', 'Jeans', 'Jumpers', 'Polos', 'Shirts', 'Shorts', 'Suits', 'Trousers', 'T-Shirts']}

shop_list = {
    'Mens': ['Adidas', 'BrooksBrothers', 'CalvinKleinMen', 'CalvinKleinPerformance','FredPerry', 'HugoBoss', 'Moncler', 'Muji', 'Nike', 'Saint_Laurent', 'Uniqlo'],
    'Womens': ['Adidas', 'CalvinKleinWomen', 'CalvinKleinPerformance','HugoBoss', 'Max&Co', 'MaxMara', 'Moncler', 'Muji', 'Nike', 'Saint_Laurent', 'Uniqlo']}

@st.cache
def get_user_df():
    return pd.read_csv('csv/User_db.csv')
user_df = get_user_df()

@st.cache
def get_customer_profiles():
    customer_profiles = pd.read_csv('csv/Customer_Profiles.csv')
    customer_profiles.set_index('Customer_Cluster', inplace = True)
    customer_profiles = customer_profiles.loc[:, ~customer_profiles.columns.str.contains('^Unnamed')]
    return customer_profiles
customer_profiles = get_customer_profiles()

@st.cache
def get_shop_profiles():
    shop_profiles = pd.read_csv('csv/Shop_Profiles.csv')
    shop_profiles.set_index('Shop_Cluster', inplace = True)
    shop_profiles = shop_profiles.loc[:, ~shop_profiles.columns.str.contains('^Unnamed')]
    return shop_profiles
shop_profiles = get_shop_profiles()

@st.cache
def get_products():
    products = pd.read_csv('csv/product_db.csv')
    products = products.loc[:, ~products.columns.str.contains('^Unnamed')]
    return products
products = get_products()

#Functions to calculate Shop / Brand profiles

def create_user_shop_profile(user_df):
    #Create empty user_shop_profile df
    user_shop_profile = pd.DataFrame(columns = shop_profiles.columns[2:])
    user_shop_profile.insert(0, 'User_id',0)
    user_shop_profile.set_index(['User_id'], inplace = True)
    #Loop through users, calculate shop weights, append to user_shop_profile df
    for user_id in user_df['User_ID'].unique():
        subset = user_df[user_df['User_ID'] == user_id]
        shop_weights = subset['Brand'].value_counts()/sum(subset['Brand'].value_counts())
        user_weights = np.zeros(shape = 0)
        for brand in user_shop_profile.columns:
            try:
                user_weights = np.append(user_weights, shop_weights[brand])
            except:
                user_weights = np.append(user_weights, 0)
                pass
        user_shop_profile.loc[user_id] = user_weights
    return user_shop_profile

def create_user_product_profile(user_df):
    #Create empty user_shop_profile df
    user_product_profile = pd.DataFrame(columns = customer_profiles.columns[2:])
    user_product_profile.insert(0, 'User_id',0)
    user_product_profile.set_index(['User_id'], inplace = True)
    #Loop through users, calculate shop weights, append to user_shop_profile df
    for user_id in user_df['User_ID'].unique():
        subset = user_df[user_df['User_ID'] == user_id]
        product_weights = subset['Category'].value_counts()/sum(subset['Category'].value_counts())
        user_weights = np.zeros(shape = 0)
        for brand in user_product_profile.columns:
            try:
                user_weights = np.append(user_weights, product_weights[brand])
            except:
                user_weights = np.append(user_weights, 0)
                pass
        user_product_profile.loc[user_id] = user_weights
    return user_product_profile

#Calculate user_shop_profile
user_shop_profile = create_user_shop_profile(user_df)
user_product_profile = create_user_product_profile(user_df)
#Combine shop and product profiles into 1 df. This will be used in the distance matrix calculation
user_both_profile = pd.concat([user_shop_profile, user_product_profile], axis = 1)

#Calculate distance matrix for products and shops
input_df = user_both_profile
distance_matrix = pd.DataFrame(squareform(pdist(input_df)), columns = input_df.index, index = input_df.index)


# Function to find nearest neighbour, and select items to recommend based on either Brand, or Category (i.e. change choice = 'Brand' / 'Category')

def nearest_neighbour(user_id, user_df, distance_matrix, choice = 'Brand'):
    #Find nearest neighbour and their ID
    neighbours = distance_matrix.loc[user_id].sort_values(ascending = True)
    neighbour_id = neighbours.index[1]
    user_list = [user_id, neighbour_id]
    #Exclude items already bought by user
    bought_items = user_df[user_df['User_ID'] == user_id]['Name'].values
    # product df for neighbour with bought_items removed
    neighbour_df = user_df[user_df['User_ID'] == neighbour_id]
    neighbour_df = neighbour_df[~neighbour_df['Name'].isin(list(bought_items))]
    #Recommend Items on either Brand or lo
    recommend_df = pd.DataFrame(columns = neighbour_df.columns)
    if choice == 'Brand':
        for brand in neighbour_df['Brand'].unique():
            recommend_df = recommend_df.append(neighbour_df[neighbour_df['Brand']==brand].sample(1))
        recommend_df.drop(columns=['User_ID', 'ID', 'Customer_Cluster', 'Shop_Cluster'], inplace = True)
    elif choice == 'Category':
        for category in neighbour_df['Category'].unique():
            recommend_df = recommend_df.append(neighbour_df[neighbour_df['Category']==category].sample(1))
        recommend_df.drop(columns=['User_ID', 'ID', 'Customer_Cluster', 'Shop_Cluster'], inplace = True)
    return user_list, neighbour_id, recommend_df

# Function to find nearest neighbour, and select items to recommend based on either Brand, or Category (i.e. change choice = 'Brand' / 'Category')
def nearest_n_neighbours(user_id, user_df, distance_matrix, num_neighbours, n_items):
    #Find nearest neighbour and their ID
    neighbours = distance_matrix.loc[user_id].sort_values(ascending = True)
    user_list = list(neighbours.index[:num_neighbours+1]) 
    neighbour_list = list(neighbours.index[1:num_neighbours+1])
    #Exclude items already bought by user
    bought_items = user_df[user_df['User_ID'] == user_id]['Name'].values
    # product df for neighbour with bought_items removed
    neighbour_df = user_df[user_df['User_ID'].isin(user_list)]
    neighbour_df = neighbour_df[~neighbour_df['Name'].isin(list(bought_items))] 
    recommend_df = pd.DataFrame(columns = neighbour_df.columns)
    #Build recommend_df with common items bought by neighbours
    common_items = list(neighbour_df[neighbour_df.groupby('Image Location')['Image Location'].transform('size')>1]['Image Location'].value_counts().index)
    recommend_df = neighbour_df[neighbour_df['Image Location'].isin(common_items)] 
    recommend_df['Recommendation'] = 'Common Items'
    #Build recommend_df with randomly selected recommended items based on Brand/Category
    splits = {'Brand': 'Brand Selection', 'Category': 'Category Selection'}
    for split in splits.keys():
        for sub_category in neighbour_df[split].unique():
            dummy_df = neighbour_df[neighbour_df[split]==sub_category]
            dummy_df['Recommendation'] = splits[split]
            recommend_df = recommend_df.append(dummy_df.sample(min(n_items, len(dummy_df))))
    #Clean up recommend_df
    recommend_df.drop(columns=['User_ID', 'ID', 'Customer_Cluster', 'Shop_Cluster'], inplace = True)
    recommend_df.drop_duplicates(inplace = True)
    return user_list, neighbour_list, recommend_df


# Function to print purchased items for user and nearest neighbours
def print_user_images(user_list, n_items, user_df, headers):
    subset = user_df[user_df['User_ID'].isin(user_list)]
    for item in subset['Category'].unique():
        item_df = subset[subset['Category']==item]
        plt.figure(figsize=(20, 10))
        print(item)
        count = 0
        for user in user_list:
            user_subset1 = item_df[item_df['User_ID']==user]
            user_subset = user_subset1.sample(min(n_items, len(user_subset1)))
            for i in range(min(n_items, len(user_subset1))):
                ax = plt.subplot(1, len(user_list)*n_items, count + 1)
                url = user_subset['Image Location'].values[i]
                brand = user_subset['Brand'].values[i]
                name = user_subset['Name'].values[i]
                try:
                    im = Image.open(image_folder + url)
                    #im = Image.open(io.BytesIO(requests.get(url, stream=True, headers = headers).content))
                    plt.imshow(im)
                    plt.axis('off')
                    plt.title(f'User: {user}\n{brand}')
                    count+=1
                except:
                    pass
        plt.show()

#Print out the recommended items for the user
def print_recommended_items(recommend_df):
    print('Recommended Items:')
    plt.figure(figsize=(20, 20))
    for i in range(len(recommend_df)):
        subset = recommend_df.iloc[i]
        ax = plt.subplot(math.ceil(len(recommend_df)**0.5), math.ceil(len(recommend_df)**0.5), i + 1)
        try:
            im = Image.open(image_folder + subset['Image Location'])
            #im = Image.open(io.BytesIO(requests.get(subset['Image Location'], stream=True, headers = headers).content))
            plt.imshow(im)
            plt.axis('off')
            plt.title(f'{subset.Brand}\n{subset.Category}')
        except:
            pass
    plt.show()

#Print out the recommended common items for the user
def print_recommended_common_items(recommend_df, recommendation = 'Common Items'):
    print('Recommended Items:')    
    category_df = recommend_df[recommend_df['Recommendation']==recommendation]
    plt.subplots(figsize=(20, 20))
    count = 0
    for i in range(len(category_df)):
        item = category_df.iloc[i]
        ax = plt.subplot(math.ceil(len(category_df)**0.5), math.ceil(len(category_df)**0.5), count + 1)
        try:
            im = Image.open(image_folder + item['Image Location'])
            #im = Image.open(io.BytesIO(requests.get(item['Image URL'], stream=True, headers = headers).content))
            plt.imshow(im)
            plt.axis('off')
            plt.title(f'{item.Brand}\n{item.Category}')
            count+=1
        except:
            pass
    plt.show()

def rec_choice(x):
    #if x == 1:
    
    if x == 2:
        shop_select = st.selectbox('Select a shop', list(shop_images.keys()))
        return shop_select
    if x == 3:
        product_select = st.selectbox('Select a product', list(product_images['Womens'].keys()))
        return product_select



    profile_expander = st.beta_expander('My Favourite Shops')
    with profile_expander:
        subset = user_df[user_df['User_ID'] == int(user_id)]
        fig, ax = plt.subplots()
        plt.title('Items purchased')
        plt.xticks(rotation=45)
        sns.countplot(data = subset, x = 'Brand')
        st.pyplot(fig)

def plot_doughnut_shop(user_id):
    subset = user_df[user_df['User_ID'] == int(user_id)]
    shop_list = dict(subset['Brand'].value_counts())
    doughnut_shop = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [
            {
                "name": "Brands",
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": [{"value": int(value), "name": key} for key, value in shop_list.items()],
            }
        ],
    }
    return doughnut_shop

def plot_doughnut_products(user_id):
    subset = user_df[user_df['User_ID'] == int(user_id)]
    shop_list = dict(subset['Category'].value_counts())
    doughnut_products = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [
            {
                "name": "Brands",
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": [{"value": int(value), "name": key} for key, value in shop_list.items()],
            }
        ],
    }
    return doughnut_products

def plot_stacked_bar(user_id):
    subset = user_df[user_df['User_ID'] == int(user_id)]
    brands = list(subset['Brand'].unique())
    items = list(subset['Category'].unique())
    stacked_bar = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {
            "data": items
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {"type": "value"},
        "yAxis": {
            "type": "category",
            "data": brands,
        },
        "series": [{"name": item, "type": "bar", "stack": "total", "label": {"show": False}, "emphasis": {"focus": "series"}, 
        "data": [len(subset[(subset['Category']==item) & (subset['Brand']==brand)]) for brand in brands ],} for item in items],
    }
    return stacked_bar
    