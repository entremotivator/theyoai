import streamlit as st
import openai
import json
import os
from datetime import datetime

# Function to configure OpenAI API settings
def configure_openai_api():
    st.sidebar.subheader("OpenAI API Settings")
    api_base = st.sidebar.text_input("API Base URL", "http://localhost:1234/v1")
    api_key = st.sidebar.text_input("API Key", type="password")
    return api_base, api_key

# Function to get OpenAI completion
def get_completion(prompt, model="local model", temperature=0.0, api_base='http://localhost:1234/v1', api_key=''):
    openai.api_base = api_base
    openai.api_key = api_key

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

# Rest of the code remains the same...

# Main app function
def app():
    st.title("Jarvis Chatbot")
    os.makedirs('chat_data', exist_ok=True)

    # Configure OpenAI API settings
    api_base, api_key = configure_openai_api()

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
        st.header(st.session_state['session_key'])  
        chat_history = load_chat_history(st.session_state['session_key'])
        
        user_input = st.text_input("You:")
        if user_input:
            response = get_completion(user_input, api_base=api_base, api_key=api_key)
            chat_history.append({"role": "user", "message": user_input})
            chat_history.append({"role": "Jarvis", "message": response})
            save_chat_history(st.session_state['session_key'], chat_history)

        # Display the chat history
        for chat in chat_history:
            role = chat["role"]
            message = chat["message"]
            with st.container():
                st.write(f"{role}: {message}")

    else:
        st.warning("Please create a new chat or select an existing chat.")

# Rest of the code remains the same...

if __name__ == "__main__":
    app()
