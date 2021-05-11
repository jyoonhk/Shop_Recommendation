import streamlit as st
import apps
from apps import *
import pandas as pd
from PIL import Image
import requests
import random
import io


def app():
    st.markdown("""
    # Shop Recommendation System 
    # 
    """)

    #Run to store cached data
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

    #Calculate user / shop_profile, combine and calculate distance matrix
    user_shop_profile = create_user_shop_profile(user_df)
    user_product_profile = create_user_product_profile(user_df)
    user_both_profile = pd.concat([user_shop_profile, user_product_profile], axis = 1)
    distance_matrix = pd.DataFrame(squareform(pdist(user_both_profile)), columns = input_df.index, index = input_df.index)

    user_id = st.sidebar.text_input('Enter User ID', max_chars=4, value = int(1))
    gender = user_df[user_df['User_ID']== int(user_id)]['Gender'].unique()[0]
    #recommend_type = st.selectbox('Select recommendation type', ['Similar Users', 'Products', 'Brands'])
    choices = {'By similar users': 'Common Items', 'By product': 'Category Selection', 'By shop':'Brand Selection'}

    st.write()
    recommend_type = st.sidebar.selectbox('How would you like your recommendations?', list(choices.keys()))
    recommend_type_dict = {
        'By similar users':['Most popular items'], 
        'By product':product_list[gender], 
        'By shop':shop_list[gender]}
    sub_recommend = st.sidebar.multiselect('Select items', recommend_type_dict[recommend_type])

    if st.sidebar.button('Recommend me items!'):
        n_columns = 5
        user_list_nn, neighbour_list_nn, recommend_df_nn = nearest_n_neighbours(int(user_id), user_df, distance_matrix, num_neighbours = 5, n_items = n_columns)
        recommend_output = recommend_df_nn[recommend_df_nn['Recommendation'] == choices[recommend_type]]
        st.header('Recommended for you:')
        if recommend_type == 'By product':
            for item in sub_recommend:
                count = 0
                st.subheader(item)
                sub_recommend_output = recommend_output[recommend_output['Category'] == item]
                cols = st.beta_columns(n_columns)
                for i in range(n_columns):
                    try:
                        df_row = sub_recommend_output.iloc[count]
                        im = Image.open(image_folder + df_row['Image Location'])
                        im = im.resize((150, 180))
                        cols[i].markdown(str(df_row['Brand']))
                        cols[i].image(im)
                        count+=1
                    except:
                        continue
        elif recommend_type == 'By shop':
            for item in sub_recommend:
                count = 0
                st.subheader(item)
                sub_recommend_output = recommend_output[recommend_output['Brand'] == item]
                cols = st.beta_columns(n_columns)
                for i in range(n_columns):
                    try:
                        df_row = sub_recommend_output.iloc[count]
                        im = Image.open(image_folder + df_row['Image Location'])
                        im = im.resize((150, 180))
                        cols[i].markdown(str(df_row['Category']))
                        cols[i].image(im)
                        count+=1
                    except:
                        continue
        elif recommend_type == 'By similar users':
            for item in recommend_output['Category'].unique():
                count = 0
                st.subheader(item)
                sub_recommend_output = recommend_output[recommend_output['Category'] == item]
                cols = st.beta_columns(n_columns)
                for i in range(n_columns):
                    try:
                        df_row = sub_recommend_output.iloc[count]
                        im = Image.open(image_folder + df_row['Image Location'])
                        im = im.resize((150, 180))
                        cols[i].markdown(str(df_row['Brand']))
                        cols[i].image(im)
                        count+=1
                    except:
                        continue

    st.header('My Profile')

    shopping_history_expander = st.beta_expander('My Shopping History')
    with shopping_history_expander:
        subset = user_df[user_df['User_ID'] == int(user_id)]
        n_columns = 5
        for item in subset['Category'].unique():
            count = 0
            st.subheader(item)
            item_df = subset[subset['Category']==item]
            cols = st.beta_columns(n_columns)
            for i in range(n_columns):
                try:
                    df_row = item_df.iloc[count]
                    im = Image.open(image_folder + df_row['Image Location'])
                    im = im.resize((150, 180))
                    cols[i].write(str(df_row['Brand']))
                    cols[i].image(im)
                    count+=1
                except:
                    pass
    
    profile_expander_3 = st.beta_expander('My Products and Stores')
    with profile_expander_3:
        stacked_bar = plot_stacked_bar(user_id)
        st_echarts(options=stacked_bar, height="300px")

    profile_expander_1 = st.beta_expander('My Favourite Stores')
    with profile_expander_1:
        doughnut_shop = plot_doughnut_shop(user_id)
        st_echarts(options=doughnut_shop, height="300px")

    profile_expander_2 = st.beta_expander('My Favourite Products')
    with profile_expander_2:
        doughnut_products = plot_doughnut_products(user_id)
        st_echarts(options=doughnut_products, height="300px")

