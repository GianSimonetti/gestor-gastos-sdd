import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext.jsx";

export function LoginForm() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      await login(form);
      navigate(location.state?.from || "/", { replace: true });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="auth-card" onSubmit={submit}>
      <h1>Iniciar sesión</h1>
      {location.state?.registered && <p className="success" role="status">Cuenta creada. Ya podés ingresar.</p>}
      {error && <p className="form-error" role="alert">{error}</p>}
      <label htmlFor="email">Email</label>
      <input id="email" name="email" type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} required />
      <label htmlFor="password">Contraseña</label>
      <input id="password" name="password" type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} required />
      <button type="submit" disabled={submitting}>{submitting ? "Ingresando…" : "Ingresar"}</button>
      <Link to="/recover">Olvidé mi contraseña</Link>
      <p>¿No tenés cuenta? <Link to="/register">Creá una</Link></p>
    </form>
  );
}
