import streamlit as st
from datetime import datetime

from auth import refresh_token, is_token_expired, exchange_code_for_token, get_logout, get_authorization_url

# Definir las credanciales y las paginas accecibles para cada usuario
USERS= {
    "gustavozunigagoni@yahoo.com":{
        "password": "contrasenaA",
        "pages": ["Inicio","Pagina 1", "Pagina 2"]
    },
    "usuarioB":{
        "password": "contrasenaB",
        "pages": ["Inicio", "Pagina 3", "Pagina 4"]
    }
}

# Variables de session para manejar el estado de login y usuario actual
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Inicio"

def login(username):
    # Funsion para manejar el login
    st.session_state['logged_in'] = True
    st.session_state['current_user'] = username
    st.rerun()

def logout():
    # Funsion para manejar el logout
    get_logout(st.session_state['refresh_token'])
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = None
    st.session_state['current_page'] = "Inicio"
    if 'access_token' in st.session_state:
        del st.session_state['access_token']
    if 'refresh_token' in st.session_state:
        del st.session_state['refresh_token']
    st.rerun()

def show_login_page():
    # Muestra la pagina de login

    auth_url = get_authorization_url()
    # Crear el enlace con target="_self" para abrir en la misma pestaña
    link = f'<a href="{auth_url}" target="_self">inicie sesión</a>'
    st.markdown(f'Por favor, {link} para continuar', unsafe_allow_html=True)

    
    #st.title("Pagina de login")
    #username = st.text_input("Usuario")
    #password = st.text_input("Password", type="password")
    #if st.button("Login"):
        #if username in USERS and password == USERS[username]["password"]:
     #   login('gustavozunigagoni@yahoo.com')
    #        st.success("Login exitoso")
    #    else:
    #        st.error("Usuario o contrasena incorrecto")
#
def show_home_page():
    # Muestra la pagina de inicio
    st.title("Pagina de inicio")
    st.write("Bienvenido a la pagina de inicio")

def show_page1():
    # Muestra la pagina 1
    st.title("Pagina 1")
    st.write("Contenido de pagina 1")

def show_page2():
    # Muestra la pagina 1
    st.title("Pagina 2")
    st.write("Contenido de pagina 2")

def show_page3():
    # Muestra la pagina 1
    st.title("Pagina 3")
    st.write("Contenido de pagina 3")

def show_page4():
    # Muestra la pagina 1
    st.title("Pagina 4")
    st.write("Contenido de pagina 4")

def show_siderbar(user):
    # Muestra el sidebar con las opciones de navegacion
    with st.sidebar:
        st.title("Navegacion")
        pages = USERS[user]["pages"]
        choice = st.radio("Ir a ", pages)
        if st.button("Logout"):
            logout()
        return choice
    
# Mostrar la pagina correspondiente basado en el estado de login
print(st.session_state['logged_in'])
if st.session_state['logged_in']:
    st.session_state['current_page'] = show_siderbar(st.session_state['current_user'])

    if st.session_state['current_page'] == "Inicio":
        show_home_page()
    elif st.session_state['current_page'] == "Pagina 1":
        show_page1()
    elif st.session_state['current_page'] == "Pagina 2":
        show_page2()
    elif st.session_state['current_page'] == "Pagina 3":
        show_page3()
    elif st.session_state['current_page'] == "Pagina 4":
        show_page4()
else:
    show_login_page()

# Validacion de acceso por token
if 'access_token' in st.session_state:
    st.write("Hay token")
    st.write(datetime.now())
    st.write(st.session_state['access_token'])
    if is_token_expired(st.session_state['access_token']):
        token_response = refresh_token(st.session_state['refresh_token'])
        if 'access_token' in token_response:
            st.session_state['access_token'] = token_response['access_token']
            st.session_state['refresh_token'] = token_response['refresh_token']
        else:
            st.error("Error refreshing token. Please log in again.")
            logout()
else:
    if 'code' in st.query_params:
        st.write("NO Hay token")
        st.write(st.query_params['code']) 
        code = st.query_params.get("code")
        token_response, token_status = exchange_code_for_token(code)    
        #st.write(token_response)  
        if token_status == 200:
            st.session_state['access_token'] = token_response['access_token']
            st.session_state['refresh_token'] = token_response['refresh_token']
            login('gustavozunigagoni@yahoo.com')
            
    else:
        st.write("No hay codigo en paramatros")

