import { useState } from "react"
import "./ChatInput.css"

function ChatInput({ onSend, loading }) {
  const [text, setText] = useState("")

  const handleSend = () => {
    if (text.trim() && !loading) {
      onSend(text.trim())
      setText("")
    }
  }

  return (
    <div className="chat-input-wrap">
      <input
        type="text"
        className="chat-input"
        placeholder="Ask about packages, prices, bookings..."
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={e => e.key === "Enter" && handleSend()}
        disabled={loading}
      />
      <button className="send-btn" onClick={handleSend} disabled={loading}>
        ➤
      </button>
    </div>
  )
}

export default ChatInput