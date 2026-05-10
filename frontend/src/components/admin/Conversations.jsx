import { useEffect, useState } from "react"

function Conversations() {
  const [convs, setConvs] = useState([])

  useEffect(() => {
    fetch("http://localhost:8000/conversations")
      .then(r => r.json())
      .then(setConvs)
      .catch(console.error)
  }, [])

  return (
    <div>
      <p className="conv-count">Showing last {convs.length} conversations</p>
      <div className="conv-list">
        {convs.map(c => (
          <div key={c.id} className="conv-card">
            <div className="conv-row user-conv">
              <span className="conv-label">User</span>
              <p>{c.user_input}</p>
            </div>
            <div className="conv-row bot-conv">
              <span className="conv-label">Bot</span>
              <p>{c.bot_response}</p>
            </div>
            <div className="conv-time">{new Date(c.timestamp).toLocaleString()}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Conversations