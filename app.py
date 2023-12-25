import streamlit as st
import requests

def main():
    st.set_page_config(layout="wide")

    st.title("LLM Playground")

    with st.sidebar:
        st.header("Custom Data Input")

        server_url = st.text_input("Server URL", value="http://localhost")  # Server URL input
        server_port = st.number_input("Server Port", value=4000, min_value=1, max_value=65535)  # Server port input

        model = st.selectbox("Select Model", ["gpt-3.5-turbo", "command-nightly", "j2-mid"])

        # ... (rest of sidebar elements)

    with st.container():
        st.subheader("Preview Messages")
        # ... (enhanced message preview)

        if st.button("Call API"):
            with st.spinner("Calling API..."):
                SERVER_URL = f"{server_url}:{server_port}"
                response = make_api_call(model, messages)
            st.success("API call successful!")
            st.json(response, expanded=True)

# ... (rest of your code)

if __name__ == "__main__":
    main()
