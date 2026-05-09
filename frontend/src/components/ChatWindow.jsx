import { useEffect, useRef } from "react"
import "./ChatWindow.css"

function ChatWindow({ messages, loading, onSuggestion }) {
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const getTime = () => new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })

  return (
    <div className="chat-window">
      {messages.map((msg, i) => (
        <div key={i} className={`msg-row ${msg.sender}`}>
          {msg.sender === "bot" && <div className="msg-avatar">🤖</div>}
          <div>
            <div className={`bubble ${msg.sender}`}>
              {msg.text.split("\n").map((line, j) => (
                <span key={j}>{line}<br /></span>
              ))}
              {msg.suggestions && (
                <div className="suggestions">
                  {msg.suggestions.map(s => (
                    <button key={s} className="suggestion-chip" onClick={() => onSuggestion(s)}>
                      {s}
                    </button>
                  ))}
                </div>
              )}
            </div>
            <div className={`timestamp ${msg.sender === "bot" ? "bot-ts" : ""}`}>
              {getTime()}
            </div>
          </div>
          {msg.sender === "user" && <div className="msg-avatar user-av">👤</div>}
        </div>
      ))}
      {loading && (
        <div className="msg-row bot">
          <div className="msg-avatar">🤖</div>
          <div className="bubble bot">
            <div className="typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      )}
      <div ref={endRef} />
    </div>
  )
}

export default ChatWindow