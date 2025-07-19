#Importing the libraries that will be needed
import streamlit as st
from rolex_core import RAGBot

# Initializing RAGBot with a session state
if "rag_bot" not in st.session_state:
    st.session_state.rag_bot = RAGBot()

# Setting up chat history with a session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#Title page for the website.
st.title("⌚ :green[Rolex] Assistant")
st.subheader("Ask about our Luxury Watch models, features, and more!")

# Chat input; where user can ask questions
user_input = st.chat_input("")

#If the user will input a query then: 
if user_input:
    #the message will first be added to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    #Then using the RAGBot, we will get the response
    response = st.session_state.rag_bot.get_answer(user_input)

    #the response generated will also be stored in the chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# Chat interface for the bot.
for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])