
🌈🤖 Autogen AI Assistant (Single Agent)

A Streamlit app powered by Microsoft Autogen + OpenAI GPT.
This app creates a single AI Assistant agent where you can chat interactively with a beautiful gradient UI.

✨ Features

✅ One AI Assistant (AssistantAgent) using Autogen

✅ GPT model (gpt-4o-mini by default)

✅ Interactive chat UI built with Streamlit

✅ Gradient background + styled input and buttons

✅ Simple .env setup for OpenAI API key

📂 Project Structure
autogen-ai-assistant/
│
├── ai.py             # Main Streamlit app (your provided code)
├── requirements.txt  # Python dependencies
├── README.md         # Documentation
└── .env              # OpenAI API key (not committed to GitHub)

⚙️ Installation

Clone this repository:

git clone https://github.com/your-username/autogen-ai-assistant.git
cd autogen-ai-assistant


Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows


Install dependencies:

pip install -r requirements.txt

🔑 Setup API Key

Create a file named .env in the project folder and add:

OPENAI_API_KEY=your_openai_api_key_here


Get your key from OpenAI
.

▶️ Run the App

Start Streamlit:

streamlit run ai.py


Open browser at 👉 http://localhost:8501

📋 Example

👉 User Input:

💬 Hello AI, who are you?


👉 AI Response:

✅ I’m your helpful AI Assistant powered by Autogen + OpenAI 🚀

🛠 Requirements (requirements.txt)
streamlit
python-dotenv
autogen-agentchat
autogen-ext
openai

🚀 Future Improvements

Add chat history to remember previous messages

Extend to multi-agent groupchat

Deploy on Streamlit Cloud / Hugging Face Spaces

✨ Built with ❤️ by Mareeswari using Autogen + Streamlit + OpenAI
