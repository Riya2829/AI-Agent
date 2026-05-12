import streamlit as st
import requests

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI File Assistant")

st.markdown("Search and discover Google Drive files using AI.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask something like 'Find images'")

if user_input:

    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response
    with st.chat_message("assistant"):

        with st.spinner("Searching files..."):

            try:

                response = requests.post(
                    "https://ai-agent-yorb.onrender.com/chat",
                    json={"message": user_input}
                )

                ai_response = response.json()["response"]

            except Exception as e:

                ai_response = f"Error: {e}"

            st.markdown(ai_response)

    # Save AI message
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })
