import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from weather_tool import get_weather

# Load environment variables
load_dotenv()

# Initialize LLM (USED ONLY FOR RESPONSE FORMATTING)
llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# -----------------------------
# Helper Functions
# -----------------------------

def extract_city(query: str):
    """
    Extract city name from natural language queries.

    Handles cases like:
    - in Pune
    - of Bangalore
    - at Mumbai
    - for Delhi
    - Bangalore weather
    - weather of New Delhi
    - weather in Mumbai city?
    - what will the weather be tomorrow in Bengaluru?
    """

    q = query.strip()

    # 1️⃣ Strong patterns with prepositions (MOST RELIABLE)
    patterns = [
        r"(?:in|of|at|for)\s+([A-Za-z ]+?)(?:\s+city|\s+today|\s+yesterday|\s+tomorrow|\s+after|\s+before|\s+next|\s+last|\?|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, q, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    # 2️⃣ Fallback: "<City> weather" or "weather <City>"
    match = re.search(
        r"(?:weather\s+(?:in|of)?\s*([A-Za-z ]+)|([A-Za-z ]+)\s+weather)",
        q,
        re.IGNORECASE
    )
    if match:
        return (match.group(1) or match.group(2)).strip()

    # 3️⃣ Last fallback: capitalized word(s) (VERY conservative)
    match = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", q)
    if match:
        # Return the longest capitalized phrase (likely city)
        return max(match, key=len)

    return None



def detect_mode(query: str):
    """
    Detect time intent and return:
    (mode, day_offset)

    mode: current | past | future
    day_offset: int (negative = past, positive = future)
    """

    q = query.lower()

    # -------------------------
    # Explicit day offsets
    # -------------------------

    # after X days
    match = re.search(r"after\s+(\d+)\s+day", q)
    if match:
        return "future", int(match.group(1))

    # before X days
    match = re.search(r"before\s+(\d+)\s+day", q)
    if match:
        return "past", -int(match.group(1))

    # X days ago
    match = re.search(r"(\d+)\s+day[s]?\s+ago", q)
    if match:
        return "past", -int(match.group(1))

    # -------------------------
    # Weeks
    # -------------------------

    if "next week" in q:
        return "future", 7

    if "last week" in q:
        return "past", -7

    # -------------------------
    # Years (approx conversion)
    # -------------------------

    # after X years
    match = re.search(r"after\s+(\d+)\s+year", q)
    if match:
        return "future", int(match.group(1)) * 365

    # before X years
    match = re.search(r"before\s+(\d+)\s+year", q)
    if match:
        return "past", -int(match.group(1)) * 365

    # X years ago
    match = re.search(r"(\d+)\s+year[s]?\s+ago", q)
    if match:
        return "past", -int(match.group(1)) * 365

    # -------------------------
    # Simple keywords
    # -------------------------

    if "yesterday" in q:
        return "past", -1

    if "tomorrow" in q:
        return "future", 1

    if "today" in q or "now" in q:
        return "current", 0

    # -------------------------
    # Generic past / future words
    # -------------------------

    if "past" in q or "previous" in q:
        return "past", -1

    if "future" in q or "upcoming" in q:
        return "future", 1

    # -------------------------
    # Default
    # -------------------------
    return "current", 0




def detect_condition(query: str):
    """
    Detect what weather detail is being asked.
    """
    q = query.lower()

    if "rain" in q:
        return "rain"
    elif "temperature" in q or "temp" in q:
        return "temperature"
    elif "humidity" in q:
        return "humidity"
    elif "wind" in q:
        return "wind"
    else:
        return "summary"


# -----------------------------
# Main Agent Function
# -----------------------------

def ask_agent(query: str) -> str:
    """
    Main function called by FastAPI.
    Handles:
    - Today
    - Past (yesterday)
    - Future (tomorrow)
    - Condition-based questions
    """

    # 1️⃣ Extract city
    city = extract_city(query)
    if not city:
        return "Please mention a city name in your question."

    # 2️⃣ Detect intent
    mode, day_offset = detect_mode(query)
    condition = detect_condition(query)

    # 3️⃣ Fetch weather deterministically (NO LLM HERE)
    weather_result = get_weather(
        city=city,
        mode=mode,
        day_offset=day_offset,
        condition=condition
    )

    # 4️⃣ Use LLM ONLY to generate a clean response
    prompt = f"""
    User Question: {query}
    Weather Data: {weather_result}
    Write a detailed, well-structured explanation in 5–7 lines.
    Guidelines:
    - Start with a clear summary sentence.
    - Explain temperature, sky condition, and comfort level.
    - Mention whether it is suitable for outdoor activities if relevant.
    - Keep the tone informative and friendly.
    - Do NOT repeat the question verbatim.
    """


    response = llm.invoke(prompt)

    return response.content
