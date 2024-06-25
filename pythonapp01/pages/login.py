import streamlit as st
from auth import get_authorization_url


def show_login():
    st.title("Login")
    st.write("Pagina de login.")
    
    # If no access token, show the login link
    auth_url = get_authorization_url()
    # Crear el enlace con target="_self" para abrir en la misma pestaña
    link = f'<a href="{auth_url}" target="_self">inicie sesión</a>'
    st.markdown(f'Por favor, {link} para continuar', unsafe_allow_html=True)