import streamlit as st
import openai

st.set_page_config(page_title="Chatbot", page_icon="💬")

# Sidebar
st.sidebar.title("💬 Chatbot Options")

# New Chat Button
if st.sidebar.button("🆕 New Chat"):
    st.session_state["messages"] = []  # Clear chat history

# API Key Input
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Display Chat History in Sidebar
st.sidebar.subheader("📜 Chat History")
if "messages" in st.session_state:
    for msg in st.session_state["messages"]:
        st.sidebar.text(f"{msg['role'].capitalize()}: {msg['content'][:40]}...")  # Show only 40 chars

# Main Chat UI
st.title("💬 Chatbot")
st.write("🚀 A Streamlit chatbot powered by OpenAI")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Show "How can I help you?" if no messages yet
if not st.session_state["messages"]:
    st.write("🤖 **How can I help you?**")

# User Input
user_input = st.text_input("Your message", "")

if st.button("Send"):
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API key.")
    elif not user_input:
        st.warning("⚠️ Please enter a message.")
    else:
        try:
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            
            bot_reply = response["choices"][0]["message"]["content"]

            # Save conversation history
            st.session_state["messages"].append({"role": "user", "content": user_input})
            st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

            # Display Response
            st.write(bot_reply)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
