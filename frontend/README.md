# Frontend Blueprint: Mangatarem Tourism Portal

## Overview
Next.js 16+ App Router web application serving as the primary public exploration portal and administrative console for the Mangatarem Cultural Map and Local Tourism Information System.

## Subdirectories & Boundaries
- [`src/app`](./src/app/README.md): Next.js App Router layouts, routes, and metadata.
- [`src/components`](./src/components/README.md): MapLibre GL mapping container, navigation layout, and UI design primitives.
- [`src/lib`](./src/lib/README.md): Client-side API client, auth context provider, and utility helpers.

## Invariants
- Client communicates with FastAPI backend at `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`).
- Static and curated fallbacks allow essential map exploration even when the backend is unseeded or cold.

## Verification
- Run: `cd frontend && npm run build`

---

## Developer Notes (Preserved)

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

### Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

### Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

### Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
