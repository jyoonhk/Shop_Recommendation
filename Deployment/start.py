import streamlit as st
from multiapp import MultiApp
import home
import vision_rec
import main
import model
import test


app = MultiApp()


# Add all your application here
app.add_app("Home", home.app)
app.add_app("Data Overview and Modelling", model.app)
app.add_app("Vision Detector", vision_rec.app)
app.add_app("Recommendation Engine", main.app)
#app.add_app("test page", test.app)
# The main app
app.run()