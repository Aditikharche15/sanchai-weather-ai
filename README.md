AI Weather Experience Console

An AI-powered weather application that provides intelligent, natural-language weather insights for past, present, and future conditions, along with context-aware recommendations (e.g., suitability for outdoor activities like cricket).

This project demonstrates end-to-end development involving:

Frontend (React)

Backend (FastAPI)

AI reasoning (LLM via OpenRouter)

Deterministic data handling (Weather API)

Secure environment configuration

Key Features

Ask questions like:

“What is the weather in Pune today?”

“What will the weather of Bangalore after two days?”

“Is today’s weather suitable for playing cricket in Delhi?”

Temporal Reasoning

Current weather

Past weather (e.g., yesterday, X days ago)

Future weather (e.g., tomorrow, after X days)



Multi-line, human-readable responses

Secure API Key Handling

API keys stored in .env (never committed)

.env.example provided for setup guidance
Tech Stack
Frontend

React.js

HTML / CSS

Fetch API

Backend

FastAPI

Python

LangChain (LLM interface)

OpenRouter (LLM provider)


📁 Project Structure
sanchai-weather-ai/
│
├── backend/
│   ├── agent.py            # Intent parsing & AI response logic
│   ├── main.py             # FastAPI server
│   ├── weather_tool.py     # Weather data fetching
│   ├── requirements.txt
│   ├── .env.example        # Sample environment config
│
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── public/
│   └── package.json
│
├── .gitignore
└── README.md

⚙️ Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/aditikharche15/sanchai-weather-ai.git
cd sanchai-weather-ai

2️⃣ Backend Setup (FastAPI)
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt


Create a .env file:

OPENROUTER_API_KEY=your_openrouter_api_key_here


Run backend:

uvicorn main:app --reload


Backend runs on:

http://127.0.0.1:8000

3️⃣ Frontend Setup (React)
cd frontend
npm install
npm start


Frontend runs on:

http://localhost:3000

🔍 How It Works (Design Explanation)

User enters a weather query

Backend:

Extracts city, time reference, and condition

Fetches weather data deterministically

LLM:

Uses fetched data to generate a clear, structured explanation

Frontend:

Displays response with confidence indicators and history

🔹 Why this design?

Reliability

Predictability

Reduced hallucination

Production-ready behavior

🔐 Security Practices

❌ .env is never committed

✅ .env.example included

✅ API keys loaded via environment variables

✅ .gitignore blocks secrets and cache files

🧪 Example Queries
What is the weather in Pune today?
What will the weather of Bangalore after two days?
Was it raining yesterday in Mumbai?
Is today’s weather suitable for playing cricket in Delhi?
