import { useEffect, useState } from 'react'
import { Brain, Activity, FileText, CheckCircle } from 'lucide-react'
import api from '../utils/api'

export default function Dashboard() {
  const [agents,    setAgents]    = useState([])
  const [workflows, setWorkflows] = useState([])

  useEffect(() => {
    api.get('/agents/').then(r => setAgents(r.data.agents)).catch(() => {})
    api.get('/workflow/history').then(r => setWorkflows(r.data)).catch(() => {})
  }, [])

  const stats = [
    { label: 'Active Agents',      value: agents.length,                            icon: Brain,      color: 'text-blue-400',  bg: 'bg-blue-400/10'  },
    { label: 'Workflows Run',      value: workflows.length,                          icon: Activity,   color: 'text-green-400', bg: 'bg-green-400/10' },
    { label: 'Completed',          value: workflows.filter(w=>w.status==='completed').length, icon: CheckCircle, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
    { label: 'Reports Generated',  value: workflows.filter(w=>w.result).length,     icon: FileText,   color: 'text-purple-400', bg: 'bg-purple-400/10' },
  ]

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-slate-400 text-sm mt-1">NEXUS Enterprise Agentic AI Platform</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        {stats.map(({ label, value, icon: Icon, color, bg }) => (
          <div key={label} className="bg-[#0d1117] border border-[#1e293b] rounded-xl p-5">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs text-slate-500">{label}</span>
              <div className={`p-2 rounded-lg ${bg}`}>
                <Icon size={14} className={color} />
              </div>
            </div>
            <div className="text-3xl font-bold text-white">{value}</div>
          </div>
        ))}
      </div>

      {/* Recent workflows */}
      <div className="bg-[#0d1117] border border-[#1e293b] rounded-xl p-6">
        <h2 className="text-sm font-semibold text-slate-300 mb-4">Recent Workflows</h2>
        {workflows.length === 0 ? (
          <div className="text-center py-12 text-slate-600">
            <Brain size={40} className="mx-auto mb-3 opacity-30" />
            <p className="text-sm">No workflows yet. Run your first query.</p>
          </div>
        ) : (
          <div className="flex flex-col gap-2">
            {workflows.slice(-5).reverse().map((w) => (
              <div key={w.id} className="flex items-center justify-between p-3 bg-[#0f1623] rounded-lg border border-[#1e293b]">
                <div className="text-sm text-slate-300 truncate flex-1 mr-4">{w.query}</div>
                <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                  w.status === 'completed' ? 'bg-green-400/10 text-green-400' :
                  w.status === 'failed'    ? 'bg-red-400/10 text-red-400'     :
                  'bg-blue-400/10 text-blue-400'
                }`}>{w.status}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}