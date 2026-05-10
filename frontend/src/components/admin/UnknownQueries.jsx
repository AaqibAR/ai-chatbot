import { useEffect, useState } from "react"

function UnknownQueries() {
  const [queries, setQueries] = useState([])
  const [answers, setAnswers] = useState({})
  const [trained, setTrained] = useState({})

  useEffect(() => {
    fetch("http://localhost:8000/unknown-queries")
      .then(r => r.json())
      .then(setQueries)
      .catch(console.error)
  }, [])

  const handleTrain = async (q) => {
    const answer = answers[q.id]
    if (!answer?.trim()) return alert("Please enter an answer first!")
    try {
      await fetch("http://localhost:8000/learn", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: q.id, question: q.user_input, answer })
      })
      setTrained(prev => ({ ...prev, [q.id]: true }))
    } catch {
      alert("Failed to train. Is the backend running?")
    }
  }

  return (
    <div>
      {queries.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">✅</div>
          <p>No unknown queries yet! The bot is handling everything.</p>
        </div>
      ) : (
        <div className="query-list">
          {queries.map(q => (
            <div key={q.id} className={`query-card ${trained[q.id] ? "trained" : ""}`}>
              <div className="query-header">
                <span className="query-badge">#{q.id}</span>
                <span className="query-freq">Asked {q.frequency}x</span>
                {trained[q.id] && <span className="trained-badge">✅ Trained</span>}
              </div>
              <p className="query-text">"{q.user_input}"</p>
              {!trained[q.id] && (
                <div className="train-row">
                  <input
                    className="train-input"
                    placeholder="Type the answer to teach the bot..."
                    value={answers[q.id] || ""}
                    onChange={e => setAnswers(prev => ({ ...prev, [q.id]: e.target.value }))}
                  />
                  <button className="train-btn" onClick={() => handleTrain(q)}>
                    Train Bot
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default UnknownQueries