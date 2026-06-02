import streamlit as st
from matches import get_matches_by_phase, is_match_open
from database import save_resultado, get_all_resultados
from scoring import calc_match_points
from datetime import datetime, timezone


def render_resultados(user):
    st.markdown("## 📊 Resultados del Mundial")
    st.markdown("Acá se cargan los resultados reales de cada partido. Cualquier participante puede actualizarlos.")

    with st.spinner("Cargando resultados..."):
        resultados = get_all_resultados()

    phases = get_matches_by_phase()
    phase_order = ["Grupos", "Octavos", "Cuartos", "Semifinal", "3er Puesto", "Final"]

    for phase in phase_order:
        if phase not in phases:
            continue
        matches = phases[phase]

        # Only show phases that have started
        started = [m for m in matches if not is_match_open(m)]
        upcoming = [m for m in matches if is_match_open(m)]

        with st.expander(f"📋 {phase} ({len(started)} jugados / {len(upcoming)} pendientes)", expanded=(phase == "Grupos")):
            if not started:
                st.info("Aún no se jugaron partidos en esta fase.")
                continue

            for match in started:
                mid = match["id"]
                real = resultados.get(mid)
                kickoff_dt = datetime.fromisoformat(match["kickoff"]).replace(tzinfo=timezone.utc)
                kickoff_str = kickoff_dt.strftime("%d/%m %H:%M UTC")

                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
                with col1:
                    st.markdown(f"**{match['home']}** vs **{match['away']}**")
                    st.caption(f"📅 {kickoff_str}")

                if real:
                    with col2:
                        new_h = st.number_input("Local", min_value=0, max_value=30,
                                                value=real["home"], key=f"rh_{mid}", label_visibility="collapsed")
                    with col3:
                        st.markdown("<div style='text-align:center;padding-top:8px;font-weight:bold'>-</div>", unsafe_allow_html=True)
                    with col4:
                        new_a = st.number_input("Visit.", min_value=0, max_value=30,
                                                value=real["away"], key=f"ra_{mid}", label_visibility="collapsed")
                    with col5:
                        if st.button("✏️ Actualizar", key=f"upd_{mid}", use_container_width=True):
                            save_resultado(mid, new_h, new_a, user["email"])
                            st.success("✅ Actualizado!")
                            st.rerun()
                else:
                    with col2:
                        new_h = st.number_input("Local", min_value=0, max_value=30,
                                                value=0, key=f"rh_{mid}", label_visibility="collapsed")
                    with col3:
                        st.markdown("<div style='text-align:center;padding-top:8px;font-weight:bold'>-</div>", unsafe_allow_html=True)
                    with col4:
                        new_a = st.number_input("Visit.", min_value=0, max_value=30,
                                                value=0, key=f"ra_{mid}", label_visibility="collapsed")
                    with col5:
                        if st.button("💾 Cargar", key=f"upd_{mid}", use_container_width=True):
                            save_resultado(mid, new_h, new_a, user["email"])
                            st.success("✅ Cargado!")
                            st.rerun()

                st.markdown("---")
