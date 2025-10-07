import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import './App.css'
import { loginUser, registerUser, getMe } from './lib/api'

function Page({ children }) {
	return (
		<motion.div
			initial={{ opacity: 0, y: 20 }}
			animate={{ opacity: 1, y: 0 }}
			exit={{ opacity: 0, y: -20 }}
			transition={{ duration: 0.5, ease: 'easeOut' }}
			className="min-h-screen"
		>
			{children}
		</motion.div>
	)
}

function Nav() {
	return (
		<div className="fixed top-0 left-0 right-0 z-50">
			<div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between backdrop-blur bg-white/60 dark:bg-slate-900/60 rounded-b-xl shadow">
				<Link to="/" className="font-bold text-xl text-brand-700 dark:text-brand-300">CareerReady</Link>
				<div className="flex gap-3 text-sm">
					<Link to="/login" className="px-3 py-1.5 rounded-md bg-brand-600 text-white hover:bg-brand-700 transition">Login</Link>
					<Link to="/register" className="px-3 py-1.5 rounded-md border border-brand-600 text-brand-700 dark:text-brand-300 hover:bg-brand-50 dark:hover:bg-slate-800 transition">Register</Link>
				</div>
			</div>
		</div>
	)
}

function Landing() {
	return (
		<Page>
			<div className="pt-28">
				<section className="mx-auto max-w-6xl px-4 grid lg:grid-cols-2 gap-10 items-center">
					<motion.div initial={{ opacity: 0, x: -40 }} whileInView={{ opacity: 1, x: 0 }} transition={{ duration: 0.6 }}>
						<h1 className="text-5xl font-extrabold leading-tight">
							Unlock Your Career Potential
						</h1>
						<p className="mt-4 text-lg opacity-80">Assess your core skills, get personalized feedback, and discover roles where you can thrive.</p>
						<div className="mt-6 flex gap-3">
							<Link to="/register" className="px-5 py-3 rounded-lg bg-brand-600 text-white shadow hover:shadow-lg hover:-translate-y-0.5 transition">Get Started</Link>
							<Link to="/login" className="px-5 py-3 rounded-lg border border-brand-600 text-brand-700 dark:text-brand-300 hover:bg-brand-50 dark:hover:bg-slate-800 transition">I already have an account</Link>
						</div>
					</motion.div>
					<motion.div initial={{ opacity: 0, x: 40 }} whileInView={{ opacity: 1, x: 0 }} transition={{ duration: 0.6 }} className="relative">
						<div className="absolute inset-0 bg-gradient-to-tr from-brand-200 to-brand-500 blur-3xl opacity-30 rounded-full -z-10"></div>
						<div className="grid grid-cols-3 gap-4">
							{Array.from({ length: 9 }).map((_, i) => (
								<motion.div key={i} whileHover={{ scale: 1.05 }} className="aspect-square rounded-xl bg-white/80 dark:bg-slate-800/80 shadow flex items-center justify-center text-sm">
									<span className="opacity-60">Skill {i + 1}</span>
								</motion.div>
							))}
						</div>
					</motion.div>
				</section>
			</div>
		</Page>
	)
}

function PageShell({ children }) {
	return (
		<div className="min-h-screen">
			<Nav />
			{children}
		</div>
	)
}

function Login() {
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
		} catch (e) {
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
							<input name="username" placeholder="Username" className="w-full rounded-lg border px-3 py-2" />
							<input type="password" name="password" placeholder="Password" className="w-full rounded-lg border px-3 py-2" />
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

function Register() {
	const navigate = useNavigate()
	const [loading, setLoading] = useState(false)
	const onSubmit = async (e) => {
		e.preventDefault()
		const formData = new FormData(e.currentTarget)
		const username = formData.get('username')
		const password = formData.get('password')
		setLoading(true)
		try {
			await registerUser({ username, password })
			navigate('/dashboard')
		} catch (e) {
			alert('Registration failed')
		} finally {
			setLoading(false)
		}
	}
	return (
		<Page>
			<div className="pt-28">
				<div className="mx-auto max-w-md px-4">
					<div className="rounded-2xl bg-white/70 dark:bg-slate-900/70 backdrop-blur shadow-xl p-6">
						<h2 className="text-2xl font-bold">Create your account</h2>
						<p className="opacity-70 text-sm">Start your career readiness journey</p>
						<form className="mt-6 space-y-3" onSubmit={onSubmit}>
							<input name="username" placeholder="Username" className="w-full rounded-lg border px-3 py-2" />
							<input type="password" name="password" placeholder="Password" className="w-full rounded-lg border px-3 py-2" />
							<button disabled={loading} className="w-full px-4 py-2 rounded-lg bg-brand-600 hover:bg-brand-700 text-white transition">
								{loading ? 'Creating…' : 'Register'}
							</button>
						</form>
					</div>
				</div>
			</div>
		</Page>
	)
}

function Dashboard() {
	const [me, setMe] = useState(null)
	useState(() => {
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

export default function App() {
	return (
		<BrowserRouter>
			<PageShell>
				<AnimatePresence mode="wait">
					<Routes>
						<Route path="/" element={<Landing />} />
						<Route path="/login" element={<Login />} />
						<Route path="/register" element={<Register />} />
						<Route path="/dashboard" element={<Dashboard />} />
						<Route path="*" element={<Navigate to="/" replace />} />
					</Routes>
				</AnimatePresence>
			</PageShell>
		</BrowserRouter>
	)
}
