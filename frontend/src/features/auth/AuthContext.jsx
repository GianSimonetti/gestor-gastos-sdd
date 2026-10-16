import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { authApi } from "./api.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [account, setAccount] = useState(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      setAccount(await authApi.me());
    } catch (error) {
      if (error.status !== 401) throw error;
      setAccount(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
    const clearSession = () => setAccount(null);
    window.addEventListener("auth:unauthorized", clearSession);
    return () => window.removeEventListener("auth:unauthorized", clearSession);
  }, [refresh]);

  const login = useCallback(async (credentials) => {
    await authApi.login(credentials);
    const current = await authApi.me();
    setAccount(current);
  }, []);

  const logout = useCallback(async () => {
    try {
      await authApi.logout();
    } finally {
      setAccount(null);
    }
  }, []);

  const value = useMemo(
    () => ({ account, loading, login, logout, refresh }),
    [account, loading, login, logout, refresh],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth debe usarse dentro de AuthProvider");
  return context;
}
