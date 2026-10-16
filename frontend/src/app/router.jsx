import { createBrowserRouter } from "react-router-dom";
import { LoginForm } from "../features/auth/LoginForm.jsx";
import { ProtectedRoute } from "../features/auth/ProtectedRoute.jsx";
import { RecoveryForm } from "../features/auth/RecoveryForm.jsx";
import { RegisterForm } from "../features/auth/RegisterForm.jsx";
import { ResetPasswordForm } from "../features/auth/ResetPasswordForm.jsx";
import { HomePage } from "../pages/HomePage.jsx";

export const router = createBrowserRouter([
  { path: "/login", element: <LoginForm /> },
  { path: "/register", element: <RegisterForm /> },
  { path: "/recover", element: <RecoveryForm /> },
  { path: "/reset-password", element: <ResetPasswordForm /> },
  {
    element: <ProtectedRoute />,
    children: [{ path: "/", element: <HomePage /> }],
  },
]);
