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

# Criar a tabela se não existir
c.execute('''CREATE TABLE IF NOT EXISTS conversation_history 
             (role text, message text)''')

# Função para enviar mensagem e obter resposta
def enviar_mensagem(pergunta, contexto):
    messages = [{"role": "system", "content": "Olá! Sou um especialista em Python, Pandas, PySpark e AWS."}]
    messages.extend(contexto)
    messages.append({"role": "user", "content": pergunta})
    response = client.chat.completions.create(
        model="llama-13b-chat",
        messages=messages
    )
    return response.choices[0].message.content, messages

# Interface Streamlit para envio de pergunta
pergunta = st.chat_input("Digite sua pergunta para a IA:")

# Botão para limpar o histórico de conversas
if st.button("Limpar Histórico de Conversas"):
    c.execute("DELETE FROM conversation_history")
    conn.commit()

# Enviar a pergunta para a IA quando o usuário enviar a mensagem
if pergunta:
    c.execute("SELECT * FROM conversation_history")
    contexto = [{"role": row[0], "content": row[1]} for row in c.fetchall()]
    resposta, contexto = enviar_mensagem(pergunta, contexto)
    c.execute("INSERT INTO conversation_history VALUES (?, ?)", ("🙎^{😊:", pergunta))
    conn.commit()
    c.execute("INSERT INTO conversation_history VALUES (?, ?)", ("🤖:", resposta))
    conn.commit()

# Barra lateral
st.sidebar.title(" LLAMA 2")  # Título na barra lateral
# Adicionando uma descrição na barra lateral
st.sidebar.markdown("Este é um projeto feito utilizando a OpenAI.")

st.title("Chat com OpenAI")

# Carregar e exibir o histórico de conversa do banco de dados
c.execute("SELECT * FROM conversation_history")
for row in c.fetchall():
    if row[0] == "🙎^{😊:":
        st.write(f'<div style="background-color: #87CEEB; padding: 10px; border-radius: 10px; color: #FFFFFF; float: right">{row[1]}</div>', unsafe_allow_html=True)
    else:
        st.write(f'<div style="background-color: #87CEEB; padding: 10px; border-radius: 10px; color: #FFFFFF; float: left">{row[1']}</div>', unsafe_allow_html=True)

# Fechar a conexão com o banco de dados
conn.close()
