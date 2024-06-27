import requests
from jose import jwt, JWTError
from datetime import datetime

import os
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

KEYCLOAK_BASE_URL = os.getenv("KEYCLOAK_BASE_URL")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTH_URL = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"

def get_authorization_url():
    params = {
        'client_id': KEYCLOAK_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': 'http://192.168.100.43:8501',
        'scope': 'openid'
    }
    return f"{AUTH_URL}?{urlencode(params)}"

def exchange_code_for_token(code):
    token_url = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    data = {
        'client_id': KEYCLOAK_CLIENT_ID,
        'client_secret': KEYCLOAK_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://192.168.100.43:8501',
    }
    response = requests.post(token_url, data=data)
    return response.json(), response.status_code

def refresh_token(refresh_token):
    token_url = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': KEYCLOAK_CLIENT_ID,
        'client_secret': KEYCLOAK_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    return response.json()

def decode_token(token, audience='app01'):
    # 'secret' can be any arbitrary string since we are not verifying the signature
    options = {"verify_signature": False,"verify_aud": True}
    try:
        print(audience)
        return jwt.decode(token, 'secret', audience=audience, options=options)
    except JWTError as e:
        print(f"JWT Error: {e}")
        return None

def is_token_expired(token):
    decoded_token = decode_token(token)
    if not decoded_token:
        return True
    return decoded_token['exp'] < datetime.now().timestamp()

def get_logout(refresh_token):
    logout_url = F"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/logout"
    data = {
        'client_id': KEYCLOAK_CLIENT_ID,
        'client_secret': KEYCLOAK_CLIENT_SECRET,
        'refresh_token' : refresh_token
    }
    response = requests.post(logout_url, data=data)
    return response

def get_user_info(access_token):
    user_info_url = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/userinfo"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(user_info_url, headers=headers)
    return response.json()
