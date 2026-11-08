# Mangatarem Cultural Mapping & Tourism Platform — Roadmap & Open Tasks

## Completed in Latest Session (2026-11-08) ✅
- [x] **Municipal Database Seeding**: Author and execute `backend/scripts/seed_initial_data.py` populating all 82 official barangays (`BARANGAY_INFO`), 7 attractions (`ATTRACTION`), 3 partner businesses (`ESTABLISHMENT`), 3 seasonal festivals (`EVENT`), and 1 public chat room (`CHAT_ROOM`).
- [x] **Map Fallback Hardening**: Export `DEFAULT_PLACES` in `frontend/src/components/map/data.ts` and update `frontend/src/app/map/page.tsx` so `/map` displays 7 pins even if the database is cold or unseeded.
- [x] **Public Chat Onboarding**: Updated `backend/app/api/chat.py` to allow discovery and messaging in public rooms (`type in ("public", "general", "barangay")`). Fixed trailing slash handling in `frontend/src/app/chat/` and connected clickable room cards.
- [x] **Admin Dashboard KPI Alignment**: Fixed payload response key mapping in `frontend/src/app/admin/page.tsx` (`attractions`, `events`, `establishments` instead of `.items`), showing accurate municipal counts.
- [x] **Merchant Peer Discovery**: Verified `/business/peers` rendering approved local peer networks.
- [x] **Form Accessibility Fix**: Added `id="newsletter-email"` and `name="email"` attributes to `frontend/src/components/public/newsletter-subscribe.tsx`, clearing DevTools form warnings.

---

## Open Tasks & Future Roadmap 📋

### 1. Production Database Deployment & Seeding
- [ ] Run `python -m backend.scripts.seed_initial_data` on production PostgreSQL/Supabase instance to bootstrap the 82 barangays and core catalogue.
- [ ] Add an automated initial migration/seed check on container boot if `BARANGAY_INFO` count is 0.

### 2. Live Device & Sensor Verification
- [ ] Test mobile responsive touch navigation, map gestures (pinch-to-zoom, compass bearing rotation), and PWA install prompt on iOS Safari and Android Chrome.
- [ ] Verify HTML5 Geolocation API (`Locate Me` button) under HTTPS with user permission prompts on real mobile devices.

### 3. Production Auth & Social Login
- [ ] Configure live production `NEXT_PUBLIC_GOOGLE_CLIENT_ID` in `.env.production` and verify OAuth redirect whitelist on Google Cloud Console.
- [ ] Test password reset email delivery with a real SMTP / transactional email provider (Resend, SendGrid, or AWS SES).

### 4. Digital Passport & QR Physical Field Testing
- [ ] Generate print-ready vector QR codes containing checkpoint URLs/tokens for each of the 7 seeded attractions.
- [ ] Test camera scanner flow on `/passport/scan` under physical lighting conditions.

### 5. Barangay Steward Expansion
- [ ] Create specialized channels for high-density tourism barangays (e.g. *Malabobo Eco-Desk*, *Poblacion Heritage Desk*) in `backend/app/api/chat.py`.
- [ ] Add steward onboarding guidance and verification review checklist in the `/contributor` console.
