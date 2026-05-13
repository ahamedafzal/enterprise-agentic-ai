import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken]   = useState(localStorage.getItem('nexus_token'))
  const [user,  setUser]    = useState(null)

  useEffect(() => {
    if (token) setUser({ username: 'admin' })
  }, [token])

  const login = (newToken) => {
    localStorage.setItem('nexus_token', newToken)
    setToken(newToken)
    setUser({ username: 'admin' })
  }

  const logout = () => {
    localStorage.removeItem('nexus_token')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ token, user, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)