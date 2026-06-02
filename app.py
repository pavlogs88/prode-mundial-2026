import streamlit as st
from auth import init_auth, get_current_user, logout, get_google_auth_url, process_login
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

# Handle OAuth callback — Google redirects back with ?code=...
query_params = st.query_params
code = query_params.get("code")

if code and not st.session_state.get("oauth_code_used") == code:
    with st.spinner("Iniciando sesión..."):
        process_login(code)
    # Clean the URL
    st.query_params.clear()
    st.rerun()

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

        auth_url = get_google_auth_url()
        st.markdown(f'''
            <a href="{auth_url}" target="_self">
                <button style="
                    width:100%;
                    padding:0.75rem 1rem;
                    background:white;
                    color:#333;
                    border:1px solid #ddd;
                    border-radius:8px;
                    font-size:1rem;
                    font-weight:600;
                    cursor:pointer;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    gap:10px;
                ">
                    <img src="https://www.google.com/favicon.ico" width="20"/>
                    Continuar con Google
                </button>
            </a>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Scoring rules
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
