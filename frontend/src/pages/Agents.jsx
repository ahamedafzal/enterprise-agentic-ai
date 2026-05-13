import { useEffect, useState } from 'react'
import AgentCard from '../components/AgentCard'
import api from '../utils/api'

export default function Agents() {
  const [agents, setAgents] = useState([])

  useEffect(() => {
    api.get('/agents/').then(r => setAgents(r.data.agents)).catch(() => {})
  }, [])

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Agent Monitor</h1>
        <p className="text-slate-400 text-sm mt-1">All 4 specialist agents in your workflow</p>
      </div>
      <div className="grid grid-cols-2 gap-4">
        {agents.map((agent) => (
          <AgentCard key={agent.id} agent={agent} status="idle" />
        ))}
      </div>
    </div>
  )
}