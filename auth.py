import streamlit as st
import requests
from database import get_or_create_user
import urllib.parse
import hashlib
import os


def init_auth():
    if "user" not in st.session_state:
        st.session_state.user = None


def get_current_user():
    return st.session_state.get("user")


def get_google_auth_url() -> str:
    client_id = st.secrets.get("GOOGLE_CLIENT_ID", "")
    redirect_uri = st.secrets.get("REDIRECT_URI", "http://localhost:8501")
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    return "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode(params)


def exchange_code_for_token(code: str) -> dict:
    client_id = st.secrets.get("GOOGLE_CLIENT_ID", "")
    client_secret = st.secrets.get("GOOGLE_CLIENT_SECRET", "")
    redirect_uri = st.secrets.get("REDIRECT_URI", "http://localhost:8501")

    resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def get_user_info(access_token: str) -> dict:
    resp = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def process_login(code: str):
    try:
        token = exchange_code_for_token(code)
        user_info = get_user_info(token["access_token"])
        user = {
            "id": user_info["id"],
            "email": user_info["email"],
            "name": user_info.get("name", user_info["email"].split("@")[0]),
            "picture": user_info.get("picture", ""),
        }
        get_or_create_user(user)
        st.session_state.user = user
        st.session_state.oauth_code_used = code
    except Exception as e:
        st.error(f"Error al iniciar sesión: {e}")


def logout():
    st.session_state.clear()
    st.rerun()
