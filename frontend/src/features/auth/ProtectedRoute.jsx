import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "./AuthContext.jsx";

export function ProtectedRoute() {
  const { account, loading } = useAuth();
  const location = useLocation();

  if (loading) return <p role="status">Comprobando sesión…</p>;
  if (!account) return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  return <Outlet />;
}
