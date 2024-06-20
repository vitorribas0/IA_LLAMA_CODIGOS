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
             (role TEXT, message TEXT)''')

# Função para enviar mensagem e obter resposta
def send_message(role, message):
    # Salvar a mensagem no banco de dados
    c.execute("INSERT INTO conversation_history (role, message) VALUES (?, ?)", (role, message))
    conn.commit()
    
    # Obter resposta da IA
    response = client.Completion.create(
        model="text-davinci-003",  # Use um modelo apropriado para sua API
        prompt=message,
        max_tokens=150
    )
    
    # Salvar a resposta no banco de dados
    response_message = response['choices'][0]['text'].strip()
    c.execute("INSERT INTO conversation_history (role, message) VALUES (?, ?)", ("assistant", response_message))
    conn.commit()
    
    return response_message

# Função para exibir o histórico da conversa
def get_conversation_history():
    c.execute("SELECT role, message FROM conversation_history")
    return c.fetchall()

# Interface do usuário com Streamlit
st.title("Chat com IA")

# Exibir histórico da conversa
st.subheader("Histórico da Conversa")
conversation_history = get_conversation_history()
for role, message in conversation_history:
    if role == "user":
        st.text(f"Você: {message}")
    else:
        st.text(f"IA: {message}")

# Entrada do usuário
user_input = st.text_input("Você:", "")
if st.button("Enviar"):
    if user_input:
        response = send_message("user", user_input)
        st.text(f"IA: {response}")

conn.close()
