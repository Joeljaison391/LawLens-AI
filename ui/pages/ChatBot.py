import streamlit as st
import requests
import json

# Set page config
st.set_page_config(page_title="Chatbot Interface", page_icon="💬", layout="wide")

# Custom CSS for a monochrome Chat UI
st.markdown(
    """
    <style>
        body {
            background-color: #f0f0f0;
        }
        .chat-container {
            max-width: 800px;
            margin: auto;
            padding: 20px;
            background-color: #ffffff;
            border: 1px solid #ccc;
            border-radius: 8px;
        }
        .user-message {
            background-color: #e0e0e0;
            color: #333;
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: right;
            font-family: monospace;
        }
        .bot-message {
            background-color: #d0d0d0;
            color: #111;
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: left;
            font-family: monospace;
        }
        .header-title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #0D47A1;
            margin-bottom: 0.2em;
            text-shadow: 2px 2px 4px #aaa;
            font-family: monospace;
        }
        .header-subtitle {
            text-align: center;
            font-size: 24px;
            color: #424242;
            margin-bottom: 1em;
            font-family: monospace;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for branding and navigation
st.sidebar.image("https://via.placeholder.com/250x150.png?text=Product+Logo", use_container_width=True)
st.sidebar.markdown("## AI Compliance Checker")
st.sidebar.markdown("**Your one-stop solution for industrial compliance analysis.**")
st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")
st.sidebar.markdown("- Home")
st.sidebar.markdown("- Chatbot")
st.sidebar.markdown("- About")
st.sidebar.markdown("---")
st.sidebar.markdown("### Contact")
st.sidebar.write("For inquiries, email [support@example.com](mailto:support@example.com)")

# Main chat container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.markdown("<div class='header-title'>Chatbot Interface</div>", unsafe_allow_html=True)
st.markdown("<div class='header-subtitle'>Ask your industrial compliance questions</div>", unsafe_allow_html=True)

# Initialize chat history in session state if not already present.
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are an AI assistant helping with industrial compliance questions."}
    ]

# Function to call the chat API endpoint.
def send_message_to_api(messages):
    api_url = "http://localhost:8000/chat"  # Replace with your actual API endpoint.
    payload = {"messages": messages}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Expecting the response to include a key "message" with the bot's reply.
            return data.get("message", "No reply received.")
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error calling API: {e}"

# Display the chat history (skipping the initial system message).
for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>{msg['content']}</div>", unsafe_allow_html=True)

# Use a form for message input for smoother flow.
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    bot_reply = send_message_to_api(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    st.rerun()

if st.button("Clear Chat"):
    st.session_state.chat_history = [
        {"role": "system", "content": "You are an AI assistant helping with industrial compliance questions."}
    ]
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
