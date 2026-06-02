import streamlit as st
import requests
from database import get_or_create_user


def init_auth():
    if "user" not in st.session_state:
        st.session_state.user = None


def get_current_user():
    return st.session_state.get("user")


def process_login(token: dict):
    """Exchange token for user info and store in session."""
    try:
        access_token = token.get("access_token")
        resp = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        resp.raise_for_status()
        user_info = resp.json()

        user = {
            "id": user_info["id"],
            "email": user_info["email"],
            "name": user_info.get("name", user_info["email"].split("@")[0]),
            "picture": user_info.get("picture", ""),
        }

        # Persist user in Google Sheets DB
        get_or_create_user(user)
        st.session_state.user = user

    except Exception as e:
        st.error(f"Error al iniciar sesión: {e}")


def logout():
    st.session_state.user = None
    st.session_state.clear()
    st.rerun()
