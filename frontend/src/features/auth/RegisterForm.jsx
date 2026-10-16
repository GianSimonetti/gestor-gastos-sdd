import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authApi } from "./api.js";

export function RegisterForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ display_name: "", email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [generalError, setGeneralError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function update(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function submit(event) {
    event.preventDefault();
    setSubmitting(true);
    setErrors({});
    setGeneralError("");
    try {
      await authApi.register(form);
      navigate("/login", { replace: true, state: { registered: true } });
    } catch (error) {
      setErrors(error.fieldErrors || {});
      setGeneralError(error.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="auth-card" onSubmit={submit} noValidate>
      <h1>Crear cuenta</h1>
      {generalError && <p className="form-error" role="alert">{generalError}</p>}
      <label htmlFor="display_name">Nombre visible</label>
      <input id="display_name" name="display_name" value={form.display_name} onChange={update} maxLength="100" required aria-describedby="display_name-error" />
      <FieldError id="display_name-error" errors={errors.display_name} />
      <label htmlFor="email">Email</label>
      <input id="email" name="email" type="email" value={form.email} onChange={update} required aria-describedby="email-error" />
      <FieldError id="email-error" errors={errors.email} />
      <label htmlFor="password">Contraseña</label>
      <input id="password" name="password" type="password" value={form.password} onChange={update} minLength="8" required aria-describedby="password-error" />
      <FieldError id="password-error" errors={errors.password} />
      <button type="submit" disabled={submitting}>{submitting ? "Creando…" : "Crear cuenta"}</button>
      <p>¿Ya tenés cuenta? <Link to="/login">Iniciá sesión</Link></p>
    </form>
  );
}

function FieldError({ id, errors }) {
  return <span id={id} className="field-error">{errors?.[0] || ""}</span>;
}
