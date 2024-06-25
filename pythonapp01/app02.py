from flask import Flask, redirect, request, session, url_for
import requests
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de Keycloak
KEYCLOAK_URL = 'https://keycloak.gustavozunigagoni.com'
REALM_NAME = 'infraestructuralabdesa'
CLIENT_ID = 'app01'
CLIENT_SECRET = 'V9dODnI9TfTEigXlMGfDH31xzPa3oDfF'
REDIRECT_URI = 'http://192.168.100.43:8501/callback'

# URLs de Keycloak
AUTH_URL = f'{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/auth'
TOKEN_URL = f'{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token'

# Función para verificar si el token de acceso es válido
def is_token_valid():
    access_token = session.get('access_token')
    expires_at = session.get('expires_at')
    
    if not access_token or not expires_at:
        return False
    
    # Convertir la cadena de expiración a un objeto datetime
    expires_at = datetime.strptime(expires_at, '%Y-%m-%d %H:%M:%S.%f')
    current_time = datetime.now()
    
    if current_time >= expires_at:
        return False
    
    return True

@app.route('/')
def home():
    if is_token_valid():
        return 'Logged in with token: ' + session['access_token']
    else:
        return redirect(url_for('login'))
        
@app.route('/login')
def login():
    return redirect(
        f'{AUTH_URL}?response_type=code&client_id={CLIENT_ID}'
        ## https://keycloak.gustavozunigagoni.com/realms/infraestructuralabdesa/protocol/openid-connect/auth?response_type=code&client_id=app01
    )

@app.route('/callback')
def callback():
    code = request.args.get('code')
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        tokens = response.json()
        session['access_token'] = tokens['access_token']
        session['refresh_token'] = tokens['refresh_token']
        session['expires_in'] = tokens['expires_in']
        return redirect(url_for('home'))
    else:
        return 'Error retrieving token', response.status_code

@app.route('/refresh')
def refresh():
    refresh_token = session.get('refresh_token')
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        tokens = response.json()
        session['access_token'] = tokens['access_token']
        session['refresh_token'] = tokens['refresh_token']
        session['expires_in'] = tokens['expires_in']
        return 'Token refreshed'
    else:
        return 'Error refreshing token', response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501, debug=True)
