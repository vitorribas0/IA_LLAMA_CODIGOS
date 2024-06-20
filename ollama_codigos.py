import streamlit as st
import sqlite3
from openai import OpenAI

st.set_page_config(layout="wide")  # Configuração para layout de página amplo

# Inicialize o cliente OpenAI
client = OpenAI(
    api_key="LL-rZdxy5UFL4evTVeC6H1Jzuph00H08neiKQUGm3HSYOm1qMD4T8YxonRYedIH6856",
    base_url="https://api.llama-api.com"
)

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('chat_history.db')
c = conn.cursor()

# Criar a tabela se não existir (incluindo contexto)
c.execute('''CREATE TABLE IF NOT EXISTS conversation_history 
             (role text, message text, context text)''')

# Função para enviar mensagem e obter resposta
def enviar_mensagem(pergunta, contexto_atual):
    messages = [
        {"role": "system", "content": "Olá! Sou um especialista em Python, Pandas, PySpark e AWS."},
        {"role": "user", "content": pergunta, "context": contexto_atual}
    ]
    
    response = client.chat.completions.create(
        model="llama-13b-chat",
        messages=messages
    )
    
    # Atualiza o contexto para a próxima interação
    novo_contexto = response.choices[0].message.context
    return response.choices[0].message.content, novo_contexto

# Interface Streamlit para envio de pergunta
pergunta = st.text_input("Digite sua pergunta para a IA:")

# Botão para limpar o histórico de conversas
if st.button("Limpar Histórico de Conversas"):
    c.execute("DELETE FROM conversation_history")
    conn.commit()

if pergunta:
    # Recupera o contexto atual da última conversa
    c.execute("SELECT context FROM conversation_history ORDER BY rowid DESC LIMIT 1")
    resultado = c.fetchone()
    contexto_atual = resultado[0] if resultado else None
    
    # Envia a pergunta para a IA com o contexto atual
    resposta, novo_contexto = enviar_mensagem(pergunta, contexto_atual)
    
    # Salva a pergunta, resposta e novo contexto no banco de dados
    c.execute("INSERT INTO conversation_history VALUES (?, ?, ?)", ("🙎‍♂:", pergunta, novo_contexto))
    c.execute("INSERT INTO conversation_history VALUES (?, ?, ?)", ("🤖:", resposta, novo_contexto))
    conn.commit()

# Barra lateral
st.sidebar.title("🦙 LLAMA 2")  # Título na barra lateral
# Adicionando uma descrição na barra lateral
st.sidebar.markdown("Este é um projeto feito utilizando o 🦙 LLAMA 2.")

st.title("Chat com OpenAI")

# Carregar e exibir o histórico de conversa do banco de dados
for row in c.execute("SELECT * FROM conversation_history"):
    st.write(row[0], row[1])

# Fechar a conexão com o banco de dados
conn.close()
