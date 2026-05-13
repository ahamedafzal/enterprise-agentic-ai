import { useState, useEffect, useRef } from 'react'
import { Brain, Send, Loader, CheckCircle } from 'lucide-react'
import api from '../utils/api'
import toast from 'react-hot-toast'
import ReactMarkdown from 'react-markdown'

const SAMPLE_QUERIES = [
  "Analyse our Q4 project delays and identify the highest risk projects",
  "Which departments have the highest employee attrition risk?",
  "Summarise all vendor contracts expiring in the next 90 days",
  "Generate an executive briefing on our AI initiative status",
]

const AGENT_STEPS = [
  { key: 'orchestrating', label: 'Orchestrator Agent',     desc: 'Decomposing your query into subtasks...'           },
  { key: 'analysing',     label: 'Document Analyst Agent', desc: 'Reading reports, contracts and documents...'       },
  { key: 'retrieving',    label: 'Data Retrieval Agent',   desc: 'Querying structured data and statistics...'        },
  { key: 'generating',    label: 'Report Generator Agent', desc: 'Synthesising findings into executive report...'    },
]

export default function Workflow() {
  const [query,    setQuery]    = useState('')
  const [loading,  setLoading]  = useState(false)
  const [step,     setStep]     = useState(-1)
  const [result,   setResult]   = useState(null)
  const resultRef               = useRef(null)

  const handleRun = async () => {
    if (!query.trim()) return toast.error('Enter a query first')
    setLoading(true)
    setResult(null)
    setStep(0)

    // Simulate step progress while waiting
    const stepInterval = setInterval(() => {
      setStep(s => (s < AGENT_STEPS.length - 1 ? s + 1 : s))
    }, 4000)

    try {
      const res = await api.get('/workflow/run-sync', { params: { query } })
      clearInterval(stepInterval)
      setStep(AGENT_STEPS.length)
      setResult(res.data)
      toast.success('Workflow completed!')
      setTimeout(() => resultRef.current?.scrollIntoView({ behavior: 'smooth' }), 300)
    } catch (err) {
      clearInterval(stepInterval)
      toast.error('Workflow failed. Check backend.')
      setStep(-1)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-8 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Run Workflow</h1>
        <p className="text-slate-400 text-sm mt-1">Submit a query and watch 4 AI agents work in sequence</p>
      </div>

      {/* Query input */}
      <div className="bg-[#0d1117] border border-[#1e293b] rounded-xl p-6 mb-6">
        <label className="text-xs text-slate-400 mb-2 block">Enterprise Query</label>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. Analyse our Q4 project delays and generate an executive action plan..."
          rows={4}
          className="w-full bg-[#0f1623] border border-[#2d3748] rounded-lg px-4 py-3 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors resize-none"
        />
        {/* Sample queries */}
        <div className="mt-3 flex flex-wrap gap-2">
          {SAMPLE_QUERIES.map((q) => (
            <button
              key={q}
              onClick={() => setQuery(q)}
              className="text-xs px-3 py-1.5 bg-[#1a2234] hover:bg-[#1e293b] text-slate-400 hover:text-slate-200 rounded-lg border border-[#2d3748] transition-all"
            >
              {q.slice(0, 40)}...
            </button>
          ))}
        </div>
        <button
          onClick={handleRun}
          disabled={loading || !query.trim()}
          className="mt-4 flex items-center gap-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white font-medium px-6 py-2.5 rounded-lg text-sm transition-all"
        >
          {loading ? <Loader size={14} className="animate-spin" /> : <Send size={14} />}
          {loading ? 'Running agents...' : 'Run Workflow'}
        </button>
      </div>

      {/* Agent progress */}
      {step >= 0 && (
        <div className="bg-[#0d1117] border border-[#1e293b] rounded-xl p-6 mb-6">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Agent Pipeline</h2>
          <div className="flex flex-col gap-3">
            {AGENT_STEPS.map((s, i) => (
              <div key={s.key} className={`flex items-center gap-4 p-3 rounded-lg transition-all duration-500 ${
                i === step && loading ? 'bg-blue-600/10 border border-blue-600/20' :
                i < step || (!loading && step === AGENT_STEPS.length) ? 'bg-green-600/5 border border-green-600/10' :
                'border border-transparent'
              }`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                  i < step || (!loading && step === AGENT_STEPS.length) ? 'bg-green-500/20' :
                  i === step && loading ? 'bg-blue-500/20' : 'bg-[#1a2234]'
                }`}>
                  {(i < step || (!loading && step === AGENT_STEPS.length)) ? (
                    <CheckCircle size={14} className="text-green-400" />
                  ) : i === step && loading ? (
                    <Loader size={14} className="text-blue-400 animate-spin" />
                  ) : (
                    <span className="text-xs text-slate-600">{i + 1}</span>
                  )}
                </div>
                <div>
                  <div className="text-sm font-medium text-slate-200">{s.label}</div>
                  <div className="text-xs text-slate-500">{s.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Results */}
      {result?.result?.final_report && (
        <div ref={resultRef} className="bg-[#0d1117] border border-[#1e293b] rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle size={16} className="text-green-400" />
            <h2 className="text-sm font-semibold text-slate-300">Executive Report</h2>
          </div>
          <div className="markdown">
            <ReactMarkdown>{result.result.final_report}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  )
}