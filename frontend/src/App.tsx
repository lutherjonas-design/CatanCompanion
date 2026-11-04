import React, { useEffect, useState } from 'react'
import { getGames, createGame } from './api'

interface Game { id: number; name: string; created_at: string }

export default function App() {
  const [games, setGames] = useState<Game[]>([])
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = async () => {
    try {
      setLoading(true)
      const data = await getGames()
      setGames(data)
      setError(null)
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const onCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return
    try {
      const g = await createGame(name.trim())
      setGames(prev => [g, ...prev])
      setName('')
    } catch (e: any) {
      setError(e.message)
    }
  }

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', maxWidth: 800, margin: '40px auto' }}>
      <h1>Settlers of Catan Companion</h1>
      <p>This demo lists games from the backend and lets you add a new one.</p>
      {error && <div style={{ color: 'red' }}>Error: {error}</div>}
      <form onSubmit={onCreate} style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="New game name"
          style={{ flex: 1, padding: 8 }}
        />
        <button type="submit" style={{ padding: '8px 16px' }}>Create</button>
      </form>
      {loading ? (
        <div>Loading…</div>
      ) : (
        <ul>
          {games.map(g => (
            <li key={g.id}>
              <strong>{g.name}</strong> <small>({new Date(g.created_at).toLocaleString()})</small>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
