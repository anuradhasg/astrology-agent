import { useState, useCallback } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export function useChat() {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'agent',
      content: "Hello! I'm your AI astrology assistant. Tell me your birthdate to find your zodiac sign, ask for today's horoscope, check compatibility between two signs, or learn about a sign's traits and ruling planet.",
      toolsUsed: [],
    },
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const sendMessage = useCallback(async (question) => {
    if (!question.trim() || isLoading) return

    const userMsg = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: question.trim(),
      toolsUsed: [],
    }

    setMessages((prev) => [...prev, userMsg])
    setIsLoading(true)
    setError(null)

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question.trim(), session_id: null }),
      })

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `Server error ${res.status}` }))
        throw new Error(err.detail || `Server error ${res.status}`)
      }

      const data = await res.json()

      setMessages((prev) => [
        ...prev,
        {
          id: `agent-${Date.now()}`,
          role: 'agent',
          content: data.answer,
          toolsUsed: data.tools_used || [],
        },
      ])
    } catch (err) {
      const msg = err.message.includes('fetch')
        ? 'Cannot reach the astrology agent API. Make sure it\'s running on localhost:8000'
        : err.message
      setError(msg)
      setMessages((prev) => [
        ...prev,
        {
          id: `agent-err-${Date.now()}`,
          role: 'agent',
          content: "I couldn't reach the stars right now. Please check the API is running.",
          toolsUsed: [],
          isError: true,
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }, [isLoading])

  return { messages, isLoading, error, sendMessage, setError }
}
