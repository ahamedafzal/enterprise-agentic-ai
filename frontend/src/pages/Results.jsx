import { useEffect, useState } from 'react'
import { FileText, ChevronDown, ChevronUp } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import api from '../utils/api'

export default function Results() {
  const [workflows, setWorkflows]   = useState([])
  const [expanded,  setExpanded]    = useState(null)

  useEffect(() => {
    api.get('/workflow/history').then(r => setWorkflows(r.data)).catch(() => {})
  }, [])

  const completed = workflows.filter(w => w.status === 'completed' && w.result?.final_report)

  return (
    <div className="p-8 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Results</h1>
        <p className="text-slate-400 text-sm mt-1">{completed.length} report{completed.length !== 1 ? 's' : ''} generated</p>
      </div>

      {completed.length === 0 ? (
        <div className="text-center py-24 text-slate-600">
          <FileText size={48} className="mx-auto mb-4 opacity-20" />
          <p>No reports yet. Run a workflow first.</p>
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          {completed.slice().reverse().map((w) => (
            <div key={w.id} className="bg-[#0d1117] border border-[#1e293b] rounded-xl overflow-hidden">
              <button
                onClick={() => setExpanded(expanded === w.id ? null : w.id)}
                className="w-full flex items-center justify-between p-5 hover:bg-[#0f1623] transition-all"
              >
                <div className="text-left">
                  <div className="text-sm font-medium text-slate-200 mb-1">{w.query}</div>
                  <div className="text-xs text-slate-500">{w.created_at}</div>
                </div>
                {expanded === w.id
                  ? <ChevronUp size={16} className="text-slate-400 flex-shrink-0" />
                  : <ChevronDown size={16} className="text-slate-400 flex-shrink-0" />
                }
              </button>
              {expanded === w.id && (
                <div className="px-5 pb-5 border-t border-[#1e293b]">
                  <div className="markdown mt-4">
                    <ReactMarkdown>{w.result.final_report}</ReactMarkdown>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}