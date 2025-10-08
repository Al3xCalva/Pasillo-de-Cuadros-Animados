# app/utils/data.py
import json, pathlib
import streamlit as st

DATA_PATH = pathlib.Path(__file__).resolve().parent.parent / "data" / "metadata.json"

@st.cache_data
def load_metadata(cache_bust: float = 0.0):
    """Carga el catálogo. cache_bust debe ser DATA_PATH.stat().st_mtime para refrescar al cambiar el archivo."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def filter_obras(data, tema="Todos", anio_rango=(1900, 2100), texto=""):
    q = (texto or "").lower()
    def _ok(o):
        ok_tema = tema == "Todos" or o.get("tema") == tema
        anio = o.get("anio") or 0
        ok_anio = anio_rango[0] <= anio <= anio_rango[1]
        blob = " ".join([o.get("titulo",""), o.get("sinopsis",""), o.get("tecnica","")]).lower()
        ok_q = q in blob
        return ok_tema and ok_anio and ok_q
    return [o for o in data if _ok(o)]
