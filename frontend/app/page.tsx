"use client"

import { useState } from "react"
import AuthPage from "@/components/auth-page"
import DiscordApp from "@/components/discord-app"

export default function HomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<{ username: string; password: string } | null>(null)

  const handleLogin = (userData: { username: string; password: string }) => {
    const url = `http://localhost:8080/info/username?username=${encodeURIComponent(userData.username)}`

    fetch(url)
      .then(res => {
        if (!res.ok) throw new Error('Network error')
        return res.json()
      })
      .then(data => {
        if (data.username === userData.username && data.password === userData.password) {
          setUser({ username: data.username, password: data.password })
          setIsAuthenticated(true)
          alert("Login Successfull " + data.username)
        } else {
          alert(`Login failed. Expected: "${data.username}" / "${data.password}", you entered: "${userData.username}" / "${userData.password}"`)
        }
      })
      .catch(err => {
        console.error(err)
        alert('Failed to fetch user')
      })
  }

  const handleLogout = () => {
    setUser(null)
    setIsAuthenticated(false)
  }

  if (isAuthenticated && user) return <DiscordApp user={user} onLogout={handleLogout} />
  return <AuthPage onLogin={handleLogin} />
}
