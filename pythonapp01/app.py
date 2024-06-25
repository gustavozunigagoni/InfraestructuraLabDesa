import streamlit as st
import requests

# Función para obtener los parámetros de la URL
def get_url_params():
    query_params = st.experimental_get_query_params()
    return query_params

# Obtener los parámetros de la URL
params = get_url_params()

# Mostrar los parámetros en la aplicación de Streamlit
st.title('Aplicación de Streamlit con Parámetros de URL')
st.write('Parámetros de la URL:', params)

# Extraer el código de los parámetros de la URL
code = params.get('code', [None])[0]

# Mostrar el código en la aplicación de Streamlit
st.write('Código:', code)

# Verificar que el código no sea None antes de hacer la solicitud
if code:
    # Datos para la solicitud
    url = 'https://keycloak.gustavozunigagoni.com/realms/infraestructuralabdesa/protocol/openid-connect/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': 'app01',
        'client_secret': 'GF0843J8R60Twpsc7i7p3ts8kGSvAQRQ',
        'code': code,
        'grant_type': 'authorization_code'
    }

    # Mostrar los datos de la solicitud
    st.write('Datos de la solicitud:', data)

    # Realizar la solicitud HTTP
    response = requests.post(url, headers=headers, data=data)

    # Mostrar la respuesta de la solicitud en la aplicación de Streamlit
    try:
        response_json = response.json()
    except ValueError:
        st.write('Respuesta no es un JSON:', response.text)
    else:
        st.write('Respuesta de la solicitud:', response_json)
else:
    st.write('No se encontró el parámetro "code" en la URL.')
