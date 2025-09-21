import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Test Psicotécnico 16PF", layout="wide")

# ==============================
# 1. Cargar preguntas JSON
# ==============================
@st.cache_data
def load_questions(json_file="questions.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        questions = json.load(f)
    return questions

questions = load_questions()

st.title("📘 Test Psicotécnico - 16PF")
st.write("Responde todas las preguntas. Al finalizar, haz clic en **Enviar** para ver tu reporte.")

# ==============================
# 2. Formulario dinámico
# ==============================
responses = {}
with st.form("test_form"):
    for q in questions:
        st.markdown(f"**Pregunta {q['q']}: {q['text']}**")
        opts = {opt["key"]: opt["text"] for opt in q["options"]}
        choice = st.radio(
            label=f"Seleccione una opción para la pregunta {q['q']}",
            options=list(opts.keys()),
            format_func=lambda x: opts[x],
            key=f"q{q['q']}"
        )
        responses[q["q"]] = choice

    submitted = st.form_submit_button("Enviar")

# ==============================
# 3. Reporte final
# ==============================
if submitted:
    results = []
    total_score = 0

    for q in questions:
        chosen_key = responses[q["q"]]
        chosen_opt = next(opt for opt in q["options"] if opt["key"] == chosen_key)
        results.append({
            "Pregunta": q["q"],
            "Factor": q.get("factor", ""),
            "Texto": q["text"],
            "Respuesta": chosen_opt["text"],
            "Puntaje": chosen_opt["score"]
        })
        total_score += chosen_opt["score"]

    df = pd.DataFrame(results)

    st.success("✅ ¡Test completado!")
    st.write("### 📊 Resultados")
    st.dataframe(df, use_container_width=True)

    st.metric("Puntaje Total", total_score)

    # Descargar reporte
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Descargar reporte en CSV",
        data=csv,
        file_name="reporte_16pf.csv",
        mime="text/csv"
    )
