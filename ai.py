import streamlit as st
import os
import asyncio
from dotenv import load_dotenv

# Autogen imports
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load API key
load_dotenv()

# Streamlit setup
st.set_page_config(page_title="🌈 AI Assistant", page_icon="🤖", layout="wide")

# CSS for colors
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #e0c3fc, #8ec5fc);
    }
    .stTextInput > div > div > input {
        border: 2px solid #6a5acd;
        border-radius: 12px;
        padding: 10px;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #6a5acd;
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #483d8b;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌈🤖 AI Assistant Chat")

# Create client + agent
llm_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)
assistant = AssistantAgent("Helper", llm_client)

# Function to run async Autogen in Streamlit
async def get_response(user_input: str):
    task = TextMessage(content=user_input, source="user")
    result = await assistant.run(task=task)   # ✅ await coroutine
    return result.messages[-1].content

# Input
user_input = st.text_input("💬 Your message:")

if st.button("🚀 Send"):
    if user_input.strip():
        with st.spinner("🤔 Thinking..."):
            response = asyncio.run(get_response(user_input))   # ✅ run async properly
            st.success("✅ AI Response:")
            st.write(response)
    else:
        st.warning("⚠️ Please type something first!")
