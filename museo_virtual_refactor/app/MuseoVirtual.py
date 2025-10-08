import streamlit as st
from pathlib import Path
from utils.data import load_metadata, DATA_PATH
data = load_metadata(DATA_PATH.stat().st_mtime)


st.set_page_config(
    page_title="Museo Virtual — Bayron Gálvez",
    page_icon="🎨",
    layout="wide"
)

BASE = Path(__file__).resolve().parent  # .../app

def resolve_asset(kind: str, name: str | None):
    """Devuelve una ruta existente dentro de assets/<kind>/ probando extensiones comunes."""
    if not name:
        return None
    p = BASE / "assets" / kind / name
    if p.exists():
        return str(p)
    stem = Path(name).stem
    for ext in (".jpg", ".jpeg", ".png") if kind == "images" else (".mp4", ".mov", ".m4v"):
        alt = BASE / "assets" / kind / f"{stem}{ext}"
        if alt.exists():
            return str(alt)
    return None

# ---------- ESTILOS SUAVES ----------
st.markdown("""
<style>
.hero { padding: 2.2rem 2.4rem; border-radius: 18px;
  background: radial-gradient(1200px 600px at 20% -10%, rgba(255,255,255,0.06), transparent),
              linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.08);
}
.hero h1 { font-size: 2.2rem; margin: 0 0 .5rem 0; }
.kicker { color: #9CA3AF; letter-spacing: .06em; text-transform: uppercase; font-size: .85rem;}
.badge { display:inline-block; padding:.3rem .6rem; border-radius:999px;
  background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.08);
  font-size:.85rem; margin-right:.35rem; }
.card { border-radius: 16px; padding: .8rem; background: rgba(255,255,255,.02);
  border: 1px solid rgba(255,255,255,.06); }
.placeholder { height: 160px; border-radius: 12px;
  border:1px dashed rgba(255,255,255,.18); display:flex; align-items:center; justify-content:center;
  opacity:.75; }
.footer { opacity:.75; font-size:.9rem; border-top:1px solid rgba(255,255,255,.08);
  padding-top:1rem; margin-top:1.5rem; }

</style>
            
"""
, unsafe_allow_html=True)

data = load_metadata()
temas = sorted({o.get("tema","—") for o in data})
anios = [o.get("anio") for o in data if o.get("anio")]
periodo = f"{min(anios)}–{max(anios)}" if anios else "—"

# ---------- HERO ----------
with st.container():
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown('<div class="kicker">Homenaje académico</div>', unsafe_allow_html=True)
    st.markdown("<h1>🎨 Museo Virtual — Pasillo de Cuadros Animados</h1>", unsafe_allow_html=True)
    st.write(
        "Una visita guiada a la obra de **Bayron Gálvez**, donde las pinturas cobran vida mediante "
        "**animación asistida por IA**. Explora los temas, recorre el pasillo y conoce el proceso creativo."
    )

    # CTA (si tienes Streamlit >=1.31 usa page_link; sino, activa el bloque fallback)
    try:
        st.page_link("pages/1_Recorrido.py", label="Iniciar recorrido")
    except Exception:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Iniciar recorrido"):
                st.switch_page("pages/1_Recorrido.py")
        with col_b:
            if st.button("Salas y temas"):
                st.switch_page("pages/2_Salas_y_Temas.py")

    st.markdown(
        f'<span class="badge">Obras: {len(data)}</span>'
        f'<span class="badge">Videos: {sum(1 for o in data if o.get("estado")=="disponible")}</span>'
        f'<span class="badge">Temas: {len(temas)}</span>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ---------- DESTACADOS (SEGURO, SIN CRASHEAR) ----------
st.subheader("Obras destacadas")
cols = st.columns(3)
featured = (data[:3] if len(data) >= 3 else data)

for col, obra in zip(cols, featured):
    with col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        img_path = resolve_asset("images", obra.get("imagen"))
        if img_path:
            st.image(img_path, use_container_width=True)
        else:
            st.markdown('<div class="placeholder">Miniatura no disponible</div>', unsafe_allow_html=True)

        st.markdown(f"**{obra.get('titulo','Obra')}**  {obra.get('anio','')}")
        st.caption(f"{obra.get('tema','—')} · {obra.get('tecnica','—')}")
        if st.button("Ver en el recorrido", key=f"goto_{obra['id']}"):
            st.session_state["current_id"] = obra["id"]
            st.switch_page("pages/1_Recorrido.py")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- SOBRE EL PROYECTO ----------
with st.expander("ℹ️ Sobre el proyecto"):
    st.write(
        "Este museo virtual presenta animaciones derivadas de pinturas, cuidando la fidelidad cromática y "
        "la textura pictórica. Incluye **fichas técnicas**, **textos curatoriales**, **audioguía** y un "
        "**cuestionario** para reforzar el aprendizaje. El proyecto se desarrolla con Streamlit y buenas "
        "prácticas de compresión de video (H.264/AAC)."
    )

# ---------- INVENTARIO ----------

st.markdown('<div class="footer">Proyecto educativo sin fines de lucro. ', unsafe_allow_html=True)
