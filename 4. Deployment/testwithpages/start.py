import streamlit as st
from multiapp import MultiApp
import home
import detector
import main
import model
import test


app = MultiApp()


# Add all your application here
app.add_app("Home", home.app)
app.add_app("Clothes Detector(Yolov5)", detector.app)
app.add_app("Recommender", main.app)
app.add_app("Model", model.app)
app.add_app("test", test.app)
# The main app
app.run()