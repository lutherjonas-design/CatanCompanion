export async function getGames() {
  const res = await fetch('/api/games')
  if (!res.ok) throw new Error(`Failed to load games: ${res.status}`)
  return res.json()
}

export async function createGame(name: string) {
  const res = await fetch('/api/games', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  })
  if (!res.ok) throw new Error(`Failed to create game: ${res.status}`)
  return res.json()
}
