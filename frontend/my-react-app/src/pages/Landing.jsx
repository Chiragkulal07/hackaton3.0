import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import Page from '../components/Page'

export default function Landing() {
  return (
    <Page>
      <div className="pt-28">
        <section className="mx-auto max-w-6xl px-4 grid lg:grid-cols-2 gap-10 items-center">
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-5xl font-extrabold leading-tight">
              Unlock Your Career Potential
            </h1>
            <p className="mt-4 text-lg opacity-80">
              Assess your core skills, get personalized feedback, and discover roles where you can thrive.
            </p>
            <div className="mt-6 flex gap-3">
              <Link
                to="/register"
                className="px-5 py-3 rounded-lg bg-brand-600 text-white shadow hover:shadow-lg hover:-translate-y-0.5 transition"
              >
                Get Started
              </Link>
              <Link
                to="/login"
                className="px-5 py-3 rounded-lg border border-brand-600 text-brand-700 dark:text-brand-300 hover:bg-brand-50 dark:hover:bg-slate-800 transition"
              >
                I already have an account
              </Link>
            </div>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="relative"
          >
            <div className="absolute inset-0 bg-gradient-to-tr from-brand-200 to-brand-500 blur-3xl opacity-30 rounded-full -z-10"></div>
            <div className="grid grid-cols-3 gap-4">
              {Array.from({ length: 9 }).map((_, i) => (
                <motion.div
                  key={i}
                  whileHover={{ scale: 1.05 }}
                  className="aspect-square rounded-xl bg-white/80 dark:bg-slate-800/80 shadow flex items-center justify-center text-sm"
                >
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