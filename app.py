# Allow users to enter their own server info in the sidebar
import streamlit as st
import openai
import json
import os
from datetime import datetime

# Default OpenAI API settings
openai.api_base = 'http://localhost:1234/v1'
openai.api_key = ''

# Function to configure OpenAI API settings
def configure_openai_api():
    st.sidebar.subheader("OpenAI API Settings")
    openai.api_base = st.sidebar.text_input("API Base URL", openai.api_base)
    openai.api_key = st.sidebar.text_input("API Key", openai.api_key, type="password")

# Your function for retrieving completions
def get_completion(prompt, model="local model", temperature=0.0):
    # (unchanged code)

# Function for the session list
def save_session_index(session_key):
    # (unchanged code)

def app():
    st.title("Jarvis Chatbot")
    os.makedirs('chat_data', exist_ok=True)

    # Configure OpenAI API settings
    configure_openai_api()

    # Sidebar
    st.sidebar.title("New Chat")
    new_chat_name = st.sidebar.text_input("Name for new chat:", value="Chatname?", key="new_chat_name_sidebar")
  
    if st.sidebar.button("New Chat"):
        st.session_state['session_key'] = new_chat_name
        save_chat_history(st.session_state['session_key'], [])
        save_session_index(st.session_state['session_key'])

    st.sidebar.markdown("---")  # Separator
    st.sidebar.header("Chat History")  # Header

    # List of existing chats
    # (unchanged code)

    # Load chat history
    if 'session_key' in st.session_state:
        st.header(st.session_state['session_key'])  
        chat_history = load_chat_history(st.session_state['session_key'])
        
        user_input = st.chat_input("You:")
        if user_input:
            response = get_completion(user_input)
            chat_history.append({"role": "user", "message": user_input})
            chat_history.append({"role": "Jarvis", "message": response})
            save_chat_history(st.session_state['session_key'], chat_history)

        # Display the chat history
        for chat in chat_history:
            role = chat["role"]
            message = chat["message"]
            with st.chat_message(role):
                st.write(message)
    else:
        st.warning("Please create a new chat or select an existing chat.")

def load_chat_history(session_key):
    # (unchanged code)

def save_chat_history(session_key, chat_history):
    # (unchanged code)

if __name__ == "__main__":
    app()
