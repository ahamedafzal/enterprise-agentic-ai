import { CheckCircle, Loader, Clock, XCircle } from 'lucide-react'

const statusConfig = {
  idle:      { icon: Clock,       color: 'text-slate-400', bg: 'bg-slate-400/10', label: 'Idle'       },
  running:   { icon: Loader,      color: 'text-blue-400',  bg: 'bg-blue-400/10',  label: 'Running'    },
  completed: { icon: CheckCircle, color: 'text-green-400', bg: 'bg-green-400/10', label: 'Done'       },
  failed:    { icon: XCircle,     color: 'text-red-400',   bg: 'bg-red-400/10',   label: 'Failed'     },
}

export default function AgentCard({ agent, status = 'idle' }) {
  const cfg  = statusConfig[status] || statusConfig.idle
  const Icon = cfg.icon

  return (
    <div className={`p-4 rounded-xl border transition-all duration-300 ${
      status === 'running'
        ? 'border-blue-600/40 bg-blue-600/5 shadow-lg shadow-blue-600/10'
        : 'border-[#1e293b] bg-[#0d1117]'
    }`}>
      <div className="flex items-start justify-between mb-3">
        <div className={`p-2 rounded-lg ${cfg.bg}`}>
          <Icon size={16} className={`${cfg.color} ${status === 'running' ? 'animate-spin' : ''}`} />
        </div>
        <span className={`text-xs px-2 py-1 rounded-full ${cfg.bg} ${cfg.color} font-medium`}>
          {cfg.label}
        </span>
      </div>
      <div className="text-sm font-medium text-slate-200 mb-1">{agent.name}</div>
      <div className="text-xs text-slate-500 leading-relaxed">{agent.description}</div>
      <div className="mt-3 flex flex-wrap gap-1">
        {agent.tools?.map((tool) => (
          <span key={tool} className="text-xs px-2 py-0.5 bg-[#1a2234] text-slate-400 rounded-md border border-[#2d3748]">
            {tool}
          </span>
        ))}
      </div>
    </div>
  )
}