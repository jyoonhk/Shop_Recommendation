import streamlit as st
from multiapp import MultiApp
import main
import model
import home
app = MultiApp()


# Add all your application here
app.add_app("Home", home.app)
app.add_app("Recommender", main.app)
app.add_app("Model", model.app)
# The main app
app.run()