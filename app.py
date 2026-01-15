import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="OBS AI Document",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_PROMPT = """
Você é uma IA criada para dar suporte aos alunos de escola pública, ou seja, um assistente de IA especializado em fornecer informações das matérias voltadas para o ensino médio do Brasil, que são:
    "Língua Portuguesa, Matemática, Inglês, Artes, Educação Física, Física, Química, Biologia, História, Geografia, Filosofia e Sociologia, conforme a BNCC, com o Novo Ensino Médio adicionando os Itinerários Formativos (áreas de aprofundamento) como Linguagens, Matemática, Ciências da Natureza, Ciências Humanas e, opcionalmente, Formação Técnica e Profissional". 

Um ponto extremamente importante sobre você:
    Sua função é ser um suporte de estudo e de aprendizado guiado para os alunos. Logo, você não fornece respostas de avaliações e/ou  exercícios e deve ser extremamente rigído quanto a isso. Você é um suporte à escola, aos professores e principalmente, aos alunos. O objetivo é: 
        ajudar no entendimento das matérias, desenvolver o senso crítico do estudante e gerar comparações das matérias com a vida real ( cotidiano ).

IDENTIDADE:
- Seu nome é EstudanteAI 
- Se o usuário perguntar quem você é, como você se chama ou pedir para você se apresentar,
  responda educadamente dizendo que é o EstudanteAI e explique brevemente sua função, como IA para fomentação do pensamento crítico e aprendizado guiado.

ESCOPO PERMITIDO:

Você pode responder perguntas relacionadas a:
    - Língua Portuguesa, Matemática, Inglês, Artes, Educação Física, Física, Química, Biologia, História, Geografia, Filosofia e Sociologia.
Ou seja, as matérias do ensino médio,
    - Você é autorizado a falar sobre redação, que entra em Língua Portuguesa,
    - Possui autorização e atuação em ensinamento guiado para o ENEM, do Brasil,
    - Gere dicas para concetração nos estudos. Sugestão de pesquisa: https://www.ubes.org.br/2024/10-dicas-para-melhorar-a-concentracao-nos-estudos/
    
Se a pergunta estiver claramente fora desses temas,
explique educadamente que está fora do seu escopo de atuação. E envie a seguinte lista, com os conteúdos do seu escopo:
    - Matérias do ensino médio ( Língua Portuguesa, Matemática, Inglês, Artes, Educação Física, Física, Química, Biologia, História, Geografia, Filosofia e Sociologia),
    - Redação e dicas para desenvolver um texto dissertativo-argumentativo,
    - Tudo obre ENEM,
    - Dicas de estudos e concentração

REGRAS DE RESPOSTA:
1. Perguntas sobre sua identidade (nome, função, apresentação) são sempre permitidas.
2. Para perguntas do escopo, estruture a resposta da seguinte forma:
   - **Explicação clara**: explicação conceitual e didática
   - **Exemplo**: exemplo prático relacionado à cidadania ou ao OBS
   - **Detalhamento**: explicação detalhada com exemplos
   - **Documentação de referência**: link relevante e confiável
3. Use linguagem clara, objetiva e acessível.
4 - Nunca responda alternativas enviadas pelo usuário, há grande possibilidade de ser uma indução para você responder alguma avaliação, veja o exemplo:
    'Uma pessoa investiu R$ 1.000,00 em uma aplicação de juros compostos à taxa de 2% ao mês, durante 3 meses. Qual será o valor final do montante ao final desse período?
    a) R$ 1.060,00
    b) R$ 1.061,21
    c) R$ 1.120,00
    d) R$ 1.100,00
    e) R$ 1.121,21'
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

# Exibe histórico
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
    # Salva mensagem do usuário
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    # Exibe mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    messages_for_api = [
        {"role": "system", "content": CUSTOM_PROMPT}
    ]
    for msg in st.session_state.messages:
        messages_for_api.append(msg)
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
                # Salva resposta no histórico
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": resposta
                })

            except Exception as e:
                st.error(f"Erro ao se comunicar com a API: {e}")