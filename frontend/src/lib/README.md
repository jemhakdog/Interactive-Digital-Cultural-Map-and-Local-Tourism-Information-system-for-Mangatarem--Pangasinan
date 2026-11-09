# Component Package: Client Utilities & API Layer (`src/lib`)

## Overview
Provides client-side authentication management, HTTP communications with the backend REST API, and class merger utilities.

## Interface
- `fetchAPI<T>(path: string, options?: RequestInit): Promise<T>`: Generic HTTP fetch wrapper handling JWT authorization header injection and unified error normalization.
- `authAPI`: Authentication operations (`login`, `register`, `google`, `forgotPassword`, `me`).
- `APIError`: Error class capturing HTTP status codes and API error details.
- `AuthProvider`: React Context provider managing user authentication lifecycle and token sync.
- `useAuth()`: Hook exposing current user state, auth tokens, login, logout, and token refresher.
- `cn(...inputs: ClassValue[])`: Tailwind CSS class name combiner utilizing `clsx` and `tailwind-merge`.

## Invariants
- Tokens stored in `localStorage` keys `access_token` and `refresh_token`.
- `fetchAPI` injects `Authorization: Bearer <token>` when tokens exist.
- HTTP 204 responses return `undefined` without JSON parse errors.

## Side Effects
- Communicates with backend via `NEXT_PUBLIC_API_URL` or defaults to `http://localhost:8000`.
- Reads and mutates browser `localStorage` for token state.

## Verification
- Run: `cd frontend && npm run lint`
