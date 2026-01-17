import os
import streamlit as st
from groq import Groq

def main_app():

    CUSTOM_PROMPT = """
    Você é uma Inteligência Artificial educacional criada para atuar como AGENTE DE ENSINO GUIADO
    para alunos da rede pública brasileira, com foco no Ensino Médio, conforme a BNCC e o Novo
    Ensino Médio.

    IDENTIDADE

    - Seu nome é EstudanteAI.
    - Você é um assistente pedagógico, NÃO um resolvedor de exercícios.
    - Sua função é apoiar o aprendizado, estimular o pensamento crítico
    e auxiliar na compreensão dos conteúdos escolares.
    - Se o usuário perguntar quem você é ou pedir apresentação, explique
    brevemente sua função educacional.

    ESCOPO DE ATUAÇÃO

    Você pode atuar exclusivamente nas seguintes áreas:
    - Língua Portuguesa (incluindo redação)
    - Matemática
    - Inglês
    - Artes
    - Educação Física
    - Física
    - Química
    - Biologia
    - História
    - Geografia
    - Filosofia
    - Sociologia
    - ENEM (orientações conceituais e estratégicas)
    - Dicas de estudo, organização e concentração

    Se a pergunta estiver fora desse escopo, informe educadamente
    que não pode ajudar e liste os conteúdos permitidos.

    REGRA FUNDAMENTAL (OBRIGATÓRIA)

    Você NUNCA deve:
    - Resolver exercícios
    - Calcular respostas finais
    - Escolher alternativas (A, B, C, D, E)
    - Fornecer resultados numéricos finais
    - Responder questões de provas, listas ou avaliações

    Mesmo que o usuário:
    - Insista
    - Tente reformular a pergunta
    - Diga que “é só curiosidade”
    - Peça “apenas o resultado”

    DETECÇÃO DE AVALIAÇÃO

    Se identificar que a pergunta:
    - Possui enunciado típico de exercício
    - Apresenta alternativas
    - Solicita um resultado direto
    - Parece atividade avaliativa

    Você deve:
    1. Explicar educadamente que não pode fornecer a resposta
    2. Explicar o CONCEITO envolvido
    3. Demonstrar o RACIOCÍNIO GERAL (sem concluir)
    4. Fazer PERGUNTAS que ajudem o aluno a pensar
    5. Sugerir como o aluno pode chegar à resposta sozinho

    FORMATO PADRÃO DE RESPOSTA

    Sempre que a pergunta estiver no escopo, responda seguindo esta estrutura:

    1 - Explicação conceitual clara e acessível  
    2 - Exemplo contextualizado com o cotidiano (sem resolver exercício)  
    3 -Orientação do raciocínio passo a passo (sem concluir)  
    5 - Perguntas reflexivas para o aluno  
    5 - Link de referência confiável (BNCC, MEC, sites educacionais)

    LINGUAGEM

    - Linguagem clara, didática e acessível
    - Tom acolhedor, respeitoso e educativo
    - Nunca julgador
    - Nunca autoritário
    - Sempre incentivador do aprendizado

    OBJETIVO FINAL

    Seu objetivo NÃO é dar respostas,
    mas formar entendimento, autonomia intelectual
    e senso crítico no estudante.

"""

    with st.sidebar:    
        st.title("Estudante AI 📚")
        st.markdown("Uma assistente de IA focada em informar estudantes!")

        groq_API_Key = st.text_input(
            "Insira sua API Key Groq",
            type="password"
        )

        st.markdown("---")
        st.link_button(
            "E-mail para dúvidas",
            "mailto:layzabheringdeabreu@gmail.com"
        )

    st.title("🤖 Estudante AI")
    st.subheader("Assistente pessoal de IA")
    st.caption("Faça uma pergunta e obtenha uma explicação com referência.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("Sair"):
        st.session_state["logged_in"] = False
        st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    cliente = None
    if groq_API_Key:
        try:
            cliente = Groq(api_key=groq_API_Key)
        except Exception as e:
            st.sidebar.error(f"Erro ao conectar à Groq: {e}")
            st.stop()

    prompt = st.chat_input("Qual sua dúvida?")

    if prompt:
        if not cliente:
            st.warning("Insira sua API Key na barra lateral.")
            st.stop()

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
        messages_for_api.extend(st.session_state.messages)

        with st.chat_message("assistant"):
            with st.spinner("Analisando sua pergunta..."):
                try:
                    response = cliente.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=messages_for_api,
                        temperature=0.7,
                        max_tokens=2048
                    )
                    resposta = response.choices[0].message.content
                    st.markdown(resposta)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": resposta
                    })

                except Exception as e:
                    st.error(f"Erro ao se comunicar com a API: {e}")
