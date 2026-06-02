import streamlit as st
from auth import init_auth, get_current_user, logout
from ui_components import render_header, render_footer

st.set_page_config(
    page_title="Prode Mundial 2026 🏆",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==================== LOGIN NATIVO GOOGLE ====================
init_auth()

if "user" not in st.session_state or st.session_state.user is None:
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
        
        # Login nativo de Streamlit
        if st.button("🌐 Continuar con Google", type="primary", use_container_width=True):
            st.login(provider="google")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Reglas de puntuación
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
    user = get_current_user()
    render_header()
    
    st.markdown(f'<p class="welcome-text">Bienvenido, <strong>{user.get("name", user.get("email", "Usuario"))}</strong>! 👋</p>', unsafe_allow_html=True)
    
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

    logout()  # Botón de cerrar sesión

render_footer()
