import type { ReactNode } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export function AppShell({ children }: { children: ReactNode }) {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    "rounded-md px-3 py-1.5 text-sm font-medium transition " +
    (isActive
      ? "bg-indigo-600 text-white"
      : "text-slate-600 hover:bg-slate-200 dark:text-slate-300 dark:hover:bg-slate-800");

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <header className="border-b border-slate-200 bg-white px-6 py-3 dark:border-slate-800 dark:bg-slate-900">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <div className="flex items-center gap-6">
            <h1 className="text-lg font-semibold text-slate-900 dark:text-slate-50">
              SQL Analytics
            </h1>
            <nav className="flex items-center gap-1">
              <NavLink to="/chat" className={linkClass}>
                Chat
              </NavLink>
              <NavLink to="/connect" className={linkClass}>
                Connection
              </NavLink>
            </nav>
          </div>
          <button
            onClick={() => {
              logout();
              navigate("/login", { replace: true });
            }}
            className="text-sm text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100"
          >
            Sign out
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
    </div>
  );
}
