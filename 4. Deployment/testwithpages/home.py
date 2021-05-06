import streamlit as st
from multiapp import MultiApp
from PIL import Image

app = MultiApp()

image = Image.open('images/HomePage.png')

def app():
    st.markdown("""
    # Welcome to 'Shop-Rec'
    """)
    st.image(image)
    st.markdown("""
    # Our real-time Detection and Shopping Recommendation system
    """)

    #Select a page from the navigation bar on the left to view our product