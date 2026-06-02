import streamlit as st
from auth import init_auth, get_current_user, logout
from ui_components import render_header, render_footer

st.set_page_config(
    page_title="Prode Mundial 2026 🏆",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
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
        import os

        CLIENT_ID = st.secrets.get("GOOGLE_CLIENT_ID", "")
        CLIENT_SECRET = st.secrets.get("GOOGLE_CLIENT_SECRET", "")
        REDIRECT_URI = st.secrets.get("REDIRECT_URI", "http://localhost:8501")

        if CLIENT_ID and CLIENT_SECRET:
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
                key="google_oauth",
                extras_params={"prompt": "consent", "access_type": "offline"},
                use_container_width=True,
            )

            if result and "token" in result:
                from auth import process_login
                process_login(result["token"])
                st.rerun()
        else:
            st.warning("⚠️ Configurá las credenciales de Google en `.streamlit/secrets.toml`")
            st.code("""
# .streamlit/secrets.toml
GOOGLE_CLIENT_ID = "tu-client-id"
GOOGLE_CLIENT_SECRET = "tu-client-secret"
REDIRECT_URI = "https://tu-app.streamlit.app"
SHEET_ID = "tu-google-sheet-id"
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    # Show scoring rules
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown('<div class="rule-card"><div class="rule-pts">3</div><div class="rule-label">pts por resultado exacto</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="rule-card"><div class="rule-pts">1</div><div class="rule-label">pt por acertar ganador/empate</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="rule-card"><div class="rule-pts">1</div><div class="rule-label">pt por goles de un equipo</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="rule-card"><div class="rule-pts">0.5</div><div class="rule-label">pts por diferencia de goles</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="rule-card"><div class="rule-pts">10</div><div class="rule-label">pts bonus goleador/MVP final</div></div>', unsafe_allow_html=True)

else:
    # Logged in - show main navigation
    st.markdown(f'<p class="welcome-text">Bienvenido, <strong>{user["name"]}</strong>! 👋</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["⚽ Mis Pronósticos", "🏆 Tabla de Posiciones", "📊 Resultados", "🌟 Bonus Final"])

    with tab1:
        from pages.pronosticos import render_pronosticos
        render_pronosticos(user)

    with tab2:
        from pages.tabla import render_tabla
        render_tabla()

    with tab3:
        from pages.resultados import render_resultados
        render_resultados(user)

    with tab4:
        from pages.bonus import render_bonus
        render_bonus(user)

render_footer()
