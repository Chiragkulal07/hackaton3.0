import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Page from '../components/Page'
import { loginUser } from '../lib/api'

export default function Login() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)

  const onSubmit = async (e) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const username = formData.get('username')
    const password = formData.get('password')
    setLoading(true)
    try {
      await loginUser({ username, password })
      navigate('/dashboard')
    } catch {
      alert('Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Page>
      <div className="pt-28">
        <div className="mx-auto max-w-md px-4">
          <div className="rounded-2xl bg-white/70 dark:bg-slate-900/70 backdrop-blur shadow-xl p-6">
            <h2 className="text-2xl font-bold">Welcome back</h2>
            <p className="opacity-70 text-sm">Log in to access your dashboard</p>
            <form className="mt-6 space-y-3" onSubmit={onSubmit}>
              <input name="username" placeholder="Username" className="w-full rounded-lg border px-3 py-2 text-black" />
              <input type="password" name="password" placeholder="Password" className="w-full rounded-lg border px-3 py-2 text-black" />
              <button disabled={loading} className="w-full px-4 py-2 rounded-lg bg-brand-600 hover:bg-brand-700 text-white transition">
                {loading ? 'Signing in…' : 'Login'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </Page>
  )
}