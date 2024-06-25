import streamlit as st

from auth import get_user_info,decode_token

def change_page(page):
    st.session_state['page'] = page

def show_home():
    st.title("Home")
    st.write("Bienvenido a la Home")

    st.write(decode_token(st.session_state['access_token']))

    st.write(st.session_state['access_token'])


    if st.button(label="Logout"):
        del st.session_state["page"]
        st.session_state['loginstatus'] = False
        st.rerun()

    if st.button(label="rerun"):
        st.rerun()
    




    
  