import streamlit as st
from openai import OpenAI

# Function to interact with the local LLM chat model
def interact_with_model(messages, base_url):
    # Point to the user-specified server
    client = OpenAI(base_url=base_url, api_key="not-needed")

    # Make a request to the local model
    completion = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=messages,
        temperature=0.7,
    )

    return completion.choices[0].message


# Streamlit app
def main():
    st.title("LLM Chat App")

    # User input for server settings
    base_url = st.text_input("Enter Local Server Base URL", "http://localhost:1231/v1")

    # Sidebar settings
    st.sidebar.header("Server Settings")
    cors_enabled = st.sidebar.checkbox("Cross-Origin-Resource-Sharing (CORS)", value=True)
    request_queuing = st.sidebar.checkbox("Request Queuing", value=True)
    server_logging = st.sidebar.checkbox("Server Logging", value=True)

    # Automatic Prompt Formatting
    auto_prompt_formatting = st.sidebar.checkbox("Automatic Prompt Formatting", value=True)

    # Local Inference Server
    st.sidebar.header("Local Inference Server")
    st.sidebar.info("Start a local HTTP server that behaves like OpenAI's API.")

    # Chat UI
    st.subheader("Chat Interface")

    # User input for chat messages
    user_message = st.text_input("User Message")

    # Display chat messages
    chat_messages = [
        {"role": "system", "content": "Always answer in rhymes."},
        {"role": "user", "content": user_message},
    ]

    # Display messages
    st.subheader("Chat Messages")
    for msg in chat_messages:
        st.text(f"{msg['role'].capitalize()}: {msg['content']}")

    # Interaction with the model
    if st.button("Send Message"):
        # Make a request to the user-specified server
        response = interact_with_model(chat_messages, base_url)

        # Display model's response
        st.subheader("Model's Response")
        st.text(f"Model: {response}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
