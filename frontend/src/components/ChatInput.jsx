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
    if (e.key === "Enter") handleSend()
  }

  return (
    <div className="chat-input">
      <input
        type="text"
        placeholder="Type a message..."
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={handleKey}
        disabled={loading}
      />
      <button onClick={handleSend} disabled={loading}>
        Send ➤
      </button>
    </div>
  )
}

export default ChatInput