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
st.set_page_config(page_title="💪 Fitness Plan Generator", page_icon="🏋️", layout="wide")

# CSS for colorful UI
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #fceabb, #f8b500);
    }
    .stTextInput > div > div > input {
        border: 2px solid #ff8c00;
        border-radius: 12px;
        padding: 10px;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #ff8c00;
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #e67e22;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💪🏋️ AI Multi-Agent Fitness Plan Generator")

# Create LLM client
llm_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define three fitness agents
trainer = AssistantAgent(
    "Trainer",
    llm_client,
    system_message="You are a fitness trainer. Focus on workout routines, exercises, and physical activity."
)

nutritionist = AssistantAgent(
    "Nutritionist",
    llm_client,
    system_message="You are a nutritionist. Focus on diet, meal planning, and healthy eating habits."
)

psychologist = AssistantAgent(
    "Psychologist",
    llm_client,
    system_message="You are a psychologist. Focus on motivation, consistency, and mental well-being in fitness."
)

# Create a team (group chat) using Round Robin
fitness_team = RoundRobinGroupChat([trainer, nutritionist, psychologist], max_turns=6)

# Function to run async group chat
async def get_fitness_plan(user_input: str):
    task = TextMessage(content=user_input, source="user")
    result = await fitness_team.run(task=task)
    return [m.content for m in result.messages if m.source != "user"]

# Input from user
user_input = st.text_input("💬 Enter your fitness goal (e.g., 'Lose 5 kg in 2 months'): ")

if st.button("🚀 Generate Fitness Plan"):
    if user_input.strip():
        with st.spinner("🤝 Trainer, Nutritionist, and Psychologist are discussing..."):
            responses = asyncio.run(get_fitness_plan(user_input))

            st.success("✅ Final AI Fitness Plan:")
            for idx, msg in enumerate(responses, 1):
                st.write(f"**💬 Message {idx}:** {msg}")
    else:
        st.warning("⚠️ Please type your fitness goal first!")
