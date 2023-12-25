import streamlit as st
import requests

# Sample API call function
def make_api_call(server_url, model, messages):
    api_endpoint = f"{server_url}/chat/completions"
    data = {"model": model, "messages": messages}
    response = requests.post(api_endpoint, json=data)
    return response.json()

# Streamlit app with sidebar for custom data input
def main():
    st.title("LLM Playground")

    # Sidebar for custom data input
    st.sidebar.title("Custom Data Input")
    
    # Allow users to input their server URL
    server_url = st.sidebar.text_input("Enter Server URL", "http://localhost:4000")

    model = st.sidebar.selectbox("Select Model", ["gpt-3.5-turbo", "command-nightly", "j2-mid"])

    # Allow users to add multiple messages
    messages = []
    message_count = st.sidebar.number_input("Number of Messages", value=1, min_value=1, max_value=10)
    for i in range(message_count):
        role = st.sidebar.selectbox(f"Role for Message {i+1}", ["user", "assistant"])
        content = st.sidebar.text_area(f"Content for Message {i+1}")
        messages.append({"role": role, "content": content})

    # Streamlit main content
    st.subheader("Preview Messages")
    st.json(messages)

    # Call API button
    if st.button("Call API"):
        st.info("Calling API...")
        response = make_api_call(server_url, model, messages)
        st.success("API call successful!")
        st.json(response)

if __name__ == "__main__":
    main()
