import streamlit as st
import json

# Cargar preguntas desde JSON
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

st.title("📋 Test Psicotécnico")

# Diccionario para guardar respuestas
respuestas = {}

# Crear formulario
with st.form("test_form"):
    for q in questions:
        st.markdown(f"**Pregunta {q['id']}: {q['text']}**")  # 👈 cambiado 'q' → 'id'
        opts = {opt["key"]: opt["text"] for opt in q["options"]}
        choice = st.radio(
            label=f"Seleccione una opción para la pregunta {q['id']}",
            options=list(opts.keys()),
            format_func=lambda x: opts[x],
            key=f"pregunta_{q['id']}",
            index=None  # No preselecciona nada
        )
        respuestas[q["id"]] = choice

    # Botón de envío
    submitted = st.form_submit_button("Enviar")

# Mostrar resultados
if submitted:
    st.success("✅ Respuestas enviadas correctamente.")
    st.json(respuestas)
