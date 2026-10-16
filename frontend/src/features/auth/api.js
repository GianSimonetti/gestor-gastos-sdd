import { apiRequest } from "../../lib/api.js";

export const authApi = {
  register(payload) {
    return apiRequest("/auth/register", { method: "POST", body: JSON.stringify(payload) });
  },
  login(payload) {
    return apiRequest("/auth/login", { method: "POST", body: JSON.stringify(payload) });
  },
  logout() {
    return apiRequest("/auth/logout", { method: "POST" });
  },
  me() {
    return apiRequest("/auth/me");
  },
  recover(email) {
    return apiRequest("/auth/password-recovery", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
  },
  reset(token, newPassword) {
    return apiRequest("/auth/password-reset", {
      method: "POST",
      body: JSON.stringify({ token, new_password: newPassword }),
    });
  },
};
