import { useEffect, useRef } from "react"
import "./ChatWindow.css"

function ChatWindow({ messages, loading }) {
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  return (
    <div className="chat-window">
      {messages.map((msg, i) => (
        <div key={i} className={`message ${msg.sender}`}>
          <div className="bubble">{msg.text}</div>
        </div>
      ))}
      {loading && (
        <div className="message bot">
          <div className="bubble typing">
            <span></span><span></span><span></span>
          </div>
        </div>
      )}
      <div ref={endRef} />
    </div>
  )
}

export default ChatWindow