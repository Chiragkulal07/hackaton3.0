import Nav from './nav'

export default function PageShell({ children }) {
  return (
    <div className="min-h-screen">
      <Nav />
      {children}
    </div>
  )
}