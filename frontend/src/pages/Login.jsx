import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Brain, Loader } from 'lucide-react'
import { useAuth } from '../store/AuthContext'
import api from '../utils/api'
import toast from 'react-hot-toast'

export default function Login() {
  const [form,    setForm]    = useState({ username: '', password: '' })
  const [loading, setLoading] = useState(false)
  const { login }             = useAuth()
  const navigate              = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await api.post('/auth/login', form)
      login(res.data.access_token)
      toast.success('Welcome to NEXUS')
      navigate('/')
    } catch {
      toast.error('Invalid credentials')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#0f1117] flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-blue-600/20 border border-blue-600/30 mb-4">
            <Brain size={32} className="text-blue-400" />
          </div>
          <h1 className="text-2xl font-bold text-white">NEXUS</h1>
          <p className="text-slate-400 text-sm mt-1">Enterprise Agentic AI Platform</p>
        </div>

        {/* Card */}
        <div className="bg-[#0d1117] border border-[#1e293b] rounded-2xl p-8">
          <h2 className="text-lg font-semibold text-white mb-6">Sign in</h2>
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div>
              <label className="text-xs text-slate-400 mb-1.5 block">Username</label>
              <input
                type="text"
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
                placeholder="admin"
                className="w-full bg-[#1a2234] border border-[#2d3748] rounded-lg px-4 py-2.5 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors"
              />
            </div>
            <div>
              <label className="text-xs text-slate-400 mb-1.5 block">Password</label>
              <input
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                placeholder="••••••••"
                className="w-full bg-[#1a2234] border border-[#2d3748] rounded-lg px-4 py-2.5 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-medium py-2.5 rounded-lg text-sm transition-all flex items-center justify-center gap-2 mt-2"
            >
              {loading ? <><Loader size={14} className="animate-spin" /> Signing in...</> : 'Sign in'}
            </button>
          </form>
          <p className="text-xs text-slate-600 text-center mt-4">
            Demo credentials: admin / nexus123
          </p>
        </div>
      </div>
    </div>
  )
}