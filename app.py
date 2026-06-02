import streamlit as st
from auth import init_auth, get_current_user, logout
from ui_components import render_header, render_footer
import uuid
from streamlit_oauth import OAuth2Component
import uuid

st.set_page_config(
    page_title="Prode Mundial 2026 🏆",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)


if "oauth_state" not in st.session_state:
    st.session_state.oauth_state = str(uuid.uuid4())

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

init_auth()
user = get_current_user()
render_header()

if not user:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">⚽ MUNDIAL 2026</div>
        <h1 class="hero-title">PRODE<br><span class="hero-accent">MUNDIAL</span></h1>
        <p class="hero-subtitle">Predicí los resultados, acumulá puntos<br>y ganá el torneo entre amigos.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Ingresá con tu cuenta Google")
        st.markdown("Compartí el link con tus amigos para que se unan al prode.")

        from streamlit_oauth import OAuth2Component

        CLIENT_ID = st.secrets.get("GOOGLE_CLIENT_ID", "")
        CLIENT_SECRET = st.secrets.get("GOOGLE_CLIENT_SECRET", "")
        REDIRECT_URI = st.secrets.get("REDIRECT_URI", "")

        if CLIENT_ID and CLIENT_SECRET and REDIRECT_URI:
            oauth2 = OAuth2Component(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                authorize_endpoint="https://accounts.google.com/o/oauth2/auth",
                token_endpoint="https://oauth2.googleapis.com/token",
                refresh_token_endpoint="https://oauth2.googleapis.com/token",
                revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
            )

            result = oauth2.authorize_button(
                name="Continuar con Google",
                icon="https://www.google.com.tw/favicon.ico",
                redirect_uri=REDIRECT_URI,
                scope="openid email profile",
                key="google_oauth_login",           # Cambié la key
                extras_params={"prompt": "select_account"},
                use_container_width=True,
                pkce="S256",
            )

            if result and "token" in result:
                from auth import process_login_token
                process_login_token(result["token"])
                st.rerun()
        else:
            st.error("❌ Faltan credenciales en secrets.toml")

        st.markdown('</div>', unsafe_allow_html=True)

    # Reglas de puntuación
    st.markdown("---")
    cols = st.columns(5)
    rules = [("3", "pts por resultado exacto"), ("1", "pt por acertar ganador/empate"),
             ("1", "pt por goles de un equipo"), ("0.5", "pts por diferencia de goles"),
             ("10", "pts bonus goleador/MVP final")]
    for col, (pts, label) in zip(cols, rules):
        with col:
            st.markdown(f'<div class="rule-card"><div class="rule-pts">{pts}</div><div class="rule-label">{label}</div></div>', unsafe_allow_html=True)

else:
    st.markdown(f'<p class="welcome-text">Bienvenido, <strong>{user.get("name", "Usuario")}</strong>! 👋</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["⚽ Mis Pronósticos", "🏆 Tabla de Posiciones", "📊 Resultados", "🌟 Bonus Final"])
    
    with tab1:
        from pages_modules.pronosticos import render_pronosticos
        render_pronosticos(user)
    with tab2:
        from pages_modules.tabla import render_tabla
        render_tabla()
    with tab3:
        from pages_modules.resultados import render_resultados
        render_resultados(user)
    with tab4:
        from pages_modules.bonus import render_bonus
        render_bonus(user)

    logout()

render_footer()
