import streamlit as st
import os
import asyncio
from dotenv import load_dotenv

# Autogen imports
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load API key
load_dotenv()

# Streamlit setup
st.set_page_config(page_title="🌟 Smart To-Do Planner", page_icon="📝", layout="wide")

# CSS for colorful UI
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #ffecd2, #fcb69f);
    }
    .stTextInput > div > div > input {
        border: 2px solid #4CAF50;
        border-radius: 12px;
        padding: 10px;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #388E3C;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌟📝 AI Multi-Agent To-Do List Planner")

# Create LLM client
llm_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define different role agents
organizer = AssistantAgent(
    "Organizer", llm_client,
    system_message="You are an organizer. Break down tasks into clear, step-by-step actionable items."
)

motivator = AssistantAgent(
    "Motivator", llm_client,
    system_message="You are a motivator. Add positive encouragement and tips to complete tasks."
)

deadline_manager = AssistantAgent(
    "DeadlineManager", llm_client,
    system_message="You are a deadline manager. Suggest realistic deadlines and priorities for tasks."
)

# Create a team (group chat) using Round Robin
todo_team = RoundRobinGroupChat([organizer, motivator, deadline_manager], max_turns=6)

# Function to run async group chat
async def get_todo_plan(user_input: str):
    task = TextMessage(content=user_input, source="user")
    result = await todo_team.run(task=task)
    return [m.content for m in result.messages if m.source != "user"]

# Input from user
user_input = st.text_input("💬 Enter your task (e.g., 'Prepare for an office presentation'): ")

if st.button("🚀 Generate To-Do Plan"):
    if user_input.strip():
        with st.spinner("🤖 Agents are collaborating..."):
            responses = asyncio.run(get_todo_plan(user_input))

            st.success("✅ Final AI-Powered To-Do Plan:")
            for idx, msg in enumerate(responses, 1):
                st.write(f"**💬 Agent {idx}:** {msg}")
    else:
        st.warning("⚠️ Please type something first!")
