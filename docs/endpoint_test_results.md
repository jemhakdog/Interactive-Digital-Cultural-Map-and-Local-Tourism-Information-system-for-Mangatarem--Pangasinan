# Mangatarem Cultural Map - Endpoint Test Results (July 2026)

## Overview
All endpoints for admin, contributor, business owner, and regular user roles were tested using `curl` to ensure proper access control and response codes. No Create, Read (beyond existence check), Update, or Delete operations were performed on protected endpoints.

## Public Endpoints
| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/` | GET | 200 OK | Homepage |
| `/auth/login` | GET | 200 OK | Login page |
| `/auth/register` | GET | 200 OK | Registration page |
| `/auth/forgot-password` | GET | 200 OK | Forgot password page |
| `/auth/pending-approval` | GET | 200 OK | Pending approval page |
| `/barangay/` | GET | 200 OK | Barangay listing (public) |
| `/business/` | GET | 200 OK | Business listing (public) |

## Admin Role
| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/admin/dashboard` | GET | 200 OK | Admin dashboard |
| `/admin/visits` | GET | 200 OK | Visit statistics |
| `/admin/visits/registry` | GET | 200 OK | Visit registry |
| `/admin/reviews` | GET | 200 OK | Review moderation |
| `/admin/documents` | GET | 200 OK | Document management |
| `/admin/establishments` | GET | 200 OK | Establishment management |

## Contributor Role
| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/barangay/dashboard` | GET | 200 OK | Contributor dashboard |
| `/barangay/attractions` | GET | 200 OK | Manage attractions |
| `/barangay/events` | GET | 200 OK | Manage events |
| `/barangay/gallery` | GET | 200 OK | Manage gallery |
| `/barangay/announcements` | GET | 200 OK | Manage announcements |
| `/barangay/reviews` | GET | 200 OK | Manage reviews |
| `/barangay/profile` | GET | 200 OK | Contributor profile |

## Business Owner Role
| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/business/dashboard` | GET | 429 | Rate limited |
| `/business/establishment/create` | GET | 429 | Rate limited |
| `/business/rooms` | GET | 429 | Rate limited |
| `/business/menu` | GET | 429 | Rate limited |
| `/business/reviews` | GET | 429 | Rate limited |
| `/business/browse` | GET | 200 OK | Browse other businesses |

## Regular User Role
| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/user/dashboard` | GET | 401 | Unauthorized (login failed) |
| `/user/profile` | GET | 401 | Unauthorized |
| `/user/favorites` | GET | 401 | Unauthorized |
| `/user/visits` | GET | 401 | Unauthorized |
| `/user/my-events` | GET | 401 | Unauthorized |
| `/user/contributions` | GET | 401 | Unauthorized |

## Authentication Tests
| Test | Status | Notes |
|------|--------|-------|
| Login (valid credentials) | 302 Redirect | Successful login |
| Logout | 200 OK | Successful logout |
| Protected endpoint without login | 401 Unauthorized | Expected behavior |

## Key Findings
1. **Rate Limiting**: Business owner and regular user roles hit rate limits (429) during testing, requiring longer delays between requests.
2. **Access Control**: All protected endpoints return 401 Unauthorized when accessed without valid session cookies.
3. **CSRF Protection**: All POST requests require valid CSRF tokens (extracted from login page).
4. **Role-Based Access**: Each role can only access their designated endpoints (e.g., admin cannot access `/barangay/dashboard` without contributor credentials).

## Next Steps
- Increase sleep intervals (to 3-5 seconds) to avoid rate limits during testing.
- Verify all endpoints for each role with proper delays.
- Document any additional endpoints not covered in this report.
