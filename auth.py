# auth.py
import streamlit as st
from supabase import create_client, Client
import urllib.parse

@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_ANON_KEY"]
    )

def handle_auth_callback():
    """Maneja el callback después de volver de Google"""
    supabase = get_supabase()
    try:
        # Intentar recuperar la sesión del callback
        session = supabase.auth.get_session()
        if session and session.user:
            st.session_state.user = {
                "id": session.user.id,
                "email": session.user.email,
                "name": session.user.user_metadata.get("name", session.user.email.split("@")[0]),
                "picture": session.user.user_metadata.get("avatar_url", "")
            }
            st.success(f"✅ Bienvenido, {st.session_state.user['name']}!")
            st.rerun()
    except:
        pass

def login_with_google():
    """Inicia login con Google"""
    if "user" in st.session_state:
        return

    supabase = get_supabase()
    
    try:
        with st.spinner("Redirigiendo a Google..."):
            response = supabase.auth.sign_in_with_oauth({
                "provider": "google",
                "options": {
                    "redirect_to": st.secrets["REDIRECT_URI"]
                }
            })
            
            if response and response.url:
                st.session_state.auth_url = response.url
                st.markdown(f"""
                    <meta http-equiv="refresh" content="0; url={response.url}">
                    <script>window.location.href = "{response.url}";</script>
                """, unsafe_allow_html=True)
            else:
                st.error("No se pudo generar la URL")
    except Exception as e:
        st.error(f"Error: {str(e)}")

def get_current_user():
    """Obtiene el usuario actual (mejorado)"""
    if "user" in st.session_state:
        return st.session_state.user

    supabase = get_supabase()
    handle_auth_callback()  # Intenta recuperar sesión del callback
    
    try:
        session = supabase.auth.get_session()
        if session and session.user:
            user_data = {
                "id": session.user.id,
                "email": session.user.email,
                "name": session.user.user_metadata.get("name", session.user.email.split("@")[0]),
                "picture": session.user.user_metadata.get("avatar_url", "")
            }
            st.session_state.user = user_data
            return user_data
    except:
        pass
    return None

def logout():
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
        supabase = get_supabase()
        supabase.auth.sign_out()
        if "user" in st.session_state:
            del st.session_state.user
        st.session_state.clear()
        st.rerun()
