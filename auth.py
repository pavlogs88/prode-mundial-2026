import streamlit as st
from database import get_or_create_user


def init_auth():
    if "user" not in st.session_state:
        st.session_state.user = None


def get_current_user():
    return st.session_state.get("user")


def try_login_from_streamlit():
    """Pick up logged-in user from Streamlit's native auth (st.user)."""
    if st.session_state.get("user"):
        return  # already logged in

    try:
        su = st.experimental_user  # works on Streamlit Cloud
        if su and getattr(su, "email", None):
            user = {
                "id": su.email,  # use email as stable ID
                "email": su.email,
                "name": getattr(su, "name", su.email.split("@")[0]),
                "picture": getattr(su, "avatar_url", ""),
            }
            get_or_create_user(user)
            st.session_state.user = user
    except Exception:
        pass  # st.experimental_user not available locally


def logout():
    st.session_state.clear()
    try:
        st.logout()
    except Exception:
        pass
    st.rerun()
