import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

_client = None
_spreadsheet = None


def _get_client():
    global _client
    if _client is None:
        # Secrets stored as TOML section [GCP_SERVICE_ACCOUNT] — comes as dict directly
        creds_info = st.secrets["GCP_SERVICE_ACCOUNT"]
        creds = Credentials.from_service_account_info(dict(creds_info), scopes=SCOPES)
        _client = gspread.authorize(creds)
    return _client


def _get_spreadsheet():
    global _spreadsheet
    if _spreadsheet is None:
        sheet_id = st.secrets.get("SHEET_ID", "")
        if not sheet_id:
            raise ValueError("SHEET_ID not found in secrets")
        _spreadsheet = _get_client().open_by_key(sheet_id)
        _ensure_sheets(_spreadsheet)
    return _spreadsheet


def _ensure_sheets(spreadsheet):
    required = {
        "users": ["id", "email", "name", "picture", "created_at"],
        "pronosticos": ["user_id", "match_id", "home_goals", "away_goals", "timestamp"],
        "resultados": ["match_id", "home_goals", "away_goals", "updated_at", "updated_by"],
        "bonus": ["user_id", "goleador", "mejor_jugador", "timestamp"],
    }
    existing = {ws.title for ws in spreadsheet.worksheets()}
    for name, headers in required.items():
        if name not in existing:
            ws = spreadsheet.add_worksheet(title=name, rows=1000, cols=len(headers))
            ws.append_row(headers)


def _get_ws(name: str):
    return _get_spreadsheet().worksheet(name)


def get_or_create_user(user: dict):
    ws = _get_ws("users")
    data = ws.get_all_records()
    for row in data:
        if str(row["id"]) == str(user["id"]):
            return row
    ws.append_row([user["id"], user["email"], user["name"], user.get("picture", ""), datetime.utcnow().isoformat()])
    return user


def get_all_users() -> pd.DataFrame:
    ws = _get_ws("users")
    data = ws.get_all_records()
    return pd.DataFrame(data) if data else pd.DataFrame(columns=["id","email","name","picture","created_at"])


def save_pronostico(user_id, match_id, home_goals, away_goals):
    ws = _get_ws("pronosticos")
    data = ws.get_all_records()
    now = datetime.utcnow().isoformat()
    for i, row in enumerate(data, start=2):
        if str(row["user_id"]) == str(user_id) and str(row["match_id"]) == str(match_id):
            ws.update(f"C{i}:E{i}", [[home_goals, away_goals, now]])
            return
    ws.append_row([user_id, match_id, home_goals, away_goals, now])


def get_pronosticos_user(user_id) -> dict:
    ws = _get_ws("pronosticos")
    data = ws.get_all_records()
    return {
        str(row["match_id"]): {"home": int(row["home_goals"]), "away": int(row["away_goals"])}
        for row in data if str(row["user_id"]) == str(user_id)
    }


def get_all_pronosticos() -> pd.DataFrame:
    ws = _get_ws("pronosticos")
    data = ws.get_all_records()
    return pd.DataFrame(data) if data else pd.DataFrame(columns=["user_id","match_id","home_goals","away_goals","timestamp"])


def save_resultado(match_id, home_goals, away_goals, updated_by):
    ws = _get_ws("resultados")
    data = ws.get_all_records()
    now = datetime.utcnow().isoformat()
    for i, row in enumerate(data, start=2):
        if str(row["match_id"]) == str(match_id):
            ws.update(f"B{i}:E{i}", [[home_goals, away_goals, now, updated_by]])
            return
    ws.append_row([match_id, home_goals, away_goals, now, updated_by])


def get_all_resultados() -> dict:
    ws = _get_ws("resultados")
    data = ws.get_all_records()
    return {
        str(row["match_id"]): {"home": int(row["home_goals"]), "away": int(row["away_goals"])}
        for row in data if row["home_goals"] != ""
    }


def save_bonus(user_id, goleador, mejor_jugador):
    ws = _get_ws("bonus")
    data = ws.get_all_records()
    now = datetime.utcnow().isoformat()
    for i, row in enumerate(data, start=2):
        if str(row["user_id"]) == str(user_id):
            ws.update(f"B{i}:D{i}", [[goleador, mejor_jugador, now]])
            return
    ws.append_row([user_id, goleador, mejor_jugador, now])


def get_bonus_user(user_id) -> dict:
    ws = _get_ws("bonus")
    data = ws.get_all_records()
    for row in data:
        if str(row["user_id"]) == str(user_id):
            return {"goleador": row["goleador"], "mejor_jugador": row["mejor_jugador"]}
    return {}


def get_all_bonus() -> pd.DataFrame:
    ws = _get_ws("bonus")
    data = ws.get_all_records()
    return pd.DataFrame(data) if data else pd.DataFrame(columns=["user_id","goleador","mejor_jugador","timestamp"])
