import streamlit as st

st.markdown("## 📝 Cuestionario de visita")
st.caption("Responde para comprobar tu comprensión del recorrido.")

preguntas = [
    {
        "q": "¿Qué tema recorre con mayor frecuencia la obra seleccionada?",
        "options": ["Figura", "Paisaje", "Abstracción"],
        "answer": 0,
        "explain": "En esta curaduría de ejemplo, el foco está puesto en la figura y el movimiento."
    },
    {
        "q": "Selecciona un elemento cromático característico en los cuadros animados",
        "options": ["Gamas frías y neutras", "Rojos y ocres vibrantes", "Monocromo azul"],
        "answer": 1,
        "explain": "Los rojos y ocres refuerzan el dinamismo y la corporeidad."
    },
    {
        "q": "¿Qué técnica pictórica se utiliza con mayor frecuencia en la exposición?",
        "options": ["Óleo sobre tela", "Acuarela", "Grafito sobre papel"],
        "answer": 0,
        "explain": "El óleo sobre tela permite lograr mayor profundidad y saturación cromática."
    },
     {
        "q": "¿Qué tipo de fondo predomina en las composiciones?",
        "options": ["Fondos neutros y planos", "Paisajes detallados", "Espacios urbanos"],
        "answer": 0,
        "explain": "Los fondos neutros permiten resaltar la presencia y el movimiento de las figuras."
    },
    {
        "q": "¿Qué elemento visual destaca en la mayoría de las obras?",
        "options": ["El uso del espacio negativo", "La repetición de formas humanas", "El contraste entre luz y sombra"],
        "answer": 1,
        "explain": "La figura humana se repite como motivo principal en distintos contextos visuales."
    },
   
  
]

score = 0
for i, p in enumerate(preguntas, start=1):
    st.markdown(f"**{i}. {p['q']}**")
    pick = st.radio("Elige una opción", p["options"], index=None, key=f"q{i}")
    if pick is not None:
        if p["options"].index(pick) == p["answer"]:
            score += 1
            st.success("✔️ Correcto")
        else:
            st.error("✖️ Incorrecto")
        st.caption(p["explain"])
    st.divider()

st.metric("Puntaje", f"{score}/{len(preguntas)}")
