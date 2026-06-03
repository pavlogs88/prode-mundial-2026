import streamlit as st
from supabase import create_client, Client
from database import get_or_create_user


@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_ANON_KEY"]
    )


def get_current_user():
    return st.session_state.get("user")


def process_supabase_session(access_token: str, refresh_token: str = ""):
    """Set Supabase session from tokens and extract user info."""
    try:
        supabase = get_supabase()
        session = supabase.auth.set_session(access_token, refresh_token)
        u = session.user
        if u:
            user = {
                "id": u.id,
                "email": u.email,
                "name": u.user_metadata.get("full_name") or u.user_metadata.get("name") or u.email.split("@")[0],
                "picture": u.user_metadata.get("avatar_url", ""),
            }
            get_or_create_user(user)
            st.session_state.user = user
    except Exception as e:
        st.error(f"Error procesando sesión: {e}")


def logout():
    try:
        get_supabase().auth.sign_out()
    except Exception:
        pass
    st.session_state.clear()
    st.rerun()
