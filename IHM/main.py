import streamlit as st
import captcha

st.set_page_config(page_title="Google Killer", page_icon="📝", layout="wide")
# Page layout
class Page1:
    def __init__(self):
        self.title = "Captcha"
    def show_content(self):
        captcha.show_page(self)


class Page2:
    def __init__(self):
        self.title = "Page 2"

    def show_content(self):
        st.header(self.title)
        st.write("Contenu de la page 2")

class Page3:
    def __init__(self):
        self.title = "Page 3"

    def show_content(self):
        st.header(self.title)
        st.write("Contenu de la page 3")

# Liste des pages disponibles
pages = {
    "Captcha": Page1(),
    "Page 2": Page2(),
    "Page 3": Page3()
}

# État de la page actuelle
current_page = st.sidebar.selectbox("Menu", list(pages.keys()))

# Affichage du contenu de la page sélectionnée
pages[current_page].show_content()