import { useState } from "react"
import ChatWindow from "./components/ChatWindow"
import ChatInput from "./components/ChatInput"
import "./App.css"

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! Welcome to the Travel Assistant. How can I help you today? 🌍" }
  ])
  const [loading, setLoading] = useState(false)

  const sendMessage = async (userText) => {
    const userMessage = { sender: "user", text: userText }
    setMessages(prev => [...prev, userMessage])
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
      <div className="chat-container">
        <div className="chat-header">
          <div className="header-avatar">✈️</div>
          <div>
            <h2>Travel Assistant</h2>
            <span className="status">● Online</span>
          </div>
        </div>
        <ChatWindow messages={messages} loading={loading} />
        <ChatInput onSend={sendMessage} loading={loading} />
      </div>
    </div>
  )
}

export default App