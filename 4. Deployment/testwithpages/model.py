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

def app():
    st.markdown("""
    # A detailed overview of our recommendation system using KNN algorithm and YOLOv5 
    """)
    st.header('Data, Model and Prediction Overview')
    #data Overview
    data_expander = st.beta_expander('Data Overview')
    with data_expander:
        st.subheader('Data Collection and Preparation')
        #webscraping
        st.write('Sample of images scraped and bounding boxes drawn over clothing categories to assist YOLO in identifying classes')
        img5,img6,img7 = st.beta_columns((1,1,2))
        with img5:
            st.image('images/suitsample.jpg')
            st.write("sample image of 'Suits' category")
        with img6:
            st.image('images/DressSample.jpg')
            st.write("sample image of 'Dresses' category")
        with img7:
            st.image('images/turkexample.jpg')
            st.write("Manual image bounding boxes drawn to assist classification for YOLO")

        #dataframe
        st.subheader('Dataframe and Cataloging')
        df, text = st.beta_columns((2,1))
        with df:
            st.dataframe(userdb)
        with text:
            st.write("""Our Database was cataloged through webscraping with BeautifulSoup of real brands we found at a real shopping mall. 
                        Values and images were scraped for our dataset and then organised into their respective columns.
                        This dataset forms the basis of our recommendation system and allows us perform necessary EDA and eventually modelling""")

        chart1, chart2 = st.beta_columns((2,1))
        with chart1:
            st.write("total no. of categories of clothing items in our dataset")
            category_counts = userdb['Category'].value_counts()
            st.bar_chart(category_counts)

        with chart2:
            st.write("breakdown of brands scraped")
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
                        YOLO employs similar methodology to CNN using feature extraction.
                        The YOLO network consists of three main parts; Backbone, Neck and Head.
                        YOLO offers a faster and more accurate recognition system and is able to create bounding boxes around detected objects
                        and offer predictions.""")
        with img1:
            st.image('images/YOLOArchitecture.png')
        #Modelling
        st.subheader("Modelling")
        st.write("""YOLO was re-trained using our dataset of images with bounding boxes to help classify the clothing categories
                    A total of 1000000 epochs were ran on Pytorch""")
        img3,img4 = st.beta_columns((1,1))
        with img3:
            st.write('Precision')
            st.image('images/P_curve.png')
        with img4:
            st.write('Recall')
            st.image('images/R_curve.png')
        #Predictions
        st.subheader("Predictions")
        img2, text3 = st.beta_columns((1,2))
        with text3:
            st.write("""Our YOLOv5 model was able to provide accuracy of upto 70% of objects detected within bounding boxes on a validation set.
                        Discrepancies and innacuracies located were rectified with various means such as deletion of categories or additional
                        images supplied to dataset to improve training and prediction accuracy""")
        with img2:
            st.image('images/yolopredictexample.jpg')

    ##Recommendation Engine Overview
    recommend_expander = st.beta_expander('KNN Recommendation Engine')
    with recommend_expander:
        st.subheader("Using KNN Algorithm to recommend items to users")
        st.write("""For user with known shopping histories, Product and Shop weightings were calculated based on Product and Shop weights.
                    Product weighting measures the proportion of each clothing type purchased; Shop weightings measures the proportion of clothes purchased at each shop.
                    Nearest Neighbours were found based on Euclidean distance to both these weightings. A static distance matrix of the distance between all known users was calculated and stored, which allowed faster calculations of nearest neighbours.
                    For illustration, User 1 and 193 are nearest neighbours as they both have very similar Product and Shop profiles.
                    """)
