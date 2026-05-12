import { NavLink } from 'react-router-dom'
import { Brain, LayoutDashboard, Bot, FileText, LogOut } from 'lucide-react'
import { useAuth } from '../store/AuthContext'

const links = [
  { to: '/',         icon: LayoutDashboard, label: 'Dashboard'   },
  { to: '/workflow', icon: Brain,           label: 'Run Workflow' },
  { to: '/agents',   icon: Bot,             label: 'Agents'       },
  { to: '/results',  icon: FileText,        label: 'Results'      },
]

export default function Sidebar() {
  const { logout, user } = useAuth()

  return (
    <aside style={{ width: '240px' }} className="fixed left-0 top-0 h-screen bg-[#0d1117] border-r border-[#1e293b] flex flex-col z-10">
      {/* Logo */}
      <div className="p-6 border-b border-[#1e293b]">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center">
            <Brain size={16} className="text-white" />
          </div>
          <div>
            <div className="text-sm font-semibold text-white">NEXUS</div>
            <div className="text-xs text-slate-500">Agentic AI Platform</div>
          </div>
        </div>
      </div>

      {/* Nav links */}
      <nav className="flex-1 p-4 flex flex-col gap-1">
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-150 ${
                isActive
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-[#1a2234]'
              }`
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* User + logout */}
      <div className="p-4 border-t border-[#1e293b]">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs font-medium text-slate-300">{user?.username}</div>
            <div className="text-xs text-slate-500">Administrator</div>
          </div>
          <button
            onClick={logout}
            className="p-2 text-slate-500 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-all"
          >
            <LogOut size={14} />
          </button>
        </div>
      </div>
    </aside>
  )
}