import streamlit as st
from multiapp import MultiApp
from PIL import Image

app = MultiApp()

image = Image.open('images/HomePage.png')
st.sidebar.title('Shop Rec')

def app():

    st.markdown("""
    # Welcome to Shop-Rec
    """)
    st.subheader('Our real-time Detection and Shopping Recommendation system')
    st.image(image, width=600)

    st.write("""
        ShopRec is a Computer Vision recommendation system, used for in store personalised clothing recommendations. 
        ShopRec aims to personalise the customer retail shopping experience, and revitalise in store shopping.""")

    st.write("""
        Using machine learning and computer vision libraries such as 'YOLO' and 'RCNN', ShopRec offers a tailor made shopping experience for all users.
        Navigate through the pages on the left sidebar to understand and test our product.""")


