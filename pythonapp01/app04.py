import streamlit as st
import requests
from urllib.parse import urlencode, urlparse, parse_qs
import json
import time

# Configuración de Keycloak
KEYCLOAK_SERVER_URL = "https://keycloak.gustavozunigagoni.com"
REALM = "infraestructuralabdesa"
CLIENT_ID = "app01"
CLIENT_SECRET = "GF0843J8R60Twpsc7i7p3ts8kGSvAQRQ"
REDIRECT_URI = "http://192.168.100.43:8501"
AUTH_URL = f"{KEYCLOAK_SERVER_URL}/realms/{REALM}/protocol/openid-connect/auth"
TOKEN_URL = f"{KEYCLOAK_SERVER_URL}/realms/{REALM}/protocol/openid-connect/token"
USERINFO_URL = f"{KEYCLOAK_SERVER_URL}/realms/{REALM}/protocol/openid-connect/userinfo"


# Función para obtener el token
def get_token(auth_code):
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=payload)
    return response.json()

# Función para obtener información del usuario
def get_user_info(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(USERINFO_URL, headers=headers)
    return response.json()

# Función para verificar si el usuario pertenece al grupo "admin"
def is_user_admin(user_info):
    return "admin" in user_info.get("groups", [])

# Interfaz de Streamlit
st.title("Aplicación con Keycloak")

query_params = st.query_params
auth_code = query_params.get("code")

if auth_code:
    auth_code = auth_code[0]
    token_response = get_token(auth_code)
    
    if 'access_token' in token_response:
        access_token = token_response['access_token']
        refresh_token = token_response['refresh_token']
        expires_in = token_response['expires_in']
        token_expiry_time = time.time() + expires_in
        
        st.session_state.access_token = access_token
        st.session_state.refresh_token = refresh_token
        st.session_state.token_expiry_time = token_expiry_time
        
        user_info = get_user_info(access_token)
        st.session_state.user_info = user_info
        
        if is_user_admin(user_info):
            st.write("Bienvenido, Admin!")
        else:
            st.write("No tienes permisos de administrador.")
    else:
        st.write("Error al obtener el token.")
else:
    if 'access_token' in st.session_state:
        if st.session_state.token_expiry_time > time.time():
            st.write("Ya has iniciado sesión.")
            if is_user_admin(st.session_state.user_info):
                st.write("Bienvenido, Admin!")
            else:
                st.write("No tienes permisos de administrador.")
        else:
            st.write("El token ha expirado. Por favor, inicia sesión de nuevo.")
    else:
        params = {
            'client_id': CLIENT_ID,
            'response_type': 'code'
        }
        auth_url = f"{AUTH_URL}?{urlencode(params)}"
        st.markdown(f"[Iniciar sesión en Keycloak]({auth_url})")

