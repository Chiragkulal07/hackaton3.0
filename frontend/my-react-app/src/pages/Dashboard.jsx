import { useEffect, useState } from 'react'
import Page from '../components/Page'
import { getMe } from '../lib/api'

export default function Dashboard() {
  const [me, setMe] = useState(null)

  useEffect(() => {
    getMe().then(setMe).catch(() => setMe({ authenticated: false }))
  }, [])

  return (
    <Page>
      <div className="pt-28 mx-auto max-w-6xl px-4">
        <h2 className="text-3xl font-bold">Dashboard</h2>
        <p className="opacity-70">Your readiness overview and next steps</p>
        <div className="mt-6 rounded-xl bg-white/70 dark:bg-slate-900/70 backdrop-blur p-4 shadow">
          <pre className="text-sm opacity-80">{JSON.stringify(me, null, 2)}</pre>
        </div>
      </div>
    </Page>
  )
}