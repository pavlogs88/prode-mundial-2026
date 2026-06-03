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
    res = supabase.auth.sign_in_with_oauth(
        provider="google",
        options={"redirect_to": st.secrets["REDIRECT_URI"]}
    )
    st.markdown(f'<meta http-equiv="refresh" content="0; url={res.url}">', unsafe_allow_html=True)
    st.stop()

def get_current_user():
    supabase = get_supabase()
    try:
        # Intentar recuperar sesión
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
    if st.sidebar.button("🚪 Cerrar Sesión"):
        supabase = get_supabase()
        supabase.auth.sign_out()
        st.session_state.clear()
        st.rerun()
