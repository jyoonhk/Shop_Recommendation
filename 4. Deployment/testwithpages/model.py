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
    # 
    """)
    
    st.write("Database of scraped images cataloged")
    st.dataframe(userdb)

    category_counts = userdb['Category'].value_counts()
    st.bar_chart(category_counts)

    st_echarts(options=doughnut, height="300px")

