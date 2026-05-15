import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

st.set_page_config(page_title="Sasank AI")

llm = ChatOpenAI(model="gpt-4o-mini")

search_tool = TavilySearchResults(max_results=3)

st.title("Sasank AI")

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

    realtime_keywords = [
        "weather",
        "news",
        "today",
        "score",
        "live",
        "price",
        "current"
    ]

    if any(word in prompt.lower() for word in realtime_keywords):

        search_results = search_tool.invoke(prompt)

        final_prompt = f"""
        Use this live internet data to answer:

        {search_results}

        User question:
        {prompt}
        """

        response = llm.invoke(final_prompt)

    else:
        response = llm.invoke(prompt)

    with st.chat_message("assistant"):
        st.markdown(response.content)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.content
        }
    )