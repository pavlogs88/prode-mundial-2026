import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_ANON_KEY"]
    )

def login_with_google():
    supabase = get_supabase()
    redirect_url = st.secrets["REDIRECT_URI"] + "/callback"   # ← Importante: /callback

    try:
        response = supabase.auth.sign_in_with_oauth(
            provider="google",
            options={
                "redirect_to": redirect_url,
            }
        )
        st.markdown(f'<meta http-equiv="refresh" content="0; url={response.url}">', unsafe_allow_html=True)
        st.stop()
    except Exception as e:
        st.error(f"Error generando login: {e}")

def process_supabase_session(access_token: str, refresh_token: str = None):
    supabase = get_supabase()
    try:
        supabase.auth.set_session(access_token, refresh_token)
        st.session_state.user = get_current_user()
    except Exception as e:
        st.error(f"Error procesando sesión: {e}")

def get_current_user():
    supabase = get_supabase()
    try:
        user = supabase.auth.get_user()
        if user and user.user:
            return {
                "id": user.user.id,
                "email": user.user.email,
                "name": user.user.user_metadata.get("full_name") or user.user.email.split("@")[0],
                "picture": user.user.user_metadata.get("avatar_url", "")
            }
    except:
        pass
    return None

def logout():
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
        get_supabase().auth.sign_out()
        st.session_state.clear()
        st.rerun()
