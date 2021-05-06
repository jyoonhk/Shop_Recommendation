import streamlit as st
import numpy as np


def app():
    st.markdown("""
    # A detailed overview of our recommendation system using KNN algorithm and YOLOv5 
    # 
    """)
    with st.beta_container():
        st.write("This is inside the container")
        st.bar_chart(np.random.randn(50, 3))
    st.write("This is outside the container")