# Component Package: Next.js App Router (`src/app`)

## Overview
Defines page routing, SSR/SSG boundaries, global styles, and layout templates for the Mangatarem tourism web portal.

## Interface
- Root Layout & Metadata: `RootLayout({ children })`, `metadata`
- Public Pages: `/` (Home), `/map` (Interactive Map), `/attractions`, `/events`, `/heritage`, `/business`
- Back-office Portals: `/admin/*` (Attractions, Events, Establishments, Bookings, Reviews, Analytics), `/contributor/*`
- Auth Routes: `/auth/*` (`login`, `register`, `forgot-password`, `reset-password`, `select-role`)

## Invariants
- Server-side data fetching for home featured attractions revalidates every 60 seconds.
- Theme resolution script executes before hydration to avoid theme flashing.
- Admin and business owners route to dedicated dashboards based on user role.

## Side Effects
- Direct fetch calls to `/api/` on page load.
- Next.js client-side navigation and history URL search parameter synchronization.

## Verification
- Run: `cd frontend && npm run build`
