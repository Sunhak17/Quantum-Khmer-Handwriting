import { NavLink } from 'react-router-dom'

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `text-sm font-medium ${isActive ? 'text-red-600' : 'text-slate-500 hover:text-slate-800'}`

export default function NavBar() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="flex items-center justify-between px-8 py-5">
        <h1 className="text-xl font-bold text-slate-900">Khmer Handwriting Recognition</h1>
        <nav className="flex gap-6">
          <NavLink to="/" end className={linkClass}>
            Predict
          </NavLink>
          <NavLink to="/history" className={linkClass}>
            History
          </NavLink>
        </nav>
      </div>
    </header>
  )
}
