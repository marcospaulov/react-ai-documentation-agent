# 🤖 Agente ReAct para Engenharia de Software

## 📖 Visão Geral

O **react-ai-documentation-agent** é um projeto avançado de Inteligência Artificial Generativa direcionado à **Engenharia de Software**. O seu propósito é atuar como um assistente virtual totalmente autônomo através do paradigma **ReAct (Reasoning + Acting)**.

A principal missão deste agente é realizar a geração, atualização e manutenção automatizada de documentação técnica de software. Ele interage dinamicamente com o repositório, inspecionando o código-fonte, mapeando diretórios e analisando o histórico do Git (commits e diffs) para formular suas próprias deduções e gerar relatórios consistentes em Markdown, minimizando a dependência de um usuário prestando contextos.

### 🎯 Objetivos do Projeto

- **Geração de Documentação Tecnológica**: Criar manuais e explicações de código de forma 100% automatizada.
- **Integração Real com Git**: Analisar difs de commits passados e criar resumos de arquitetura com precisão.
- **Mitigação de Alucinações (ReAct Cycle)**: Em vez de submeter o "Zero-shot" (perguntar cegamente ao modelo), o agente é forçado a raciocinar *passo-a-passo*, acionando ferramentas de sistema iterativamente no background.

---

## 🛠️ Paradigma ReAct (Thought, Action, Observation)

O Agente age seguindo um loop rígido de iterações configurado no `gemini-2.5-flash`:

1. **Thought (Raciocínio):** O modelo avalia o problema atual e decide qual ação tomar e qual será sua entrada.
2. **Action (Ação):** O LLM escolhe exatamente UMA ferramenta do rol fornecido a ele (Ex: `list_directory`).
3. **Observation (Observação):** O script Python executa e captura o resultado bruto dessa ferramenta e re-injeta a saída no prompt da próxima etapa, alimentando a IA até que a Tarefa se conclua perfeitamente.

As **Ferramentas (Tools)** disponíveis nativamente para o agente são:

- `read_file`: Lê o texto exato de qualquer código ou arquivo estruturado do repositório físico local.
- `list_directory`: Inspeciona subdiretórios ajudando a vasculhar lógicas de arquivos.
- `git_log`: Extrai o changelog de mensagens registradas em commits com ferramentas nativas `git` na máquina.
- `git_diff`: Traz as entranhas exclusivas das modificações em um branch ou arquivos não trackeados.

---

## 📦 Dependências do Projeto

A stack do ecossistema adota pacotes puramente cirúrgicos para diminuir peso na memória. Atualmente os listados primários em `requirements.txt` consistem em:

- **`google-genai`**: SDK Oficial nativo do Google moderno para interação de Chatbot Rápida via API Key com os LLMs da família `Gemini Flash 2.5`.
- **`streamlit`**: Framework robusto responsável por "pintar" o Frontend Web. Interliga componentes dinâmicos (chatbars, file uploaders e live loggers) tratando reatividade visual em código Python nativo de forma fluida.
- **`python-dotenv`**: Carregador de credenciais do ambiente local que expõe propriedades do arquivo local do `.env`, prevenindo assim riscos de Segurança e vazamento de Chaves de API publicamente.

---

## 📁 Estrutura de Diretórios

- **`app.py`**: Ponto de Entrada mestre (Entrypoint). Inicia o Servidor Interativo do Streamlit.
- **`src/`**: A camada principal do projeto em Python focada no backend subdividida no paradigma *Single Responsibility*:
  - **`src/agent/`**: Camada do *Cérebro do Agente* Autônomo
    - `react.py`: Módulo que processa dinamicamente a conversação re-passando os prompts gerados usando Expressões Regulares (Regex).
    - `tools.py`: O "executor" responsável pelas regras estritas do Sistema Operacional. Integra o script local com subprocessos shell de OS/Git.
    - `prompts.py`: Os contratos de sistema formatados em hard-text do ReAct que instruem à GenAI a obrigatoriedade de não quebrar as formatações JSON e Textuais para não quebrar a UI.
  - **`src/config.py`** e **`src/llm.py`**: Central de Constants e injeção do Client de Autenticação de Nuvem pela Variável de OS.

---

## 🚀 Como Iniciar Seu Agente

1. **Clonando e Isolando o Repositório**
Após instalar o repositório em sua máquina, crie de imediato um *Virtual Environment* de uso limpo pelo seu terminal na raiz da pasta:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac / Bash / Linux
python -m venv .venv
source .venv/bin/activate
```

1. **Instalando as Bibliotecas**
Com a virtualização ativada com o nome da Venv no prefixo do console, adquira nossos pipelines principais:

```bash
pip install -r requirements.txt
```

1. **Injeção de Credenciais de Nuvem (.env)**
Crie manualmente na raiz da pasta matriz (.gitignore blindado) um arquivo unicamente chamado de `.env`. Preencha de imediato sua autenticação oficial da plataforma Cloud do Gemini:

```dotenv
GEMINI_API_KEY="SUA-CHAVE-AQUI"
```

1. **Iniciando a Aplicação ReAct Visível!**
Levante o servidor Streamlit Server em Localhost via comando na raiz:

```bash
streamlit run app.py
```

Essa interface vai se desdobrar automaticamente até criar uma nova guia rápida e limpa no Browser da máquina com a Interface de Conversação Inteligente pronta para seus uploads!

Integrantes do grupo:

- Marcos Paulo Vimieiro Silva (código do aluno: 229546)
- Bruno Henrique Ribeiro da Paixão (código do aluno: 229499)
- João Paulo Silva Borges (código do aluno: 229201)
- Vitor Passos de Moraes (código do aluno: 238414)
- Gustavo Tartaglia Silva de Paula (código do aluno: 229428)
