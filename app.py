import streamlit as st
import requests

# Function to fetch model options dynamically
def get_available_models():
    api_endpoint = "https://your-server-url/models"  # Replace with your model server's endpoint
    response = requests.get(api_endpoint)
    models = response.json()
    return models

# API call function with error handling
def make_api_call(server_url, model, messages):
    api_endpoint = f"{server_url}/chat/completions"
    data = {"model": model, "messages": messages}
    try:
        response = requests.post(api_endpoint, json=data)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {e}")
        return None

# Streamlit app with enhanced features
def main():
    st.title("LLM Playground")

    # Sidebar
    st.sidebar.title("Custom Data Input")

    server_url = st.sidebar.text_input("Enter Server URL", "http://localhost:4000")

    # Fetch available models dynamically
    available_models = get_available_models()
    model = st.sidebar.selectbox("Select Model", available_models)

    # Message input with improved layout
    st.sidebar.subheader("Messages")
    messages = []
    for i in range(1, 11):
        role_input = st.sidebar.selectbox(f"Role for Message {i}", ["user", "assistant"], key=f"role_{i}")
        content_input = st.sidebar.text_area(f"Content for Message {i}", key=f"content_{i}")
        messages.append({"role": role_input, "content": content_input})

    # Preview and API call
    st.subheader("Preview Messages")
    st.json(messages)

    if st.button("Call API"):
        st.info("Calling API...")
        response = make_api_call(server_url, model, messages)
        if response:
            st.success("API call successful!")
            st.json(response)

if __name__ == "__main__":
    main()
