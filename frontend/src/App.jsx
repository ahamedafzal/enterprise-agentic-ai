import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider, useAuth } from './store/AuthContext'
import Sidebar from './components/Sidebar'
import Login    from './pages/Login'
import Dashboard from './pages/Dashboard'
import Workflow  from './pages/Workflow'
import Agents    from './pages/Agents'
import Results   from './pages/Results'

function ProtectedLayout({ children }) {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated) return <Navigate to="/login" replace />
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main style={{ marginLeft: '240px' }} className="flex-1 min-h-screen">
        {children}
      </main>
    </div>
  )
}

function AppRoutes() {
  const { isAuthenticated } = useAuth()
  return (
    <Routes>
      <Route path="/login" element={
        isAuthenticated ? <Navigate to="/" replace /> : <Login />
      } />
      <Route path="/" element={
        <ProtectedLayout><Dashboard /></ProtectedLayout>
      } />
      <Route path="/workflow" element={
        <ProtectedLayout><Workflow /></ProtectedLayout>
      } />
      <Route path="/agents" element={
        <ProtectedLayout><Agents /></ProtectedLayout>
      } />
      <Route path="/results" element={
        <ProtectedLayout><Results /></ProtectedLayout>
      } />
    </Routes>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Toaster
          position="top-right"
          toastOptions={{
            style: { background: '#1a2234', color: '#e2e8f0', border: '1px solid #2d3748' }
          }}
        />
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  )
}