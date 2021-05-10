import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#dataframe
userdb = pd.read_csv('csv/User_db.csv')


def app():
    st.markdown("""
    # A detailed overview of our recommendation system using KNN algorithm and YOLOv5 
    # 
    """)
    with st.beta_container():
        st.write("This is inside the container")
        st.bar_chart(np.random.randn(50, 3))

        st.write("Database of scraped images cataloged")
        st.dataframe(userdb)

        category_counts = userdb['Category'].value_counts()
        st.bar_chart(category_counts)

        gen_cat = pd.crosstab(userdb['Category'],userdb['Gender']).plot(kind="bar",stacked=True)
        st.pyplot(gen_cat)