import streamlit as st
from lmstudio import LMStudio

def main():
    st.title("LM Studio UI with Streamlit")

    # Load model (adjust as needed)
    model = LMStudio.from_pretrained("gpt-j-6b")

    # Sidebar elements
    st.sidebar.title("Model Options")
    selected_model = st.sidebar.selectbox("Select Model", ["gpt-j-6b", "other_models"])
    prompt = st.sidebar.text_input("Enter your prompt:")
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.5)

    if st.sidebar.button("Generate"):
        with st.spinner("Generating..."):
            response = model.generate(prompt, temperature=temperature)
        st.write(response)

if __name__ == "__main__":
    main()
