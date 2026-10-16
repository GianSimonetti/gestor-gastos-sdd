import { useState } from "react";
import { Link } from "react-router-dom";
import { authApi } from "./api.js";

export function RecoveryForm() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      const result = await authApi.recover(email);
      setMessage(result.message);
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  return (
    <form className="auth-card" onSubmit={submit}>
      <h1>Recuperar acceso</h1>
      <p>Ingresá tu email y te enviaremos instrucciones si existe una cuenta asociada.</p>
      {message && <p className="success" role="status">{message}</p>}
      {error && <p className="form-error" role="alert">{error}</p>}
      <label htmlFor="recovery-email">Email</label>
      <input id="recovery-email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
      <button type="submit">Enviar instrucciones</button>
      <Link to="/login">Volver al inicio de sesión</Link>
    </form>
  );
}
