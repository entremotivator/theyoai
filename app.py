import streamlit as st
import openai
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List

# Function to retrieve completions
def get_completion(api_key, api_base, prompt, model="local model", temperature=0.0):
    openai.api_key = api_key
    openai.api_base = api_base

    prefix = "### Instruction:\n"
    suffix = "\n### Response:"
    formatted_prompt = f"{prefix}{prompt}{suffix}"
    messages = [{"role": "user", "content": formatted_prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

# Function for session index
def save_chat_history(session_key: str, chat_history: List[dict]):
    file_path = Path('chat_data') / f'{session_key}_chat_history.json'
    with open(file_path, 'w') as f:
        json.dump(chat_history, f)

def load_chat_history(session_key: str) -> List[dict]:
    try:
        with open(Path('chat_data') / f'{session_key}_chat_history.json', 'r') as f:
            chat_history = json.load(f)
    except FileNotFoundError:
        chat_history = []
    return chat_history

def save_session_index(session_key: str):
    try:
        with open(Path('chat_data') / 'session_index.json', 'r') as f:
            session_index = json.load(f)
    except FileNotFoundError:
        session_index = []
    session_index.append({
        "name": session_key,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "link": f'{session_key}_chat_history.json'
    })
    with open(Path('chat_data') / 'session_index.json', 'w') as f:
        json.dump(session_index, f)

def app():
    st.title("Jarvis Chatbot")
    os.makedirs('chat_data', exist_ok=True)

    st.sidebar.title("OpenAI Configuration")
    openai_api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")
    openai_api_base = st.sidebar.text_input("Enter OpenAI API Base URL:", value='https://api.openai.com/v1')

    st.sidebar.title("Neuer Chat")
    neuer_chat_name = st.sidebar.text_input("Name für neuen Chat:", value="Chatname?", key="neuer_chat_name_sidebar")

    if st.sidebar.button("Neuer Chat"):
        st.session_state['session_key'] = neuer_chat_name
        save_chat_history(st.session_state['session_key'], [])  # Create a new empty chat history file
        save_session_index(st.session_state['session_key'])

    st.sidebar.markdown("---", unsafe_allow_html=True)  # Separator
    st.sidebar.header("Chatverlauf")  # Chat history header

    try:
        with open(Path('chat_data') / 'session_index.json', 'r') as f:
            session_index = json.load(f)
    except FileNotFoundError:
        session_index = []
    
    for session in session_index:
        if st.sidebar.button(session["name"]):
            st.session_state['session_key'] = session["name"]

    if 'session_key' in st.session_state:
        st.header(st.session_state['session_key'])  # Display the current session name
        chat_history = load_chat_history(st.session_state['session_key'])

        user_input = st.text_input("Sie:")
        if user_input:
            response = get_completion(openai_api_key, openai_api_base, user_input)
            chat_history.append({"sender": "user", "message": user_input})
            chat_history.append({"sender": "Jarvis", "message": response})
            save_chat_history(st.session_state['session_key'], chat_history)

        for chat in chat_history:
            sender = chat["sender"]
            message = chat["message"]
            with st.beta_container():
                st.text(sender)
                st.text(message)
    else:
        st.warning("Bitte erstellen Sie einen neuen Chat oder wählen Sie einenvorhandenen Chat aus.")
        
if __name__ == "__main__":
    app()
