# Museo Virtual — Bayron Gálvez (Streamlit)

## Cómo ejecutar
1. Instala dependencias:
   ```bash
   pip install streamlit streamlit-image-comparison pillow
   ```
2. Copia tus videos a `app/assets/videos/` y las imágenes a `app/assets/images/`.  
   Asegúrate de que los nombres coincidan con `app/data/metadata.json`.
3. Ejecuta:
   ```bash
   streamlit run app/MuseoVirtual.py
   ```

## Estructura
```
app/
  MuseoVirtual.py                # Portada
  /pages
    1_Recorrido.py              # Slider + vista general
    2_Salas_y_Temas.py          # Filtros por tema/año/búsqueda
    3_Cuestionario.py           # Quiz interactivo
    4_Créditos_y_Fuentes.py     # Créditos y metodología
  /components
    card.py                     # Tarjeta + ficha técnica + video
  /utils
    data.py                     # Carga/filtrado de metadata (cache)
  /data/metadata.json           # Catalogación de obras
  /assets/images                # Miniaturas (jpg/png)
  /assets/videos                # MP4 (H.264/AAC)
  /assets/audio                 # Audioguías opcionales
  /.streamlit/config.toml       # Tema y estilo
```

## Siguientes pasos sugeridos
- Añadir comparador Antes/Después (`streamlit-image-comparison`) en la ficha.
- Registrar vistas en SQLite para métricas.
- Extraer paleta de color y usarla como encabezado por obra.
- Agregar subtítulos `.vtt` y audioguías en ES/EN.