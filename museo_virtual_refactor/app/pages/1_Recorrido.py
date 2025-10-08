
import streamlit as st
from utils.data import load_metadata, DATA_PATH

data = load_metadata(DATA_PATH.stat().st_mtime)  # <-- fuerza recarga cuando cambie metadata.json

from components.card import obra_card


st.markdown("## Recorrido")
st.caption("Navega por todas las obras disponibles. Usa los filtros para personalizar el paseo.")

data = load_metadata()
ids = [o["id"] for o in data]
current = st.slider("Recorre el pasillo", min_value=min(ids), max_value=max(ids), value=min(ids), step=1, label_visibility="visible")

obra = next((o for o in data if o["id"]==current), None)
if obra:
    obra_card(obra)



