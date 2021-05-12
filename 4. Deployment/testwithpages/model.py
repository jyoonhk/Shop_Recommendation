import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts import options as opts
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts

#dataframe
userdb = pd.read_csv('csv/User_db.csv')



doughnut = {
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
            "data": [
                {"value": 1048, "name": "Uniqlo"},
                {"value": 735, "name": "Adidas"},
                {"value": 580, "name": "Nike"},
                {"value": 484, "name": "Hugo Boss"},
                {"value": 300, "name": "Zara"},
            ],
        }
    ],
}

radar_shops = {
    "title": {"text": ""},
    "legend": {"data": ["User 1", "User 193 (Nearest Neighbour)"]},
    "radar": {
        "indicator": [
            {"name": "Jackets & Coats", "max": 0.5},
            {"name": "T-Shirts", "max": 0.5},
            {"name": "Shorts", "max": 0.5},
            {"name": "Polos", "max": 0.5},
            {"name": "Jumpers", "max": 0.5},
            {"name": "Jeans", "max": 0.5},
        ]
    },
    "series": [
        {
            "name": "Nearest Neighbours",
            "type": "radar",
            "data": [
                {
                    "value": [0.2, 0.3, 0.1, 0.15, 0.2, 0.1],
                    "name": "User 1",
                },
                {
                    "value": [0.18, 0.4, 0.12, 0.1, 0.15, 0.08],
                    "name": "User 193 (Nearest Neighbour)",
                },
            ],
        }
    ],
}

radar_products = {
    "title": {"text": ""},
    "legend": {"data": ["User 1", "User 193 (Nearest Neighbour)"]},
    "radar": {
        "indicator": [
            {"name": "Adidas", "max": 0.2},
            {"name": "Ralph Lauren", "max": 0.2},
            {"name": "Uniqlo", "max": 0.2},
            {"name": "Saint Laurent", "max": 0.2},
            {"name": "Fred Perry", "max": 0.2},
            {"name": "Nike", "max": 0.2},
            {"name": "Muji", "max": 0.2},
            {"name": "Calvin Klein Performance", "max": 0.2},
        ]
    },
    "series": [
        {
            "name": "Nearest Neighbours",
            "type": "radar",
            "data": [
                {
                    "value": [0.15, 0.15, 0.18, 0.05, 0.05, 0.18, 0.1, 0.15],
                    "name": "User 1",
                },
                {
                    "value": [0.17, 0.12, 0.19, 0.05, 0.07, 0.2, 0.12, 0.1],
                    "name": "User 193 (Nearest Neighbour)",
                },
            ],
        }
    ],
}

def app():
    st.markdown("""
    # Overview of the KNN Recommendation System and YOLOv5 
    """)
    st.header('Data, Modelling and Prediction Overview')
    #data Overview
    data_expander = st.beta_expander('Data Overview')
    with data_expander:
        st.subheader('Data Collection and Preparation')
        #webscraping
        st.write('Sample of images scraped and bounding boxes drawn over clothing categories to assist YOLO in identifying classes')
        img5,img6,img7 = st.beta_columns((1,1,2))
        with img5:
            st.image('images/suitsample.jpg')
            st.write("Sample image of 'Suits' category")
        with img6:
            st.image('images/DressSample.jpg')
            st.write("Sample image of 'Dresses' category")
        with img7:
            st.image('images/turkexample.jpg')
            st.write("Manual image bounding boxes drawn to assist classification for YOLO")

        #dataframe
        st.subheader('Dataframe and Cataloging')
        df, text = st.beta_columns((3,2))
        with df:
            st.dataframe(userdb)
        with text:
            st.write("""Our Database was catalogued through webscraping with BeautifulSoup of real brands identified at an existing shopping mall.""")
            st.write("""Values and images were scraped for our dataset and then organised into their respective columns.""")
            st.write("""This dataset forms the basis of our recommendation system and allows us perform necessary EDA and image recognition modelling""")

        st.write("""\n""")
        chart1, chart2 = st.beta_columns((2,1))
        with chart1:
            st.write("Total no. of clothing categories")
            category_counts = userdb['Category'].value_counts()
            st.bar_chart(category_counts)

        with chart2:
            st.write("Breakdown of brands scraped")
            st_echarts(options=doughnut, height="300px")

##CNN Expander
    cnn_expander = st.beta_expander('CNN Modelling')
    with cnn_expander:
        st.subheader("Using MobileNetV2 and others")
        st.write("An Initial attempt was made using Pre-Trained models (MobileNetV2) to train the CNN model using our dataset of images")

##YOLO Expander
    yolo_expander = st.beta_expander('YOLOv5 Modelling')
    with yolo_expander:
        st.subheader("Using YOLOv5 recognition library")
        img1, text2 = st.beta_columns((2,1))
        with text2:
            st.write("""Our final modelling rested on using YOLOv5 image recognition library.
                        YOLO employs similar methodology to CNN using feature extraction.""")
            st.write("""The YOLO network consists of three main parts; Backbone, Neck and Head. YOLO offers a faster and more accurate recognition system and is able to create bounding boxes around detected objects
                        and offer predictions.""")
        with img1:
            st.image('images/YOLOArchitecture.png')
        #Modelling
        st.subheader("Modelling")
        st.write("""YOLO was re-trained using our dataset of images with bounding boxes to help classify the clothing categories.
                    A total of 100 epochs were ran on Pytorch""")
        img3,img4 = st.beta_columns((1,1))
        with img3:
            st.write('Precision')
            st.image('images/P_curve.png')
        with img4:
            st.write('Recall')
            st.image('images/R_curve.png')
        #Predictions
        st.subheader("Predictions")
        img2, text3 = st.beta_columns((2,3))
        with text3:
            st.write("""Our YOLOv5 model was able to provide accuracy of up to 70% of objects detected within bounding boxes on a validation set.""")
            st.write("""Discrepancies and innacuracies located were rectified with various means such as deletion of categories or additional
                        images supplied to dataset to improve training and prediction accuracy""")
        with img2:
            st.image('images/yolopredictexample.jpg')

    ##Recommendation Engine Overview
    recommend_expander = st.beta_expander('KNN Recommendation Engine')
    with recommend_expander:
        st.subheader("KNN Algorithm User Recommendations")
        st.markdown("""For users with known shopping histories, Product and Shop profiles were calculated based on Product and Shop weights.
                    Product weightings measure the proportion of each clothing type purchased by a customers; shop weightings measure the proportion of clothes purchased at each shop.""")

        st.markdown("""Nearest Neighbours were found based on Euclidean distance to these weightings. A static distance matrix of the distance between all known users was calculated and stored, which allowed faster calculations of nearest neighbours.""")
        st.markdown("""For illustration, User 1 and 193 are nearest neighbours as they both have very similar Product and Shop profiles:""")

        chart1, chart2 = st.beta_columns(2)
        with chart1:
            st.write("Customer Product profiles")
            st_echarts(radar_shops, height="400px")

        with chart2:
            st.write("Customer Shop profiles")
            st_echarts(radar_products, height="400px")

        st.write("""
        Once nearest neighbours are established for a user, the recommendation system works as follows:

        - All items bought by nearest neighbours are pooled together
        
        - Items already purchased by the user are removed
        
        - Products bought by nearest neighbours are ranked and recommended based on popularity.""")

        st.markdown("""Users are also able to filter their recommendation e.g. by specific stores, and/or by product type.""")

