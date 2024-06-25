import streamlit as st
from auth import get_authorization_url, exchange_code_for_token, refresh_token, is_token_expired

st.title("Mi aplicacion segura con Keycloak")

if 'access_token' not in st.session_state:
    auth_url = get_authorization_url()
    st.write(f"Por favor, [inicie sesion]({auth_url}) para continuar")

if 'code' in st.query_params:
    code = st.query_params.get("code")
    st.write(code)
    token_response,token_status = exchange_code_for_token(code)
    st.write(token_response)
    st.write(token_status)
    if token_status == 200:
        st.write('si tengo un toque gzgzgzg')
        st.session_state['access_token'] = token_response['access_token']
        st.session_state['refresh_token'] = token_response['refresh_token']
        #st.rerun()
    else:
        if 'access_token' in st.session_state:
            del st.session_state['access_token']
        st.error(f"Error obtaining tokens: {token_response}")
    
if 'access_token' in st.session_state:
    st.write(st.session_state['access_token'])
    if is_token_expired(st.session_state['refresh_token']):
        token_response = refresh_token(st.session_state['refresh_token'])
        st.session_state['access_token'] = token_response['access_token']
        st.session_state['refresh_token'] = token_response['refresh_token']
    st.write("Estas autenticado!")
    st.write(st.session_state['access_token'])
else:
    st.write("No estas autenticado")
