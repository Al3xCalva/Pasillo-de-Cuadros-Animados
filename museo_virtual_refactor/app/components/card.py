import streamlit as st
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

def _resolve_asset(kind: str, name: str | None):
    if not name:
        return None
    base = BASE / "assets" / kind
    if not base.exists():
        return None

    # 1) intento directo (por si ya viene con extensión y mayúsculas)
    direct = base / name
    if direct.exists():
        return str(direct)

    # 2) búsqueda por stem (sin extensión), tolerante a mayúsculas
    stem = Path(name).stem.lower()
    exts_map = {
        "images": (".jpg", ".jpeg", ".png"),
        "videos": (".mp4", ".mov", ".m4v"),
        "audio":  (".mp3", ".wav", ".m4a", ".aac")
    }
    exts = exts_map.get(kind, ())
    for f in base.iterdir():
        if f.is_file() and f.stem.lower() == stem:
            if not exts or f.suffix.lower() in exts:
                return str(f)
    return None

def obra_card(obra):
    # Usa claves separadas para evitar el conflicto
    btn_key = f"btn_play_{obra['id']}"       # clave del botón
    state_key = f"playing_{obra['id']}"      # clave en session_state
    btn_audio_key = f"btn_audio_{obra['id']}"   # botón audio
    audio_state_key = f"audio_{obra['id']}"     # estado audio (mostrar reproductor)

    playing = st.session_state.get(state_key, False)
    show_audio = st.session_state.get(audio_state_key, False)

    with st.container(border=True):
        col_img, col_vid = st.columns([1, 1], vertical_alignment="top")
        st.markdown("""
<style>
.equal-media > div > img, .equal-media video {
    width: 100% !important;
    height: 380px !important;
    object-fit: cover !important;
    border-radius: 12px !important;
}
                    .mediaBox{
  position:relative; width:100%; aspect-ratio:16/9;
  border-radius:12px; overflow:hidden; background:#0f131a;
  border:1px solid rgba(255,255,255,.08);
}
.mediaBox img, .mediaBox video{
  position:absolute; inset:0;
  width:100% !important; height:100% !important;
  object-fit:cover !important;
}
.mediaBox .stVideo, .mediaBox .stVideo > div{ height:100% !important; width:100% !important; }
.mediaBox .stVideo video{ height:100% !important; width:100% !important; object-fit:cover !important; }
</style>
""", unsafe_allow_html=True)

        with col_img:
            img_path = _resolve_asset("images", obra.get("imagen"))
            st.markdown('<div class="equal-media">', unsafe_allow_html=True)
            if img_path:
                st.image(img_path, use_container_width=True)
            else:
                st.info("Miniatura no disponible. Agrega una imagen a **app/assets/images/**.")
            st.markdown('</div>', unsafe_allow_html=True)

            st.caption(f"{obra.get('tema','—')} · {obra.get('tecnica','—')}")
            st.caption(f"Duración: {obra.get('duracion','—')} s · Tamaño: {obra.get('peso_mb','—')} MB")

            if st.button("Ver animación", key=btn_key):
                st.session_state[state_key] = True
                playing = True
                st.rerun()
             # Botón: Escuchar voz de Bayron (audio)
            if st.button("Escuchar voz de Bayron", key=btn_audio_key):
                st.session_state[audio_state_key] = True
                show_audio = True
                st.rerun()

        # DERECHA: video (cuando está activo)
        with col_vid:
            st.markdown('<div class="equal-media">', unsafe_allow_html=True)
            if playing:
                vid_path = _resolve_asset("videos", obra.get("video"))
                if vid_path:
                    st.video(vid_path, format="video/mp4")
                else:
                    st.warning("No encontré el video en **app/assets/videos/**.")
            else:
                st.info("Pulsa **Ver animación** para reproducir el video aquí.")
            st.markdown('</div>', unsafe_allow_html=True)
        if show_audio:
            audio_name = obra.get("audio") or (obra.get("video") and Path(obra["video"]).stem)
            audio_path = _resolve_asset("audio", audio_name) if audio_name else None
            if audio_path:
                suf = Path(audio_path).suffix.lower()
                mime = {
                    ".mp3": "audio/mp3",
                    ".wav": "audio/wav",
                    ".m4a": "audio/mp4",
                    ".aac": "audio/aac",
                }.get(suf, None)
                if mime:
                    st.audio(audio_path, format=mime)
                else:
                    st.audio(audio_path)  # fallback
            else:
                st.warning(
                    "No encontré el archivo de audio. Colócalo en **app/assets/audio/** "
                    "y en `metadata.json` agrega la clave `\"audio\": \"archivo.mp3\"`."
                )

        # DEBAJO: sinopsis + ficha técnica
        st.markdown(f"*{obra.get('sinopsis','Sinopsis no disponible.')}*")
        with st.expander("Ficha técnica"):
            desc = obra.get("descripcion") or obra.get("sinopsis") or "Descripción no disponible."
            st.write(desc)


        rel = obra.get("relacionadas", [])
        if rel:
            st.caption("Relacionadas: " + ", ".join(f"#{x}" for x in rel))
