import json
import requests
from datetime import datetime
from openai import AzureOpenAI

# ────────────────────────────────────────────────────────────────
# 1. Initialize AzureOpenAI Client
# ────────────────────────────────────────────────────────────────
azure_endpoint = "URL"
api_key = "APIKY"
api_version = "Version"
model = "MODEL"

client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=api_key,
    api_version=api_version
)

# ────────────────────────────────────────────────────────────────
# 2. Tool Functions
# ────────────────────────────────────────────────────────────────
def get_weather(latitude: float, longitude: float) -> dict:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    data = requests.get(url).json().get('current_weather', {})
    return {
        "temperature": data.get('temperature'),
        "wind_speed": data.get('windspeed')
    }

def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    EXCHANGE_API_KEY = "a54598f3b3a6e99dcfe627fa"
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data["result"] == "success":
            return {
                "converted_amount": round(data["conversion_result"], 2),
                "rate": data["conversion_rate"]
            }
        else:
            return {"error": data.get("error-type", "Unknown error occurred")}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect: {str(e)}"}

def get_current_time() -> dict:
    now = datetime.now().isoformat(sep=' ', timespec='seconds')
    return {"current_time": now}

def search_web(query: str) -> dict:
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    data = requests.get(url).json()
    return {"summary": data.get('AbstractText', 'No summary available')}

def get_coordinates(city_name: str) -> dict:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    data = requests.get(url).json()
    results = data.get('results')
    if results:
        return {"latitude": results[0]['latitude'], "longitude": results[0]['longitude']}
    return {"error": "City not found"}

# ────────────────────────────────────────────────────────────────
# 3. Tool Schema
# ────────────────────────────────────────────────────────────────
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather by coordinates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"}
                },
                "required": ["latitude", "longitude"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current local system time.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert amount between two currencies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number"},
                    "from_currency": {"type": "string"},
                    "to_currency": {"type": "string"}
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web and return a summary of the top result.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_coordinates",
            "description": "Get latitude and longitude for a city name.",
            "parameters": {
                "type": "object",
                "properties": {"city_name": {"type": "string"}},
                "required": ["city_name"]
            }
        }
    }
]

# ────────────────────────────────────────────────────────────────
# 4. Chatbot Interaction Logic
# ────────────────────────────────────────────────────────────────
messages = []

def chat_with_tools(user_input: str):
    global messages
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    tool_calls = response.choices[0].message.tool_calls
    if not tool_calls: # when there is no tool to call 
        assistant_msg = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_msg})
        return assistant_msg

    # Tool call handling
    tc = tool_calls[0]
    args = json.loads(tc.function.arguments)
    tool_name = tc.function.name

    tool_mapping = {
        "get_weather": get_weather,
        "get_current_time": get_current_time,
        "convert_currency": convert_currency,
        "search_web": search_web,
        "get_coordinates": get_coordinates
    }

    tool_func = tool_mapping[tool_name]
    tool_output = tool_func(**args)

    # Add tool result to message history
    messages.append({"role": "assistant", "tool_calls": [tc]})
    messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(tool_output)})

    # Final assistant response after tool result
    final = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
    )

    final_msg = final.choices[0].message.content
    messages.append({"role": "assistant", "content": final_msg})
    return final_msg

# ────────────────────────────────────────────────────────────────
# 5. Console Interaction (Single Turn)
# ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        user_input = input("Enter your query (or type 'exit'): ")
        if user_input.lower() == "exit":
            break
        answer = chat_with_tools(user_input)
        print(f"Bot: {answer}\n")
