import streamlit as st
from src.agent.react import react_agent

st.set_page_config(page_title="Agente ReAct Docs", page_icon="🤖", layout="wide")

st.title("🤖 Agente ReAct - Documentação Automática")
st.markdown("Bem-vindo! Este agente lê seu código/projeto e interage com Git usando o paradigma **Reasoning + Acting (ReAct)**.")

st.sidebar.title("Opções")
task_input = st.sidebar.text_area("Descreva a Tarefa:", value="gere a documentação técnica deste código detalhadamente", height=150)

uploaded = st.file_uploader("Envie um arquivo base (.py, .txt, .md)")

if uploaded:
    code = uploaded.read().decode("utf-8")
    
    with st.spinner("O Agente está pensando e executando ferramentas... (isso pode levar alguns segundos)"):
        doc, log = react_agent(task_input, code)

    st.success("Processamento Completo!")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Documentação Gerada")
        st.markdown(doc)

    with col2:
        st.subheader("🧠 Log do Raciocínio ReAct")
        # Format the log beautifully into a text box
        log_text = "\n\n".join(log)
        st.text_area("Passo-a-passo e Tools", value=log_text, height=600)
    
    st.divider()
    with st.expander("Ver Código Original"):
        st.code(code)
