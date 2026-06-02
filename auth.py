# auth.py
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_ANON_KEY"]
    )

def login_with_google():
    """Versión simplificada para debug"""
    st.info("🔄 Intentando redirigir a Google...")   # ← Esto debería verse
    
    supabase = get_supabase()
    
    try:
        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": st.secrets["REDIRECT_URI"]
            }
        })
        
        if response and response.url:
            st.success("URL generada correctamente")
            st.session_state.auth_url = response.url
            st.rerun()
        else:
            st.error("No se recibió URL de login")
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

def get_current_user():
    supabase = get_supabase()
    try:
        session = supabase.auth.get_session()
        if session and session.user:
            return {
                "id": session.user.id,
                "email": session.user.email,
                "name": session.user.user_metadata.get("name", "Usuario"),
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
