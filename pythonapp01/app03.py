import streamlit as st
import requests
from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

KEYCLOAK_BASE_URL = os.getenv("KEYCLOAK_BASE_URL")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTH_URL = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"
TOKEN_URL = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
USERINFO_URL = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/userinfo"

def get_authorization_url():
    params = {
        'client_id': KEYCLOAK_CLIENT_ID,
        'response_type': 'code'
    }
    url = f"{AUTH_URL}?{urlencode(params)}"
    return url

def get_tokens(code):
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': KEYCLOAK_CLIENT_ID,
        'client_secret': KEYCLOAK_CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    st.write('GZGZGZG')
    st.write(TOKEN_URL)
    st.write(data)
    st.write(response)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error obtaining tokens: {response.text}")
        return None

def get_user_info(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(USERINFO_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error obtaining user info: {response.text}")
        return None

def is_admin(user_info):
    return 'admin' in user_info.get('roles', [])

def token_is_expired(expires_in):
    if expires_in is None:
        return True
    return datetime.now() > datetime.now() + timedelta(seconds=expires_in)

st.title("Keycloak Authorization Code Flow Example")

query_params = st.query_params
st.write(query_params)
if 'code' in query_params:
    code = query_params['code']
    st.write(code)
    tokens = get_tokens(code)
    if tokens:
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        expires_in = tokens.get('expires_in')

        if token_is_expired(expires_in):
            st.error("Token has expired. Please log in again.")
        else:
            user_info = get_user_info(access_token)
            if user_info:
                if is_admin(user_info):
                    st.success("Welcome Admin!")
                    st.write(user_info)
                else:
                    st.warning("You are not an admin.")
else:
    st.markdown(f"[Login with Keycloak]({get_authorization_url()})")
