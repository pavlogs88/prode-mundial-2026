"""
Scoring rules:
  - Resultado exacto:          3 pts
  - Acertar ganador/empate:    1 pt
  - Goles de un equipo exacto: 1 pt (home O away, max 2 pts)
  - Diferencia de goles:       0.5 pts extra
  - Bonus goleador del mundo:  10 pts
  - Bonus mejor jugador:       10 pts
"""

from typing import Optional


def calc_match_points(
    pred_home: int,
    pred_away: int,
    real_home: int,
    real_away: int,
) -> dict:
    points = 0.0
    breakdown = []

    # Resultado exacto
    if pred_home == real_home and pred_away == real_away:
        points += 3
        breakdown.append(("Resultado exacto", 3))
    else:
        # Ganador/empate
        pred_result = _result_sign(pred_home, pred_away)
        real_result = _result_sign(real_home, real_away)
        if pred_result == real_result:
            points += 1
            breakdown.append(("Ganador/Empate", 1))

        # Goles por equipo
        if pred_home == real_home:
            points += 1
            breakdown.append(("Goles local exacto", 1))
        if pred_away == real_away:
            points += 1
            breakdown.append(("Goles visitante exacto", 1))

        # Diferencia de goles
        if (pred_home - pred_away) == (real_home - real_away):
            points += 0.5
            breakdown.append(("Diferencia de goles", 0.5))

    return {"total": points, "breakdown": breakdown}


def calc_bonus_points(
    pred_goleador: str,
    pred_mejor: str,
    real_goleador: str,
    real_mejor: str,
) -> dict:
    points = 0.0
    breakdown = []

    if real_goleador and pred_goleador.strip().lower() == real_goleador.strip().lower():
        points += 10
        breakdown.append(("Goleador del mundial", 10))

    if real_mejor and pred_mejor.strip().lower() == real_mejor.strip().lower():
        points += 10
        breakdown.append(("Mejor jugador del mundial", 10))

    return {"total": points, "breakdown": breakdown}


def calc_leaderboard(
    all_pronosticos,  # DataFrame: user_id, match_id, home_goals, away_goals
    resultados: dict,  # {match_id: {home, away}}
    all_bonus,         # DataFrame: user_id, goleador, mejor_jugador
    bonus_results: dict,  # {goleador: str, mejor_jugador: str}
    users,             # DataFrame: id, name, email, picture
) -> list[dict]:
    """Returns list of {user_id, name, email, picture, match_pts, bonus_pts, total} sorted desc."""

    scores = {}

    # Match points
    for _, row in all_pronosticos.iterrows():
        uid = str(row["user_id"])
        mid = str(row["match_id"])
        if mid not in resultados:
            continue
        real = resultados[mid]
        res = calc_match_points(
            int(row["home_goals"]), int(row["away_goals"]),
            real["home"], real["away"]
        )
        if uid not in scores:
            scores[uid] = {"match_pts": 0.0, "bonus_pts": 0.0}
        scores[uid]["match_pts"] += res["total"]

    # Bonus points
    real_goleador = bonus_results.get("goleador", "")
    real_mejor = bonus_results.get("mejor_jugador", "")
    for _, row in all_bonus.iterrows():
        uid = str(row["user_id"])
        if uid not in scores:
            scores[uid] = {"match_pts": 0.0, "bonus_pts": 0.0}
        res = calc_bonus_points(
            str(row.get("goleador", "")),
            str(row.get("mejor_jugador", "")),
            real_goleador,
            real_mejor,
        )
        scores[uid]["bonus_pts"] += res["total"]

    # Build leaderboard
    user_map = {str(r["id"]): r for _, r in users.iterrows()}
    leaderboard = []
    for uid, pts in scores.items():
        u = user_map.get(uid, {})
        total = pts["match_pts"] + pts["bonus_pts"]
        leaderboard.append({
            "user_id": uid,
            "name": u.get("name", uid),
            "email": u.get("email", ""),
            "picture": u.get("picture", ""),
            "match_pts": pts["match_pts"],
            "bonus_pts": pts["bonus_pts"],
            "total": total,
        })

    leaderboard.sort(key=lambda x: x["total"], reverse=True)
    return leaderboard


def _result_sign(home: int, away: int) -> str:
    if home > away:
        return "H"
    elif away > home:
        return "A"
    return "D"
