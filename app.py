import streamlit as st
from groq_client import query_groq
from voice_input import get_voice_input

# --- Config ---
st.set_page_config(page_title="Code Copilot", page_icon="🤖", layout="wide")

# --- Init ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #1e1e2f;
        color: #f0f0f0;
        font-family: 'Segoe UI', sans-serif;
    }
    .chat-message {
        border-radius: 10px;
        padding: 12px 16px;
        margin: 10px 0;
        width: fit-content;
        max-width: 80%;
        clear: both;
    }
    .user {
        background-color: #3b3b5c;
        margin-left: auto;
    }
    .assistant {
        background-color: #2a2a3b;
        margin-right: auto;
    }
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #1e1e2f;
        padding: 1rem 2rem;
        border-top: 1px solid #333;
    }
    .footer {
        text-align: center;
        color: #999;
        font-size: 12px;
        padding-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("⚙️ Settings")
model = st.sidebar.selectbox("Model", ["llama3-70b-8192", "mixtral-8x7b-32768"])
temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.2, 0.05)
language = st.sidebar.selectbox("Code Language", ["python", "javascript", "html", "bash", "cpp", "java"])

if st.sidebar.button("🎙️ Speak Prompt"):
    spoken_text = get_voice_input()
    if spoken_text:
        st.session_state.messages.append({"role": "user", "content": spoken_text})

# --- Chat History Display ---
st.title("🤖 Code Copilot")

chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        css_class = "user" if role == "user" else "assistant"
        st.markdown(f"<div class='chat-message {css_class}'>{content}</div>", unsafe_allow_html=True)

# --- Prompt Input ---
with st.container():
    prompt = st.chat_input("Type your message...")
    if prompt:
        # Show user message immediately
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Query Groq
        with st.spinner("Thinking..."):
            try:
                response = query_groq(prompt, model=model, temperature=temperature)
                st.session_state.messages.append({"role": "assistant", "content": f"```\n{response}\n```"})
            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"⚠️ Error: {str(e)}"})

# --- Footer ---
st.markdown("<div class='footer'>Built with ❤️ using Streamlit + Groq API by Tasbirul</div>", unsafe_allow_html=True)
