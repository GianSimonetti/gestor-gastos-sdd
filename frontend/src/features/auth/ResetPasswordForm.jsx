import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { authApi } from "./api.js";

export function ResetPasswordForm() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const token = params.get("token") || "";
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      await authApi.reset(token, password);
      navigate("/login", { replace: true, state: { passwordReset: true } });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (!token) {
    return <section className="auth-card"><h1>Enlace inválido</h1><Link to="/recover">Solicitar uno nuevo</Link></section>;
  }

  return (
    <form className="auth-card" onSubmit={submit}>
      <h1>Definir contraseña nueva</h1>
      {error && <p className="form-error" role="alert">{error}</p>}
      <label htmlFor="new-password">Contraseña nueva</label>
      <input id="new-password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} minLength="8" required />
      <button type="submit" disabled={submitting}>{submitting ? "Guardando…" : "Guardar contraseña"}</button>
    </form>
  );
}
