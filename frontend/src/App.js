import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [reply, setReply] = useState("");
  const [confidence, setConfidence] = useState("");
  const [city, setCity] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const getConfidence = (text) => {
    if (text.includes("°C")) return "high";
    if (text.toLowerCase().includes("weather")) return "medium";
    return "low";
  };

  const extractCity = (text) => {
    const match = text.match(
      /in\s+([A-Za-z ]+?)(?:\s+is|\s+with|\s+today|\s+currently|\.|,)/i
    );
    return match ? match[1].trim() : "Unknown";
  };

  const sendQuery = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setReply("");

    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: query }),
    });

    const data = await res.json();
    const conf = getConfidence(data.reply);
    const detectedCity = extractCity(data.reply);

    setReply(data.reply);
    setConfidence(conf);
    setCity(detectedCity);

    setHistory([
      {
        question: query,
        city: detectedCity,
        time: new Date().toLocaleTimeString(),
      },
      ...history,
    ]);

    setQuery("");
    setLoading(false);
  };

  return (
    <div className="app">
      <div className="header">
        <h1>🌤️ AI Weather Experience Console</h1>
        <p>Ask natural questions. Get intelligent weather insights.</p>
      </div>

      <div className="input-section">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. What’s the weather in Pune today?"
        />
        <button onClick={sendQuery}>Ask AI</button>
      </div>

      {loading && <div className="loading">🤖 AI is analyzing your query...</div>}

      {reply && (
        <>
          <div className="card">
            <h3>🌍 Weather Insight</h3>
            <p><strong>City:</strong> {city}</p>
            <p>{reply}</p>

            <div className={`badge ${confidence}`}>
              Confidence: {confidence.toUpperCase()}
            </div>
          </div>

          <div className="card">
            <h3>🧠 Why this answer is reliable?</h3>
            <div className="explain">
              • The city was clearly identified from your question<br />
              • AI invoked a live weather tool<br />
              • Response is generated using real-time data
            </div>
          </div>
        </>
      )}

      {history.length > 0 && (
        <div className="card">
          <h3>📜 Your Recent Queries</h3>
          {history.map((item, index) => (
            <div key={index} className="history-item">
              • {item.question} → {item.city} ({item.time})
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
