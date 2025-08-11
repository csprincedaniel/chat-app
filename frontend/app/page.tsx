"use client"

import { useState } from "react"
import AuthPage from "@/components/auth-page"
import DiscordApp from "@/components/discord-app"

export default function HomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<{ username: string; email: string } | null>(null)

  const handleLogin = (userData: { username: string; email: string }) => {
    setUser(userData)
    setIsAuthenticated(true)
  }

  const handleLogout = () => {
    setUser(null)
    setIsAuthenticated(false)
  }

  if (isAuthenticated && user) {
    return <DiscordApp user={user} onLogout={handleLogout} />
  }

  return <AuthPage onLogin={handleLogin} />
}
