import streamlit as st
from matches import get_matches_by_phase, is_match_open
from database import save_pronostico, get_pronosticos_user
from datetime import datetime, timezone


def render_pronosticos(user):
    user_id = user["id"]
    st.markdown("## ⚽ Mis Pronósticos")
    st.markdown("Ingresá tu pronóstico para cada partido antes de que empiece. Una vez que arranca, se cierra automáticamente.")

    # Load existing predictions
    with st.spinner("Cargando pronósticos..."):
        existing = get_pronosticos_user(user_id)

    phases = get_matches_by_phase()
    phase_order = ["Grupos", "Octavos", "Cuartos", "Semifinal", "3er Puesto", "Final"]

    for phase in phase_order:
        if phase not in phases:
            continue
        matches = phases[phase]

        with st.expander(f"📋 {phase}", expanded=(phase == "Grupos")):
            if phase == "Grupos":
                # Group by group letter
                groups = {}
                for m in matches:
                    g = m.get("group", "?")
                    groups.setdefault(g, []).append(m)
                for g, gmatches in sorted(groups.items()):
                    st.markdown(f"**Grupo {g}**")
                    _render_match_list(gmatches, existing, user_id)
            else:
                _render_match_list(matches, existing, user_id)


def _render_match_list(matches, existing, user_id):
    for match in matches:
        mid = match["id"]
        open_match = is_match_open(match)
        kickoff_dt = datetime.fromisoformat(match["kickoff"]).replace(tzinfo=timezone.utc)
        kickoff_str = kickoff_dt.strftime("%d/%m %H:%M UTC")

        pred = existing.get(mid, {})
        pred_home = pred.get("home", 0)
        pred_away = pred.get("away", 0)

        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
        with col1:
            status_icon = "🟢" if open_match else "🔴"
            st.markdown(f"{status_icon} **{match['home']}** vs **{match['away']}**")
            st.caption(f"📅 {kickoff_str} | 🏟️ {match['venue']}")

        if open_match:
            with col2:
                h = st.number_input("Local", min_value=0, max_value=20, value=pred_home, key=f"h_{mid}", label_visibility="collapsed")
            with col3:
                st.markdown("<div style='text-align:center;padding-top:8px;font-weight:bold'>-</div>", unsafe_allow_html=True)
            with col4:
                a = st.number_input("Visit.", min_value=0, max_value=20, value=pred_away, key=f"a_{mid}", label_visibility="collapsed")
            with col5:
                if st.button("💾 Guardar", key=f"save_{mid}", use_container_width=True):
                    save_pronostico(user_id, mid, h, a)
                    st.success("✅ Guardado!")
                    st.rerun()
        else:
            with col2:
                st.markdown(f"<div style='text-align:center;padding-top:8px'>{pred_home}</div>", unsafe_allow_html=True)
            with col3:
                st.markdown("<div style='text-align:center;padding-top:8px;font-weight:bold'>-</div>", unsafe_allow_html=True)
            with col4:
                st.markdown(f"<div style='text-align:center;padding-top:8px'>{pred_away}</div>", unsafe_allow_html=True)
            with col5:
                if pred:
                    st.markdown("<div style='color:#888;padding-top:8px'>🔒 Cerrado</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='color:#f44;padding-top:8px'>⚠️ Sin pronóstico</div>", unsafe_allow_html=True)

        st.markdown("---")
