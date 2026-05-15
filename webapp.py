import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

st.title("sasank Ai")

try:
    llm = ChatOpenAI(model="gpt-4o-mini")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Type your message")

    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        response = llm.invoke(prompt)

        with st.chat_message("assistant"):
            st.markdown(response.content)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response.content
            }
        )

except Exception as e:
    st.error(f"Error: {e}")