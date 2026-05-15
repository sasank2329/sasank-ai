import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

st.set_page_config(page_title="Sasank AI")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

search_tool = TavilySearchResults(max_results=5)

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
        "today",
        "news",
        "live",
        "score",
        "ipl",
        "match",
        "price",
        "current",
        "latest"
    ]

    use_search = any(
        word in prompt.lower()
        for word in realtime_keywords
    )

    if use_search:

        search_results = search_tool.invoke(prompt)

        final_prompt = f"""
You are an AI assistant with access to LIVE internet search results.

Use ONLY the information below to answer the user accurately.

Live search results:
{search_results}

User question:
{prompt}

Give a direct answer.
Do NOT say:
- you don't have internet access
- you cannot access live data
- you recommend checking websites

Answer naturally and confidently using the live data above.
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