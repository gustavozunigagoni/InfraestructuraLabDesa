import streamlit as st
from auth import get_authorization_url, exchange_code_for_token, refresh_token, is_token_expired, get_logout
import webbrowser


def show_page_home():
    st.title("Página Home")
    st.write("Esta es la página Home")
    

# Helper function to reset session state
def reset_session():
    if 'access_token' in st.session_state:
        del st.session_state['access_token']
    if 'refresh_token' in st.session_state:
        del st.session_state['refresh_token']

# Function to clear URL parameters
def clear_url_params():
    st.query_params.clear

st.title("Mi aplicación segura con Keycloak")

# Check if there's an access token in the session
if 'access_token' in st.session_state:
    # If the token is expired, refresh it
    if is_token_expired(st.session_state['access_token']):
        token_response = refresh_token(st.session_state['refresh_token'])
        if 'access_token' in token_response:
            st.session_state['access_token'] = token_response['access_token']
            st.session_state['refresh_token'] = token_response['refresh_token']
        else:
            st.error("Error refreshing token. Please log in again.")
            reset_session()
            st.rerun()
    link = f'<a href=http://localhost:8501 target="_self">inicie sesión</a>'
    st.markdown(f'Por favor, {link} para continuar', unsafe_allow_html=True)

else:
    # Handle the callback with authorization code
    if 'code' in st.query_params:
        code = st.query_params.get("code")
        token_response, token_status = exchange_code_for_token(code)    
        if token_status == 200:
            st.session_state['access_token'] = token_response['access_token']
            st.session_state['refresh_token'] = token_response['refresh_token']
            clear_url_params()
        else:
            st.error(f"Error obtaining tokens: {token_response}")
    else:
        # If no access token, show the login link
        auth_url = get_authorization_url()
        # Crear el enlace con target="_self" para abrir en la misma pestaña
        link = f'<a href="{auth_url}" target="_self">inicie sesión</a>'
        st.markdown(f'Por favor, {link} para continuar', unsafe_allow_html=True)

if 'access_token' in st.session_state:
    st.write("Estas autenticado!")
    st.write(st.session_state['access_token'])
    if st.button("Logout"):
        response = get_logout(refresh_token=st.session_state['refresh_token'])
        st.write(response)
        reset_session()
