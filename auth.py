import streamlit as st
from supabase import create_client, Client


def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_ANON_KEY"]
    )

def login_with_google():
    response = supabase.auth.sign_in_with_oauth(
        provider="google",
        options={
            "redirect_to":
            "https://mundial2026-loschangos.streamlit.app"
        }
    )
    
    st.markdown(f'<meta http-equiv="refresh" content="0; url={response.url}">', unsafe_allow_html=True)
    st.stop()

def process_supabase_session(access_token, refresh_token=None):
    if not access_token:
        return
    try:
        supabase = get_supabase()
        supabase.auth.set_session(access_token, refresh_token)
        st.session_state.user = get_current_user()
        st.success("✅ Login exitoso!")
    except Exception as e:
        st.error(f"Error en sesión: {e}")

def get_current_user():
    supabase = get_supabase()

    try:
        user = supabase.auth.get_user()

        if user and user.user:
            return {
                "id": user.user.id,
                "email": user.user.email,
                "name": user.user.user_metadata.get("full_name")
                        or user.user.email.split("@")[0],
                "picture": user.user.user_metadata.get("avatar_url", "")
            }

    except Exception as e:
        st.error(f"GET USER ERROR: {e}")

    return None

def logout():
    if st.sidebar.button("🚪 Cerrar Sesión"):
        get_supabase().auth.sign_out()
        st.session_state.clear()
        st.rerun()
