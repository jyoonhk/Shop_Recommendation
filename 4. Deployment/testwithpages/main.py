import streamlit as st
import apps
from apps import *
import pandas as pd
from PIL import Image

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
    
    profile_expander_1 = st.beta_expander('My Products and Stores')
    with profile_expander_1:
        stacked_bar = plot_stacked_bar(user_id)
        st_echarts(options=stacked_bar, height="300px")

        chart1, chart2 = st.beta_columns(2)
        with chart1:
            st.write("My Stores")
            doughnut_shop = plot_doughnut_shop(user_id)
            st_echarts(options=doughnut_shop, height="300px")

        with chart2:
            st.write("My Products")
            doughnut_products = plot_doughnut_products(user_id)
            st_echarts(options=doughnut_products, height="300px")
        
        # Example images used in slides
        # radar_style = {
        #     "title": {"text": ""},
        #     "legend": {"data": ["Mens Casual 1", "Mens Smart 1"]},
        #     "radar": {
        #         "indicator": [
        #             {"name": "Jeans", "max": 0.4},
        #             {"name": "Polos", "max": 0.4},
        #             {"name": "Shorts", "max": 0.4},
        #             {"name": "T-Shirts", "max": 0.4},
        #             {"name": "Jackets & Coats", "max": 0.4},
        #             {"name": "Jumpers", "max": 0.4},
        #             {"name": "Shirts", "max": 0.4},
        #             {"name": "Suits", "max": 0.4},
        #             {"name": "Trousers", "max": 0.4},
        #         ]
        #     },
        #     "series": [
        #         {
        #             "name": "Product Weights",
        #             "type": "radar",
        #             "data": [
        #                 {
        #                     "value": [0.25, 0.2, 0.2, 0.35, 0, 0, 0, 0, 0.1],
        #                     "name": "Mens Casual 1",
        #                 },
        #                 {
        #                     "value": [0.1, 0, 0, 0, 0.2, 0.15, 0.1, 0.25, 0.15, 0.15],
        #                     "name": "Mens Smart 1",
        #                 },
        #             ],
        #         }
        #     ],
        # }

        # radar_style2 = {
        #     "title": {"text": ""},
        #     "legend": {"data": ["Mens Casual 1", "Mens Smart 1"]},
        #     "radar": {
        #         "indicator": [
        #             {"name": "Adidas", "max": 0.25},
        #             {"name": "CalvinKleinPerformance", "max": 0.25},
        #             {"name": "Muji", "max": 0.25},
        #             {"name": "Nike", "max": 0.25},
        #             {"name": "Uniqlo", "max": 0.25},
        #             {"name": "Calvin Klein Men", "max": 0.25},
        #             {"name": "Fred Perry", "max": 0.25},
        #             {"name": "Saint Laurent", "max": 0.25},
        #             {"name": "Ralph Lauren", "max": 0.25},
        #             {"name": "Brooks Brothers", "max": 0.25},
        #             {"name": "Hugo Boss", "max": 0.25},
        #             {"name": "Moncler", "max": 0.25},
        #         ]
        #     },
        #     "series": [
        #         {
        #             "name": "Nearest Neighbours",
        #             "type": "radar",
        #             "data": [
        #                 {
        #                     "value": [0.1, 0.15, 0.1, 0.1, 0.15, 0.1, 0.05, 0.15, 0.1, 0, 0, 0],
        #                     "name": "Mens Casual 1",
        #                 },
        #                 {
        #                     "value": [0, 0, 0, 0, 0, 0.1, 0.1, 0.1, 0.2, 0.2, 0.1, 0.2 ],
        #                     "name": "Mens Smart 1",
        #                 },
        #             ],
        #         }
        #     ],
        # }

        # st_echarts(options=radar_style, height="500px")
        # st_echarts(options=radar_style2, height="500px")