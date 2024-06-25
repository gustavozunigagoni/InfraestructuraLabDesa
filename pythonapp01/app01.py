import streamlit as st
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakError
import requests
import time

# Configuración de Keycloak
keycloak_server_url = "https://keycloak.gustavozunigagoni.com"
keycloak_realm = "infraestructuralabdesa"
keycloak_client_id = "app01"
keycloak_client_secret = "GF0843J8R60Twpsc7i7p3ts8kGSvAQRQ"

# Inicializa el cliente OpenID Connect de Keycloak
keycloak_openid = KeycloakOpenID(
    server_url=keycloak_server_url,
    client_id=keycloak_client_id,
    realm_name=keycloak_realm,
    client_secret_key=keycloak_client_secret
)

def get_keycloak_token(auth_code, redirect_uri):
    try:
        # Intercambia el código de autorización por un token
        token = keycloak_openid.token(
            grant_type='authorization_code',
            code=auth_code,
            redirect_uri=redirect_uri
        )
        return token
    except KeycloakError as e:
        st.error(f"Error al obtener el token: {e}")
        return None

def is_token_valid(token):
    try:
        # Valida el token
        keycloak_openid.introspect(token['access_token'])
        return True
    except KeycloakError:
        return False

def refresh_token(refresh_token):
    try:
        # Refresca el token
        new_token = keycloak_openid.refresh_token(refresh_token)
        return new_token
    except KeycloakError:
        return None

def main():
    st.title("Mi Aplicación Protegida")

    # Verifica si ya tenemos un token almacenado
    if 'token' in st.session_state:
        token = st.session_state['token']

        # Verifica si el token es válido
        if is_token_valid(token):
            st.success("Autenticado con éxito")
            st.write("Contenido protegido")
        else:
            st.warning("El token ha caducado, refrescando...")
            new_token = refresh_token(token['refresh_token'])
            if new_token:
                st.session_state['token'] = new_token
                st.experimental_rerun()
            else:
                st.error("No se pudo refrescar el token, redirigiendo al login")
                del st.session_state['token']
                st.experimental_rerun()
    else:
        # URL de redirección de la aplicación
        redirect_uri = "http://192.168.100.43:8501"

        # Obtén el código de autorización de la URL
        auth_code = st.query_params.get('code')

        if auth_code:
            # Intercambia el código de autorización por un token
            token = get_keycloak_token(auth_code[0], redirect_uri)
            if token:
                st.session_state['token'] = token
                st.experimental_rerun()
        else:
            # Redirige al usuario a la página de login de Keycloak
            auth_url = keycloak_openid.auth_url(redirect_uri=redirect_uri)
            st.markdown(f"[Iniciar sesión en Keycloak]({auth_url})")

if __name__ == "__main__":
    main()
