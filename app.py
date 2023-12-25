# Allow users to enter LM Studios settings
import streamlit as st
import openai
import json
import os
from datetime import datetime

# Configure your OpenAI API settings
openai.api_base = 'http://localhost:1234/v1'
openai.api_key = ''

# Your function for retrieving completions
def get_completion(prompt, model="local model", temperature=0.0):
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

# Function for the session list
def save_session_index(session_key):
    try:
        with open(os.path.join('chat_data', 'session_index.json'), 'r') as f:
            session_index = json.load(f)
    except FileNotFoundError:
        session_index = []
    session_index.append({
        "name": session_key,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "link": f'{session_key}_chat_history.json'
    })
    with open(os.path.join('chat_data', 'session_index.json'), 'w') as f:
        json.dump(session_index, f)

def app():
    st.title("Jarvis Chatbot")
    # Create subfolders for JSON files if necessary
    os.makedirs('chat_data', exist_ok=True)

    # Sidebar
    st.sidebar.title("New Chat")
    new_chat_name = st.sidebar.text_input("Name for new chat:", value="Chatname?", key="new_chat_name_sidebar")
  
    if st.sidebar.button("New Chat"):
        st.session_state['session_key'] = new_chat_name
        save_chat_history(st.session_state['session_key'], [])  # Create a new empty chat history file
        save_session_index(st.session_state['session_key'])

    st.sidebar.markdown("---")  # Separator
    st.sidebar.header("Chat History")  # Header

    # List of existing chats
    try:
        with open(os.path.join('chat_data', 'session_index.json'), 'r') as f:
            session_index = json.load(f)
    except FileNotFoundError:
        session_index = []
    for session in session_index:
        if st.sidebar.button(session["name"]):
            st.session_state['session_key'] = session["name"]

    # Load chat history
    if 'session_key' in st.session_state:
        st.header(st.session_state['session_key'])  # Display the name of the current session
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
    try:
        with open(os.path.join('chat_data', f'{session_key}_chat_history.json'), 'r') as f:
            chat_history = json.load(f)
    except FileNotFoundError:
        chat_history = []
    return chat_history

def save_chat_history(session_key, chat_history):
    with open(os.path.join('chat_data', f'{session_key}_chat_history.json'), 'w') as f:
        json.dump(chat_history, f)

if __name__ == "__main__":
    app()
