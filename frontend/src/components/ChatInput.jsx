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

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-input-wrap">
      <textarea
        className="chat-input"
        placeholder="Ask about packages, prices, bookings..."
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={handleKey}
        disabled={loading}
        rows={1}
      />
      <button className="send-btn" onClick={handleSend} disabled={loading}>
        ➤
      </button>
    </div>
  )
}

export default ChatInput