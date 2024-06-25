import streamlit as st

from pages.login import show_login
from pages.home import show_home 

from auth import refresh_token, is_token_expired, exchange_code_for_token, get_logout

def reset_session():
    if 'access_token' in st.session_state:
        del st.session_state['access_token']
    if 'refresh_token' in st.session_state:
        get_logout(st.session_state['refresh_token'])
        del st.session_state['refresh_token']

def change_page(page):
    st.session_state['page'] = page

# Configuración inicial
st.set_page_config(page_title="Multi-page Streamlit App", page_icon="🌐", layout="wide")

if 'page' not in st.session_state:
    st.session_state['page'] = 'login'  

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False 

if st.session_state['loginstatus'] == False:
    reset_session()
    
if 'access_token' in st.session_state:
    # If the token is expired, refresh it
    if is_token_expired(st.session_state['access_token']):
        token_response = refresh_token(st.session_state['refresh_token'])
        if 'access_token' in token_response:
            st.session_state['access_token'] = token_response['access_token']
            st.session_state['refresh_token'] = token_response['refresh_token']
        else:
            st.error("Error refreshing token. Please log in again.")
            st.session_state['loginstatus'] = False 
    else:
        st.session_state['loginstatus'] = True
        change_page('home')
else:
    # Handle the callback with authorization code
    if 'code' in st.query_params and st.session_state['page'] == 'login':
        code = st.query_params.get("code")
        token_response, token_status = exchange_code_for_token(code)    
        st.write(token_response)
        if token_status == 200:
            st.session_state['access_token'] = token_response['access_token']
            st.session_state['refresh_token'] = token_response['refresh_token']
            st.session_state['loginstatus'] = True
            change_page('home')
        #else:
        #    st.error(f"Error obtaining tokens: {token_response}")
    else:
        st.session_state['loginstatus'] = False
        change_page('login')

# Mostrar Página 1 (predeterminada)
if st.session_state['page'] == 'login':
    show_login()

# Mostrar Página 2
elif st.session_state['page'] == 'home':
    show_home()

