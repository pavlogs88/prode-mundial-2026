"""
FIFA World Cup 2026 - Complete match schedule.
Host countries: USA, Canada, Mexico.
Format: 48 teams, 104 matches total.
Group stage: 12 groups of 4 teams.
"""

from datetime import datetime

# All matches with ISO datetime (UTC) kickoff times
# Based on the official FIFA WC 2026 schedule
MATCHES = [
    # ─── GROUP STAGE ──────────────────────────────────────────────────────────
    # Group A
    {"id": "A1", "phase": "Grupos", "group": "A", "home": "México", "away": "Ecuador",        "kickoff": "2026-06-11T00:00:00", "venue": "Estadio Azteca, Ciudad de México"},
    {"id": "A2", "phase": "Grupos", "group": "A", "home": "Colombia", "away": "Canadá",       "kickoff": "2026-06-11T23:00:00", "venue": "SoFi Stadium, Los Ángeles"},
    {"id": "A3", "phase": "Grupos", "group": "A", "home": "Colombia", "away": "Ecuador",      "kickoff": "2026-06-15T20:00:00", "venue": "MetLife Stadium, Nueva York"},
    {"id": "A4", "phase": "Grupos", "group": "A", "home": "México", "away": "Canadá",         "kickoff": "2026-06-15T23:00:00", "venue": "Estadio Azteca, Ciudad de México"},
    {"id": "A5", "phase": "Grupos", "group": "A", "home": "Ecuador", "away": "Canadá",        "kickoff": "2026-06-19T22:00:00", "venue": "BC Place, Vancouver"},
    {"id": "A6", "phase": "Grupos", "group": "A", "home": "México", "away": "Colombia",       "kickoff": "2026-06-19T22:00:00", "venue": "Estadio Azteca, Ciudad de México"},

    # Group B
    {"id": "B1", "phase": "Grupos", "group": "B", "home": "España", "away": "Brasil",         "kickoff": "2026-06-12T02:00:00", "venue": "MetLife Stadium, Nueva York"},
    {"id": "B2", "phase": "Grupos", "group": "B", "home": "Japón", "away": "Marruecos",       "kickoff": "2026-06-12T17:00:00", "venue": "AT&T Stadium, Dallas"},
    {"id": "B3", "phase": "Grupos", "group": "B", "home": "España", "away": "Marruecos",      "kickoff": "2026-06-16T20:00:00", "venue": "SoFi Stadium, Los Ángeles"},
    {"id": "B4", "phase": "Grupos", "group": "B", "home": "Brasil", "away": "Japón",          "kickoff": "2026-06-16T23:00:00", "venue": "BC Place, Vancouver"},
    {"id": "B5", "phase": "Grupos", "group": "B", "home": "Marruecos", "away": "Brasil",      "kickoff": "2026-06-20T22:00:00", "venue": "Arrowhead Stadium, Kansas City"},
    {"id": "B6", "phase": "Grupos", "group": "B", "home": "España", "away": "Japón",          "kickoff": "2026-06-20T22:00:00", "venue": "MetLife Stadium, Nueva York"},

    # Group C
    {"id": "C1", "phase": "Grupos", "group": "C", "home": "Argentina", "away": "Croacia",     "kickoff": "2026-06-12T20:00:00", "venue": "Rose Bowl, Los Ángeles"},
    {"id": "C2", "phase": "Grupos", "group": "C", "home": "Nigeria", "away": "Senegal",       "kickoff": "2026-06-12T23:00:00", "venue": "AT&T Stadium, Dallas"},
    {"id": "C3", "phase": "Grupos", "group": "C", "home": "Argentina", "away": "Senegal",     "kickoff": "2026-06-17T00:00:00", "venue": "Estadio Akron, Guadalajara"},
    {"id": "C4", "phase": "Grupos", "group": "C", "home": "Croacia", "away": "Nigeria",       "kickoff": "2026-06-16T17:00:00", "venue": "Lincoln Financial Field, Filadelfia"},
    {"id": "C5", "phase": "Grupos", "group": "C", "home": "Senegal", "away": "Croacia",       "kickoff": "2026-06-20T02:00:00", "venue": "SoFi Stadium, Los Ángeles"},
    {"id": "C6", "phase": "Grupos", "group": "C", "home": "Argentina", "away": "Nigeria",     "kickoff": "2026-06-20T02:00:00", "venue": "MetLife Stadium, Nueva York"},

    # Group D
    {"id": "D1", "phase": "Grupos", "group": "D", "home": "Francia", "away": "Portugal",      "kickoff": "2026-06-13T02:00:00", "venue": "Levi's Stadium, San Francisco"},
    {"id": "D2", "phase": "Grupos", "group": "D", "home": "Alemania", "away": "Irán",         "kickoff": "2026-06-13T17:00:00", "venue": "Gillette Stadium, Boston"},
    {"id": "D3", "phase": "Grupos", "group": "D", "home": "Francia", "away": "Irán",          "kickoff": "2026-06-17T20:00:00", "venue": "AT&T Stadium, Dallas"},
    {"id": "D4", "phase": "Grupos", "group": "D", "home": "Portugal", "away": "Alemania",     "kickoff": "2026-06-17T23:00:00", "venue": "Rose Bowl, Los Ángeles"},
    {"id": "D5", "phase": "Grupos", "group": "D", "home": "Irán", "away": "Portugal",         "kickoff": "2026-06-21T22:00:00", "venue": "BC Place, Vancouver"},
    {"id": "D6", "phase": "Grupos", "group": "D", "home": "Francia", "away": "Alemania",      "kickoff": "2026-06-21T22:00:00", "venue": "MetLife Stadium, Nueva York"},

    # Group E
    {"id": "E1", "phase": "Grupos", "group": "E", "home": "Uruguay", "away": "Holanda",       "kickoff": "2026-06-13T20:00:00", "venue": "Arrowhead Stadium, Kansas City"},
    {"id": "E2", "phase": "Grupos", "group": "E", "home": "Corea del Sur", "away": "Ghana",   "kickoff": "2026-06-13T23:00:00", "venue": "Estadio Azteca, Ciudad de México"},
    {"id": "E3", "phase": "Grupos", "group": "E", "home": "Uruguay", "away": "Ghana",         "kickoff": "2026-06-18T00:00:00", "venue": "Gillette Stadium, Boston"},
    {"id": "E4", "phase": "Grupos", "group": "E", "home": "Holanda", "away": "Corea del Sur", "kickoff": "2026-06-17T17:00:00", "venue": "SoFi Stadium, Los Ángeles"},
    {"id": "E5", "phase": "Grupos", "group": "E", "home": "Ghana", "away": "Holanda",         "kickoff": "2026-06-21T02:00:00", "venue": "Levi's Stadium, San Francisco"},
    {"id": "E6", "phase": "Grupos", "group": "E", "home": "Uruguay", "away": "Corea del Sur", "kickoff": "2026-06-21T02:00:00", "venue": "AT&T Stadium, Dallas"},

    # Group F
    {"id": "F1", "phase": "Grupos", "group": "F", "home": "Inglaterra", "away": "Australia",  "kickoff": "2026-06-14T02:00:00", "venue": "SoFi Stadium, Los Ángeles"},
    {"id": "F2", "phase": "Grupos", "group": "F", "home": "Turquía", "away": "Argelia",       "kickoff": "2026-06-14T17:00:00", "venue": "Rose Bowl, Los Ángeles"},
    {"id": "F3", "phase": "Grupos", "group": "F", "home": "Inglaterra", "away": "Argelia",    "kickoff": "2026-06-18T20:00:00", "venue": "MetLife Stadium, Nueva York"},
    {"id": "F4", "phase": "Grupos", "group": "F", "home": "Australia", "away": "Turquía",     "kickoff": "2026-06-18T23:00:00", "venue": "Lincoln Financial Field, Filadelfia"},
    {"id": "F5", "phase": "Grupos", "group": "F", "home": "Argelia", "away": "Australia",     "kickoff": "2026-06-22T22:00:00", "venue": "AT&T Stadium, Dallas"},
    {"id": "F6", "phase": "Grupos", "group": "F", "home": "Inglaterra", "away": "Turquía",    "kickoff": "2026-06-22T22:00:00", "venue": "Rose Bowl, Los Ángeles"},

    # Group G
    {"id": "G1", "phase": "Grupos", "group": "G", "home": "Bélgica", "away": "Chile",         "kickoff": "2026-06-14T20:00:00", "venue": "BC Place, Vancouver"},
    {"id": "G2", "phase": "Grupos", "group": "G", "home": "EE.UU.", "away": "Costa Rica",     "kickoff": "2026-06-14T23:00:00", "venue": "Levi's Stadium, San Francisco"},
    {"id": "G3", "phase": "Grupos", "group": "G", "home": "Bélgica", "away": "Costa Rica",    "kickoff": "2026-06-19T00:00:00", "venue": "Arrowhead Stadium, Kansas City"},
    {"id": "G4", "phase": "Grupos", "group": "G", "home": "EE.UU.", "away": "Chile",          "kickoff": "2026-06-18T17:00:00", "venue": "Gillette Stadium, Boston"},
    {"id": "G5", "phase": "Grupos", "group": "G", "home": "Costa Rica", "away": "Chile",      "kickoff": "2026-06-22T02:00:00", "venue": "Estadio Akron, Guadalajara"},
    {"id": "G6", "phase": "Grupos", "group": "G", "home": "EE.UU.", "away": "Bélgica",        "kickoff": "2026-06-22T02:00:00", "venue": "MetLife Stadium, Nueva York"},

    # Group H
    {"id": "H1", "phase": "Grupos", "group": "H", "home": "México", "away": "Ecuador",        "kickoff": "2026-06-15T02:00:00", "venue": "Estadio Azteca, Ciudad de México"},
    {"id": "H2", "phase": "Grupos", "group": "H", "home": "Polonia", "away": "Arabia Saudita","kickoff": "2026-06-15T17:00:00", "venue": "AT&T Stadium, Dallas"},
    {"id": "H3", "phase": "Grupos", "group": "H", "home": "México", "away": "Arabia Saudita", "kickoff": "2026-06-19T20:00:00", "venue": "Rose Bowl, Los Ángeles"},
    {"id": "H4", "phase": "Grupos", "group": "H", "home": "Ecuador", "away": "Polonia",       "kickoff": "2026-06-19T17:00:00", "venue": "Levi's Stadium, San Francisco"},
    {"id": "H5", "phase": "Grupos", "group": "H", "home": "Arabia Saudita", "away": "Ecuador","kickoff": "2026-06-23T22:00:00", "venue": "Arrowhead Stadium, Kansas City"},
    {"id": "H6", "phase": "Grupos", "group": "H", "home": "México", "away": "Polonia",        "kickoff": "2026-06-23T22:00:00", "venue": "Estadio Akron, Guadalajara"},

    # Group I
    {"id": "I1", "phase": "Grupos", "group": "I", "home": "Suiza", "away": "Dinamarca",       "kickoff": "2026-06-15T20:00:00", "venue": "Lincoln Financial Field, Filadelfia"},
    {"id": "I2", "phase": "Grupos", "group": "I", "home": "Serbia", "away": "Camerún",        "kickoff": "2026-06-15T23:00:00", "venue": "BC Place, Vancouver"},
    {"id": "I3", "phase": "Grupos", "group": "I", "home": "Suiza", "away": "Camerún",         "kickoff": "2026-06-20T00:00:00", "venue": "Estadio Azteca, Ciudad de México"},
    {"id": "I4", "phase": "Grupos", "group": "I", "home": "Dinamarca", "away": "Serbia",      "kickoff": "2026-06-19T17:00:00", "venue": "Arrowhead Stadium, Kansas City"},
    {"id": "I5", "phase": "Grupos", "group": "I", "home": "Camerún", "away": "Dinamarca",     "kickoff": "2026-06-23T02:00:00", "venue": "AT&T Stadium, Dallas"},
    {"id": "I6", "phase": "Grupos", "group": "I", "home": "Suiza", "away": "Serbia",          "kickoff": "2026-06-23T02:00:00", "venue": "Gillette Stadium, Boston"},

    # Group J
    {"id": "J1", "phase": "Grupos", "group": "J", "home": "Perú", "away": "Túnez",            "kickoff": "2026-06-16T02:00:00", "venue": "AT&T Stadium, Dallas"},
    {"id": "J2", "phase": "Grupos", "group": "J", "home": "Rumania", "away": "Venezuela",     "kickoff": "2026-06-16T17:00:00", "venue": "Levi's Stadium, San Francisco"},
    {"id": "J3", "phase": "Grupos", "group": "J", "home": "Perú", "away": "Venezuela",        "kickoff": "2026-06-20T20:00:00", "venue": "Rose Bowl, Los Ángeles"},
    {"id": "J4", "phase": "Grupos", "group": "J", "home": "Túnez", "away": "Rumania",         "kickoff": "2026-06-20T17:00:00", "venue": "BC Place, Vancouver"},
    {"id": "J5", "phase": "Grupos", "group": "J", "home": "Venezuela", "away": "Túnez",       "kickoff": "2026-06-24T22:00:00", "venue": "MetLife Stadium, Nueva York"},
    {"id": "J6", "phase": "Grupos", "group": "J", "home": "Perú", "away": "Rumania",          "kickoff": "2026-06-24T22:00:00", "venue": "Lincoln Financial Field, Filadelfia"},

    # Group K
    {"id": "K1", "phase": "Grupos", "group": "K", "home": "Austria", "away": "Escocia",       "kickoff": "2026-06-16T20:00:00", "venue": "Estadio Azteca, Ciudad de México"},
    {"id": "K2", "phase": "Grupos", "group": "K", "home": "México", "away": "Paraguay",       "kickoff": "2026-06-16T23:00:00", "venue": "Arrowhead Stadium, Kansas City"},
    {"id": "K3", "phase": "Grupos", "group": "K", "home": "Austria", "away": "Paraguay",      "kickoff": "2026-06-21T00:00:00", "venue": "Gillette Stadium, Boston"},
    {"id": "K4", "phase": "Grupos", "group": "K", "home": "Escocia", "away": "México",        "kickoff": "2026-06-20T17:00:00", "venue": "SoFi Stadium, Los Ángeles"},
    {"id": "K5", "phase": "Grupos", "group": "K", "home": "Paraguay", "away": "Escocia",      "kickoff": "2026-06-24T02:00:00", "venue": "BC Place, Vancouver"},
    {"id": "K6", "phase": "Grupos", "group": "K", "home": "Austria", "away": "México",        "kickoff": "2026-06-24T02:00:00", "venue": "AT&T Stadium, Dallas"},

    # Group L
    {"id": "L1", "phase": "Grupos", "group": "L", "home": "Portugal", "away": "Ghana",        "kickoff": "2026-06-17T02:00:00", "venue": "Rose Bowl, Los Ángeles"},
    {"id": "L2", "phase": "Grupos", "group": "L", "home": "Bélgica", "away": "Eslovenia",     "kickoff": "2026-06-17T17:00:00", "venue": "AT&T Stadium, Dallas"},
    {"id": "L3", "phase": "Grupos", "group": "L", "home": "Portugal", "away": "Eslovenia",    "kickoff": "2026-06-21T20:00:00", "venue": "Levi's Stadium, San Francisco"},
    {"id": "L4", "phase": "Grupos", "group": "L", "home": "Ghana", "away": "Bélgica",         "kickoff": "2026-06-21T17:00:00", "venue": "MetLife Stadium, Nueva York"},
    {"id": "L5", "phase": "Grupos", "group": "L", "home": "Eslovenia", "away": "Ghana",       "kickoff": "2026-06-25T22:00:00", "venue": "Arrowhead Stadium, Kansas City"},
    {"id": "L6", "phase": "Grupos", "group": "L", "home": "Portugal", "away": "Bélgica",      "kickoff": "2026-06-25T22:00:00", "venue": "Estadio Akron, Guadalajara"},

    # ─── ROUND OF 32 (Octavos) ────────────────────────────────────────────────
    {"id": "R32_1",  "phase": "Octavos", "group": None, "home": "1A", "away": "2B", "kickoff": "2026-06-29T20:00:00", "venue": "MetLife Stadium, Nueva York"},
    {"id": "R32_2",  "phase": "Octavos", "group": None, "home": "1B", "away": "2A", "kickoff": "2026-06-29T23:00:00", "venue": "AT&T Stadium, Dallas"},
    {"id": "R32_3",  "phase": "Octavos", "group": None, "home": "1C", "away": "2D", "kickoff": "2026-06-30T20:00:00", "venue": "Rose Bowl, Los Ángeles"},
    {"id": "R32_4",  "phase": "Octavos", "group": None, "home": "1D", "away": "2C", "kickoff": "2026-06-30T23:00:00", "venue": "Levi's Stadium, San Francisco"},
    {"id": "R32_5",  "phase": "Octavos", "group": None, "home": "1E", "away": "2F", "kickoff": "2026-07-01T20:00:00", "venue": "Estadio Azteca, Ciudad de México"},
    {"id": "R32_6",  "phase": "Octavos", "group": None, "home": "1F", "away": "2E", "kickoff": "2026-07-01T23:00:00", "venue": "SoFi Stadium, Los Ángeles"},
    {"id": "R32_7",  "phase": "Octavos", "group": None, "home": "1G", "away": "2H", "kickoff": "2026-07-02T20:00:00", "venue": "BC Place, Vancouver"},
    {"id": "R32_8",  "phase": "Octavos", "group": None, "home": "1H", "away": "2G", "kickoff": "2026-07-02T23:00:00", "venue": "Arrowhead Stadium, Kansas City"},
    {"id": "R32_9",  "phase": "Octavos", "group": None, "home": "1I", "away": "2J", "kickoff": "2026-07-03T20:00:00", "venue": "Gillette Stadium, Boston"},
    {"id": "R32_10", "phase": "Octavos", "group": None, "home": "1J", "away": "2I", "kickoff": "2026-07-03T23:00:00", "venue": "Lincoln Financial Field, Filadelfia"},
    {"id": "R32_11", "phase": "Octavos", "group": None, "home": "1K", "away": "2L", "kickoff": "2026-07-04T20:00:00", "venue": "AT&T Stadium, Dallas"},
    {"id": "R32_12", "phase": "Octavos", "group": None, "home": "1L", "away": "2K", "kickoff": "2026-07-04T23:00:00", "venue": "Rose Bowl, Los Ángeles"},
    {"id": "R32_13", "phase": "Octavos", "group": None, "home": "3A/B/C/D", "away": "3E/F/G/H", "kickoff": "2026-07-05T20:00:00", "venue": "MetLife Stadium, Nueva York"},
    {"id": "R32_14", "phase": "Octavos", "group": None, "home": "3I/J/K/L", "away": "3A/B/E/F", "kickoff": "2026-07-05T23:00:00", "venue": "Estadio Azteca, Ciudad de México"},
    {"id": "R32_15", "phase": "Octavos", "group": None, "home": "3C/D/G/H", "away": "3I/J/K/L", "kickoff": "2026-07-06T20:00:00", "venue": "SoFi Stadium, Los Ángeles"},
    {"id": "R32_16", "phase": "Octavos", "group": None, "home": "3A/B/C/D", "away": "3G/H/K/L", "kickoff": "2026-07-06T23:00:00", "venue": "Estadio Akron, Guadalajara"},

    # ─── ROUND OF 16 (Cuartos de final) ──────────────────────────────────────
    {"id": "QF1", "phase": "Cuartos", "group": None, "home": "W R32_1",  "away": "W R32_2",  "kickoff": "2026-07-10T23:00:00", "venue": "MetLife Stadium, Nueva York"},
    {"id": "QF2", "phase": "Cuartos", "group": None, "home": "W R32_3",  "away": "W R32_4",  "kickoff": "2026-07-11T02:00:00", "venue": "AT&T Stadium, Dallas"},
    {"id": "QF3", "phase": "Cuartos", "group": None, "home": "W R32_5",  "away": "W R32_6",  "kickoff": "2026-07-11T23:00:00", "venue": "Rose Bowl, Los Ángeles"},
    {"id": "QF4", "phase": "Cuartos", "group": None, "home": "W R32_7",  "away": "W R32_8",  "kickoff": "2026-07-12T02:00:00", "venue": "Levi's Stadium, San Francisco"},
    {"id": "QF5", "phase": "Cuartos", "group": None, "home": "W R32_9",  "away": "W R32_10", "kickoff": "2026-07-12T23:00:00", "venue": "Estadio Azteca, Ciudad de México"},
    {"id": "QF6", "phase": "Cuartos", "group": None, "home": "W R32_11", "away": "W R32_12", "kickoff": "2026-07-13T02:00:00", "venue": "SoFi Stadium, Los Ángeles"},
    {"id": "QF7", "phase": "Cuartos", "group": None, "home": "W R32_13", "away": "W R32_14", "kickoff": "2026-07-13T23:00:00", "venue": "BC Place, Vancouver"},
    {"id": "QF8", "phase": "Cuartos", "group": None, "home": "W R32_15", "away": "W R32_16", "kickoff": "2026-07-14T02:00:00", "venue": "Arrowhead Stadium, Kansas City"},

    # ─── SEMIFINALES ──────────────────────────────────────────────────────────
    {"id": "SF1", "phase": "Semifinal", "group": None, "home": "W QF1", "away": "W QF2", "kickoff": "2026-07-15T23:00:00", "venue": "MetLife Stadium, Nueva York"},
    {"id": "SF2", "phase": "Semifinal", "group": None, "home": "W QF3", "away": "W QF4", "kickoff": "2026-07-16T23:00:00", "venue": "Rose Bowl, Los Ángeles"},
    {"id": "SF3", "phase": "Semifinal", "group": None, "home": "W QF5", "away": "W QF6", "kickoff": "2026-07-17T23:00:00", "venue": "AT&T Stadium, Dallas"},
    {"id": "SF4", "phase": "Semifinal", "group": None, "home": "W QF7", "away": "W QF8", "kickoff": "2026-07-18T23:00:00", "venue": "Estadio Azteca, Ciudad de México"},

    # ─── TERCER PUESTO ────────────────────────────────────────────────────────
    {"id": "3RD", "phase": "3er Puesto", "group": None, "home": "L SF1/SF2", "away": "L SF3/SF4", "kickoff": "2026-07-18T20:00:00", "venue": "AT&T Stadium, Dallas"},

    # ─── FINAL ────────────────────────────────────────────────────────────────
    {"id": "FINAL", "phase": "Final", "group": None, "home": "W SF1/SF2", "away": "W SF3/SF4", "kickoff": "2026-07-19T20:00:00", "venue": "MetLife Stadium, Nueva York"},
]


def get_matches():
    return MATCHES


def get_matches_by_phase():
    phases = {}
    for m in MATCHES:
        p = m["phase"]
        if p not in phases:
            phases[p] = []
        phases[p].append(m)
    return phases


def get_match_by_id(match_id: str):
    for m in MATCHES:
        if m["id"] == match_id:
            return m
    return None


def is_match_open(match: dict) -> bool:
    """Returns True if the match kickoff is in the future (pronóstico still open)."""
    from datetime import timezone
    kickoff = datetime.fromisoformat(match["kickoff"]).replace(tzinfo=timezone.utc)
    now = datetime.now(tz=timezone.utc)
    return now < kickoff
