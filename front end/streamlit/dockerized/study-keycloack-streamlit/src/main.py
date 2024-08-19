from dataclasses import asdict
import streamlit as st
from streamlit_keycloak import login

st.title('Keycloack Login')

keycloak = login(
    url="http://localhost:3333/auth",
    realm="myrealm",
    client_id="myclient",
    init_options={
        "checkLoginIframe": False
    },
    custom_labels={
        "labelButton": "Sign in",
        "labelLogin": "Please sign in to your account.",
        "errorNoPopup": "Unable to open the authentication popup. Allow popups and refresh the page to proceed.",
        "errorPopupClosed": "Authentication popup was closed manually.",
        "errorFatal": "Unable to connect to Keycloak using the current configuration."   
    }
)

if keycloak.authenticated:
    st.subheader(f"Welcome {keycloak.user_info['preferred_username']}!")
    st.write(f"Here is your user information:")
    st.write(asdict(keycloak))
