import { useEffect, useState } from "react"

function Stats() {
  const [stats, setStats] = useState({ conversations: 0, unknown: 0, faqs: 0, learned: 0 })

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [convRes, unknownRes, faqRes, learnedRes] = await Promise.all([
          fetch("http://localhost:8000/conversations"),
          fetch("http://localhost:8000/unknown-queries"),
          fetch("http://localhost:8000/faqs"),
          fetch("http://localhost:8000/auto-learned")
        ])
        const [conv, unknown, faqs, learned] = await Promise.all([
          convRes.json(), unknownRes.json(), faqRes.json(), learnedRes.json()
        ])
        setStats({
          conversations: conv.length,
          unknown: unknown.length,
          faqs: faqs.length,
          learned: learned.length
        })
      } catch (e) {
        console.error(e)
      }
    }
    fetchStats()
  }, [])

  const cards = [
    { label: "Total Conversations", value: stats.conversations, icon: "💬" },
    { label: "Unknown Queries", value: stats.unknown, icon: "❓" },
    { label: "Knowledge Base FAQs", value: stats.faqs, icon: "🧠" },
    { label: "Auto Learned", value: stats.learned, icon: "✅" },
  ]

  return (
    <div>
      <div className="stats-grid">
        {cards.map(c => (
          <div key={c.label} className="stat-card">
            <div className="stat-icon">{c.icon}</div>
            <div className="stat-value">{c.value}</div>
            <div className="stat-label">{c.label}</div>
          </div>
        ))}
      </div>
      <div className="info-box">
        <h3>How training works</h3>
        <p>1. Users ask questions the bot doesn't understand → saved as Unknown Queries</p>
        <p>2. Go to <strong>Unknown Queries</strong> tab → click Train to teach the bot</p>
        <p>3. Answer is saved to the Knowledge Base → bot uses it for future users</p>
        <p>4. Bot also auto-learns when the same question is asked 3+ times</p>
      </div>
    </div>
  )
}

export default Stats