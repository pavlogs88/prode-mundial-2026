import streamlit as st
import pandas as pd
from database import get_all_pronosticos, get_all_resultados, get_all_users, get_all_bonus
from scoring import calc_leaderboard

# Bonus results placeholder — admin sets via secrets or manual
BONUS_RESULTS_KEY = "bonus_results"


def render_tabla():
    st.markdown("## 🏆 Tabla de Posiciones")

    with st.spinner("Calculando puntos..."):
        try:
            pronosticos = get_all_pronosticos()
            resultados = get_all_resultados()
            users = get_all_users()
            bonus_df = get_all_bonus()
            bonus_results = st.session_state.get(BONUS_RESULTS_KEY, {"goleador": "", "mejor_jugador": ""})

            leaderboard = calc_leaderboard(pronosticos, resultados, bonus_df, bonus_results, users)
        except Exception as e:
            st.error(f"Error cargando datos: {e}")
            return

    if not leaderboard:
        st.info("Aún no hay pronósticos cargados. ¡Invitá a tus amigos!")
        return

    # Medals for top 3
    medals = ["🥇", "🥈", "🥉"]

    for i, row in enumerate(leaderboard):
        medal = medals[i] if i < 3 else f"#{i+1}"
        pic = row.get("picture", "")

        col1, col2, col3, col4, col5 = st.columns([0.5, 0.5, 3, 2, 2])
        with col1:
            st.markdown(f"<div class='rank-badge'>{medal}</div>", unsafe_allow_html=True)
        with col2:
            if pic:
                st.image(pic, width=40)
        with col3:
            st.markdown(f"**{row['name']}**")
            st.caption(row['email'])
        with col4:
            st.markdown(f"⚽ Partidos: **{row['match_pts']:.1f}** pts")
            st.markdown(f"🌟 Bonus: **{row['bonus_pts']:.1f}** pts")
        with col5:
            st.markdown(f"<div class='total-pts'>{row['total']:.1f} pts</div>", unsafe_allow_html=True)

        st.markdown("---")

    # Show as dataframe too
    with st.expander("📊 Ver como tabla"):
        df = pd.DataFrame(leaderboard)[["name", "match_pts", "bonus_pts", "total"]]
        df.columns = ["Jugador", "Puntos Partidos", "Bonus", "Total"]
        df.index = range(1, len(df) + 1)
        st.dataframe(df, use_container_width=True)
