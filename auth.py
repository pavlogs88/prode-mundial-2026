import streamlit as st
import requests
from database import get_or_create_user


def init_auth():
    if "user" not in st.session_state:
        st.session_state.user = None


def get_current_user():
    return st.session_state.get("user")


def process_login_token(token: dict):
    try:
        access_token = token.get("access_token")
        resp = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        resp.raise_for_status()
        info = resp.json()
        user = {
            "id": info["id"],
            "email": info["email"],
            "name": info.get("name", info["email"].split("@")[0]),
            "picture": info.get("picture", ""),
        }
        get_or_create_user(user)
        st.session_state.user = user
    except Exception as e:
        st.error(f"Error al iniciar sesión: {e}")


def logout():
    st.session_state.clear()
    st.rerun()
