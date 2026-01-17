import streamlit as st

def login_page():
    st.title("🔐 Login — EstudanteAI")
    st.caption("Acesso ao assistente educacional")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar", use_container_width=True):
            if username == "aluno" and password == "2026Aluno!":
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos")

