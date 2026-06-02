# utils/auth.py
import streamlit as st

def login():
    """Login nativo con Google (recomendado)"""
    
    if "user" not in st.session_state:
        # Intenta hacer login con Google
        user = st.login(
            provider="google",
            redirect_uri=st.secrets["auth"]["redirect_uri"]
        )
        
        if user is not None:
            st.session_state.user = user
            st.rerun()
        else:
            st.stop()  # Detiene hasta que se loguee
    
    return st.session_state.user


def logout():
    """Cerrar sesión"""
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.clear()
        st.rerun()
