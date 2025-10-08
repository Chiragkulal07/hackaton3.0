import { Link } from 'react-router-dom'

export default function Nav() {
  return (
    <div className="fixed top-0 left-0 right-0 z-50">
      <div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between backdrop-blur bg-white/60 dark:bg-slate-900/60 rounded-b-xl shadow">
        <Link to="/" className="font-bold text-xl text-brand-700 dark:text-brand-300">
          CareerReady
        </Link>
        <div className="flex gap-3 text-sm">
          <Link
            to="/login"
            className="px-3 py-1.5 rounded-md bg-brand-600 text-white hover:bg-brand-700 transition"
          >
            Login
          </Link>
          <Link
            to="/register"
            className="px-3 py-1.5 rounded-md border border-brand-600 text-brand-700 dark:text-brand-300 hover:bg-brand-50 dark:hover:bg-slate-800 transition"
          >
            Register
          </Link>
        </div>
      </div>
    </div>
  )
}