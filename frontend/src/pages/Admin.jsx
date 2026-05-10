import { useState } from "react"
import Stats from "../components/admin/Stats"
import UnknownQueries from "../components/admin/UnknownQueries"
import KnowledgeBase from "../components/admin/KnowledgeBase"
import Conversations from "../components/admin/Conversations"
import "../admin.css"

const TABS = ["Dashboard", "Unknown Queries", "Knowledge Base", "Conversations"]

function Admin() {
  const [activeTab, setActiveTab] = useState("Dashboard")

  return (
    <div className="admin-wrap">
      <div className="admin-sidebar">
        <div className="admin-logo">
          <div className="admin-logo-icon">⚙️</div>
          <span className="admin-logo-text">Admin Panel</span>
        </div>
        <nav className="admin-nav">
          {TABS.map(tab => (
            <button
              key={tab}
              className={`admin-nav-btn ${activeTab === tab ? "active" : ""}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab === "Dashboard" && "📊 "}
              {tab === "Unknown Queries" && "❓ "}
              {tab === "Knowledge Base" && "🧠 "}
              {tab === "Conversations" && "💬 "}
              {tab}
            </button>
          ))}
        </nav>
        <a href="/" className="back-link">← Back to Chat</a>
      </div>

      <div className="admin-main">
        <div className="admin-topbar">
          <h1 className="admin-title">{activeTab}</h1>
        </div>
        <div className="admin-content">
          {activeTab === "Dashboard" && <Stats />}
          {activeTab === "Unknown Queries" && <UnknownQueries />}
          {activeTab === "Knowledge Base" && <KnowledgeBase />}
          {activeTab === "Conversations" && <Conversations />}
        </div>
      </div>
    </div>
  )
}

export default Admin