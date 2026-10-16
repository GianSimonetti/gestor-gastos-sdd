export class ApiError extends Error {
  constructor(status, payload) {
    super(payload?.message || "No se pudo completar la operación");
    this.name = "ApiError";
    this.status = status;
    this.code = payload?.code || "request_failed";
    this.fieldErrors = payload?.field_errors || {};
  }
}

export async function apiRequest(path, options = {}) {
  const headers = new Headers(options.headers || {});
  if (options.body && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }
  const response = await fetch(`/api${path}`, {
    ...options,
    headers,
    credentials: "include",
  });

  if (response.status === 204) {
    return null;
  }

  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    if (response.status === 401) {
      window.dispatchEvent(new Event("auth:unauthorized"));
    }
    throw new ApiError(response.status, payload);
  }
  return payload;
}
