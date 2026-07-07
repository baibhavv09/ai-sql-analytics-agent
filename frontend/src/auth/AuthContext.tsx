import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from "react";
import { api, clearToken, getToken, setToken } from "../api/client";

type AuthState = {
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (fullName: string, email: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenState] = useState<string | null>(getToken());

  const login = useCallback(async (email: string, password: string) => {
    const { data } = await api.post<{ access_token: string; token_type: string }>(
      "/auth/login",
      { email, password },
    );
    setToken(data.access_token);
    setTokenState(data.access_token);
  }, []);

  const register = useCallback(async (full_name: string, email: string, password: string) => {
    await api.post("/auth/register", { full_name, email, password });
  }, []);

  const logout = useCallback(() => {
    clearToken();
    setTokenState(null);
  }, []);

  const value = useMemo<AuthState>(
    () => ({ token, isAuthenticated: Boolean(token), login, register, logout }),
    [token, login, register, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
