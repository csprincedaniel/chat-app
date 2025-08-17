"use client"

import type React from "react"
import { useState } from "react"
import styles from "./auth-page.module.css"

interface AuthPageProps {
  onLogin: (userData: { username: string; password: string }) => void
}

export default function AuthPage({ onLogin }: AuthPageProps) {
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  })
  const [errors, setErrors] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    setErrors([])
  }

  const validateForm = () => {
    const newErrors: string[] = []

    if (!formData.email) newErrors.push("Email is required")
    else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.push("Email is invalid")

    if (!formData.password) newErrors.push("Password is required")
    else if (formData.password.length < 6) newErrors.push("Password must be at least 6 characters")

    if (!isLogin) {
      if (!formData.username) newErrors.push("Username is required")
      else if (formData.username.length < 3) newErrors.push("Username must be at least 3 characters")
      if (formData.password !== formData.confirmPassword) newErrors.push("Passwords do not match")
    }

    return newErrors
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const validationErrors = validateForm()
    if (validationErrors.length > 0) {
      setErrors(validationErrors)
      return
    }

    setIsLoading(true)
    setErrors([])

    setTimeout(() => {
      const userData = {
        username: formData.email, // email as login identifier
        password: formData.password
      }
      onLogin(userData)
      setIsLoading(false)
    }, 500)
  }

  const toggleMode = () => {
    setIsLogin(!isLogin)
    setFormData({ username: "", email: "", password: "", confirmPassword: "" })
    setErrors([])
  }

  return (
    <div className={styles.authContainer}>
      <div className={styles.authBackground}>
        <div className={styles.backgroundPattern}></div>
      </div>

      <div className={styles.authContent}>
        <div className={styles.authCard}>
          <div className={styles.authHeader}>
            <div className={styles.logo}>
              <span className={styles.logoIcon}>💬</span>
              <h1>ChatApp</h1>
            </div>
            <h2>{isLogin ? "Welcome back!" : "Create an account"}</h2>
            <p>{isLogin ? "We're so excited to see you again!" : "Join the conversation with friends!"}</p>
          </div>

          <form onSubmit={handleSubmit} className={styles.authForm}>
            {errors.length > 0 && (
              <div className={styles.errorContainer}>
                {errors.map((error, index) => (
                  <div key={index} className={styles.error}>{error}</div>
                ))}
              </div>
            )}

            {!isLogin && (
              <div className={styles.inputGroup}>
                <label htmlFor="username" className={styles.label}>
                  USERNAME <span className={styles.required}>*</span>
                </label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                  className={styles.input}
                  disabled={isLoading}
                />
              </div>
            )}

            <div className={styles.inputGroup}>
              <label htmlFor="email" className={styles.label}>
                EMAIL <span className={styles.required}>*</span>
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className={styles.input}
                disabled={isLoading}
              />
            </div>

            <div className={styles.inputGroup}>
              <label htmlFor="password" className={styles.label}>
                PASSWORD <span className={styles.required}>*</span>
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                className={styles.input}
                disabled={isLoading}
              />
            </div>

            {!isLogin && (
              <div className={styles.inputGroup}>
                <label htmlFor="confirmPassword" className={styles.label}>
                  CONFIRM PASSWORD <span className={styles.required}>*</span>
                </label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  className={styles.input}
                  disabled={isLoading}
                />
              </div>
            )}

            <button type="submit" className={styles.submitButton} disabled={isLoading}>
              {isLoading ? "Loading..." : isLogin ? "Log In" : "Continue"}
            </button>
          </form>

          <div className={styles.authFooter}>
            <span>
              {isLogin ? "Need an account? " : "Already have an account? "}
              <button type="button" onClick={toggleMode} className={styles.toggleButton}>
                {isLogin ? "Register" : "Log In"}
              </button>
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
