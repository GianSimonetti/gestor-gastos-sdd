import { useAuth } from "../features/auth/AuthContext.jsx";

export function HomePage() {
  const { account, logout } = useAuth();
  return (
    <main className="home-card">
      <div>
        <p className="eyebrow">Gestor de Gastos</p>
        <h1>Hola, {account.display_name}</h1>
        <p>Tu acceso seguro está listo. Los tableros se incorporarán en el próximo incremento.</p>
      </div>
      <button type="button" className="secondary" onClick={logout}>Cerrar sesión</button>
    </main>
  );
}
