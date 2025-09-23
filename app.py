import streamlit as st
import json

# Cargar preguntas desde JSON
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

st.title("📋 Test Psicotécnico")

# Crear formulario
with st.form("test_form"):
    respuestas = {}
    
    for q in questions:
        st.markdown(f"**Pregunta {q['q']}: {q['text']}**")
        # Construir opciones
        opts = {opt["key"]: opt["text"] for opt in q["options"]}
        # Guardar selección
        respuestas[q["id"]] = st.radio(
            "Selecciona una opción:",
            options=list(opts.keys()),
            format_func=lambda x: opts[x],
            key=f"pregunta_{q['id']}"
        )
        st.write("---")
    
    # Botón para enviar
    submitted = st.form_submit_button("Enviar respuestas")

# Mostrar resultados al enviar
if submitted:
    st.success("✅ Respuestas enviadas correctamente.")
    st.json(respuestas)

