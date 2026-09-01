export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class APIError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.name = "APIError";
    this.status = status;
    this.detail = detail;
  }
}

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

/** Generic fetch with Bearer token + unified error handling. */
export async function fetchAPI<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> | undefined),
  };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (body?.detail) {
        detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
      }
    } catch {
      // non-JSON error body — keep generic message
    }
    throw new APIError(res.status, detail);
  }

  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

function body(data: unknown): RequestInit {
  return { method: "POST", body: JSON.stringify(data) };
}

interface TokenResponse {
  access_token: string;
  refresh_token: string;
}

export interface UserProfile {
  id: number;
  email: string;
  name: string;
  role: string;
  is_approved: boolean;
  created_at?: string | null;
}

export const authAPI = {
  login: (email: string, password: string) =>
    fetchAPI<TokenResponse>("/api/auth/login", body({ email, password })),
  register: (data: {
    name: string;
    email: string;
    password: string;
    role?: string;
    barangay?: string;
  }) => fetchAPI<TokenResponse>("/api/auth/register", body(data)),
  google: (credential: string, role?: string) =>
    fetchAPI<TokenResponse>("/api/auth/google", body({ credential, role })),
  forgotPassword: (email: string) =>
    fetchAPI<{ detail: string }>("/api/auth/forgot-password", body({ email })),
  me: () => fetchAPI<UserProfile>("/api/auth/me"),
  refresh: (refresh_token: string) =>
    fetchAPI<TokenResponse>("/api/auth/refresh", body({ refresh_token })),
};

/** Typed helper endpoints for public data. */
export const api = {
  home: () => fetchAPI<Record<string, unknown>>("/api/"),
  attractions: (params?: Record<string, string>) => {
    const qs = params ? `?${new URLSearchParams(params)}` : "";
    return fetchAPI<{ attractions?: unknown[]; items?: unknown[] }>(`/api/attractions${qs}`);
  },
  events: (params?: Record<string, string>) => {
    const qs = params ? `?${new URLSearchParams(params)}` : "";
    return fetchAPI<{ items?: unknown[] }>(`/api/events${qs}`);
  },
  business: (params?: Record<string, string>) => {
    const qs = params ? `?${new URLSearchParams(params)}` : "";
    return fetchAPI<{ businesses?: unknown[]; establishments?: unknown[]; items?: unknown[] }>(
      `/api/business${qs}`
    );
  },
  search: (q: string, params?: Record<string, string>) => {
    const qs = new URLSearchParams({ q, ...params });
    return fetchAPI<Record<string, unknown>>(`/api/search?${qs}`);
  },
  map: (category?: string) => {
    const qs = category ? `?category=${encodeURIComponent(category)}` : "";
    return fetchAPI<{ markers?: unknown[] }>(`/api/map${qs}`);
  },
  heritageTypes: () => fetchAPI<{ types?: unknown[] }>("/api/heritage/types"),
  gallery: (params?: Record<string, string>) => {
    const qs = params ? `?${new URLSearchParams(params)}` : "";
    return fetchAPI<{ items?: unknown[] }>(`/api/gallery${qs}`);
  },
};
