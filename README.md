# 🤖 Tool-Enabled AI Assistant (Streamlit + Azure OpenAI)

This project is a **Streamlit-based AI assistant** powered by **Azure OpenAI (GPT-4o)**. It enhances GPT with tool-calling capabilities such as:

- 🌤️ **Weather Lookup**
- ⏰ **Current Time**
- 📍 **Get Coordinates from City**
- 💱 **Currency Conversion**
- 🌐 **Web Search (Live)**

---

## 🚀 Features

- ✅ Chat interface with **tool-use support**
- ✅ Clean UI with **chat history dropdown**
- ✅ Fast responses using **Azure-hosted GPT-4o**
- ✅ Modular backend (`main.py`) for tool integration

---


## 🧠 How It Works

The assistant intelligently uses tools when needed via `chat_with_tools()`. Tool-calling is based on keywords in the user's query.

Supported tools:

| Tool Name         | Description                         |
|------------------|-------------------------------------|
| `get_weather`    | Fetches weather by coordinates      |
| `get_time`       | Returns current time                |
| `get_coordinates`| Gets latitude and longitude of city |
| `convert_currency`| Converts currencies using latest rate |
| `search_web`     | Performs live Google search         |

## 1. COpy this 
```bash
git clone https://github.com/your-username/tool-enabled-chatbot.git
cd tool-enabled-chatbot
```
## 2. Install dependencies
```bash
pip install streamlit openai requests python-dotenv
```
## 3. Run the Application
```bash
streamlit run app.py
``` 

