import streamlit as st
import json
import streamlit_authenticator as stauth


# ======================
# 1. Autenticación
# ======================
users = ['fabio', 'admin']
usernames = ['fabio', 'admin']
passwords = ['1234', 'abcd']  # ⚠️ cámbialos por contraseñas seguras

# Hashear contraseñas
hashed_passwords = stauth.Hasher(passwords).generate()

# Configurar autenticador
authenticator = stauth.Authenticate(
    {"usernames": {
        usernames[i]: {"name": users[i], "password": hashed_passwords[i]}
        for i in range(len(users))
    }},
    "psicotest", "abcdef", cookie_expiry_days=1
)

# Formulario de login
name, authentication_status, username = authenticator.login("Login", "main")

# ======================
# 2. Mostrar app solo si el login fue correcto
# ======================
if authentication_status:
    st.success(f"Bienvenido, {name} 👋")
    st.title("📋 Test Psicotécnico")
    
# Cargar preguntas desde JSON
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

#st.title("📋 Test Psicotécnico")

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

elif authentication_status is False:
    st.error("Usuario o contraseña incorrectos ❌")
elif authentication_status is None:
    st.warning("Por favor ingresa tus credenciales 🔑")
