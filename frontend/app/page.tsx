"use client"

import { useState } from "react"
import AuthPage from "@/components/auth-page"
import DiscordApp from "@/components/discord-app"
import { useEffect } from "react";



export default function HomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<{ username: string; } | null>(null)

useEffect(() => {
  const checkSession = async () => {
    try {
      const res = await fetch("http://localhost:8080/info/me", {
        credentials: "include" // sends the session cookie automatically
      });
      if (!res.ok) throw new Error("Not logged in");

      const data = await res.json();
      setUser({ username: data.username });
      setIsAuthenticated(true);
    } catch {
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  checkSession();
}, []);


const handleLogin = async (userData: { username: string; password: string }) => {
  try {
    const res = await fetch("http://localhost:8080/info/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // important for cookies
      body: JSON.stringify(userData)
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Login failed");

    setUser({ username: data.username });
    setIsAuthenticated(true);
    alert("Login successful " + data.username);
  } catch (err: any) {
    console.error(err);
    alert(err.message);
  }
};



  const handleLogout = () => {
    localStorage.removeItem("token")
    setUser(null)
    setIsAuthenticated(false)
  }

  if (isAuthenticated && user) return <DiscordApp user={user} onLogout={handleLogout} />
  return <AuthPage onLogin={handleLogin} />
}
