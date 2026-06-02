# auth.py
import streamlit as st
from supabase import create_client, Client
from datetime import datetime

@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_ANON_KEY"]
    )

def login_with_google():
    """Inicia login con Google usando Supabase"""
    supabase = get_supabase()
    
    if "user" not in st.session_state:
        # Redirigir a login de Supabase con Google
        res = supabase.auth.sign_in_with_oauth(
            provider="google",
            options={"redirect_to": st.secrets["REDIRECT_URI"]}
        )
        st.session_state.auth_url = res.url
        st.rerun()

def get_current_user():
    supabase = get_supabase()
    try:
        session = supabase.auth.get_session()
        if session and session.user:
            return {
                "id": session.user.id,
                "email": session.user.email,
                "name": session.user.user_metadata.get("name", session.user.email.split("@")[0]),
                "picture": session.user.user_metadata.get("avatar_url", "")
            }
    except:
        pass
    return None

def logout():
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
        supabase = get_supabase()
        supabase.auth.sign_out()
        st.session_state.clear()
        st.rerun()
