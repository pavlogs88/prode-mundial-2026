import streamlit as st
from auth import login_with_google, get_current_user, logout
from ui_components import render_header, render_footer

st.set_page_config(
    page_title="Prode Mundial 2026 🏆",
    page_icon="⚽",
    layout="wide"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

user = get_current_user()

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
        
        if st.button("🌐 Continuar con Google", type="primary", use_container_width=True):
            login_with_google()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Reglas de puntuación
    st.markdown("---")
    cols = st.columns(5)
    rules = [("3","resultado exacto"), ("1","ganador/empate"), ("1","goles de un equipo"), 
             ("0.5","diferencia de goles"), ("10","bonus goleador/MVP")]
    for col, (pts, label) in zip(cols, rules):
        with col:
            st.markdown(f'<div class="rule-card"><div class="rule-pts">{pts}</div><div class="rule-label">pts por {label}</div></div>', unsafe_allow_html=True)

else:
    render_header()
    st.markdown(f"**Bienvenido, {user['name']}** 👋", unsafe_allow_html=True)

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
