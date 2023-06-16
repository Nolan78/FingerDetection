import streamlit as st
from captcha import show_page as captcha_show_page
from try_page import show_page as try_show_page
from validated import show_page as validated_show_page

# Page layout
class Page1:
    def __init__(self):
        self.title = "Captcha"
    def show_content(self):
        captcha_show_page(self)

class Page2:
    def __init__(self):
        self.title = "Try"
    def show_content(self):
        try_show_page(self)

class Page3:
    def __init__(self):
        self.title = "Verifie les images"
    def show_content(self):
        validated_show_page(self)

# Liste des pages disponibles
pages = {
    "Captcha": Page1(),
    "Try": Page2(),
    "Verifier": Page3()
}

# État de la page actuelle
current_page = st.sidebar.selectbox("Menu", list(pages.keys()))

# Affichage du contenu de la page sélectionnée
pages[current_page].show_content()