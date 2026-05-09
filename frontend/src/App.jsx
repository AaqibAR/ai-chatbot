import { useState } from "react"
import ChatWindow from "./components/ChatWindow"
import ChatInput from "./components/ChatInput"
import "./App.css"

const QUICK_BUTTONS = [
  { label: "Packages", msg: "Show me all packages" },
  { label: "Prices", msg: "What are the prices?" },
  { label: "Book a tour", msg: "I want to book a tour" },
  { label: "FAQs", msg: "Show me FAQs" },
]

const DESTINATIONS = [
  { label: "Kandy", msg: "Tell me about Kandy" },
  { label: "Ella", msg: "Tell me about Ella" },
  { label: "Sigiriya", msg: "Tell me about Sigiriya" },
]

function App() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! I'm your Sri Lanka travel assistant. I can help you explore our packages, check prices, and plan your perfect trip!",
      suggestions: ["View packages", "Check prices", "Book now"]
    }
  ])
  const [loading, setLoading] = useState(false)

  const sendMessage = async (userText) => {
    setMessages(prev => [...prev, { sender: "user", text: userText }])
    setLoading(true)
    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText })
      })
      const data = await res.json()
      setMessages(prev => [...prev, { sender: "bot", text: data.response }])
    } catch {
      setMessages(prev => [...prev, { sender: "bot", text: "Sorry, I'm having trouble connecting. Please try again!" }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="chat-wrap">
        <div className="sidebar">
          <div className="sidebar-logo">
            <div className="logo-icon">✈️</div>
            <span className="logo-text">TravelBot</span>
          </div>
          <div className="sidebar-label">Quick access</div>
          {QUICK_BUTTONS.map(b => (
            <button key={b.label} className="quick-btn" onClick={() => sendMessage(b.msg)}>
              {b.label}
            </button>
          ))}
          <hr className="sidebar-divider" />
          <div className="sidebar-label">Destinations</div>
          {DESTINATIONS.map(d => (
            <button key={d.label} className="quick-btn" onClick={() => sendMessage(d.msg)}>
              {d.label}
            </button>
          ))}
        </div>

        <div className="main">
          <div className="chat-header">
            <div className="chat-header-left">
              <div className="avatar">🤖</div>
              <div className="chat-header-info">
                <p>Travel Assistant</p>
                <span className="status">● Online</span>
              </div>
            </div>
          </div>
          <ChatWindow messages={messages} loading={loading} onSuggestion={sendMessage} />
          <ChatInput onSend={sendMessage} loading={loading} />
        </div>
      </div>
    </div>
  )
}

export default App