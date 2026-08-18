# Trip Cost Estimator System Plan

## Original Location
`/docs/planning/PLAN-trip-cost.md`

## Status: ❌ NOT IMPLEMENTED

### What Was Planned

A comprehensive trip cost estimator feature that allows tourists to:
1. Select attractions they want to visit
2. See itemized cost breakdowns (entrance, transport, food, accommodation, tour guide, souvenirs)
3. Get a total estimated trip budget

### Database Schema (5 New Models)
- `AttractionCost` - Entrance fees per attraction
- `TransportOption` - Local transport fare estimates
- `FoodOption` - Dining cost estimates
- `AccommodationOption` - Lodging cost estimates
- `MiscCost` - Tour guides, souvenirs, other costs

### Routes Planned
- `GET /trip-cost` - Public trip cost estimator page
- `GET /api/trip-costs` - JSON API for pricing data
- `GET/POST /admin/costs` - Admin cost management dashboard
- `GET/POST /barangay-admin/costs` - Contributor cost management

### Files To Create
- `templates/pagez/trip_cost.html` - Trip Cost Estimator page
- `templates/admin/costs.html` - Admin cost management page
- `templates/barangay/costs.html` - Contributor cost management page

### Files To Modify
- `models.py` - Add 5 new models
- `routes/admin.py` - Add cost CRUD routes
- `routes/barangay.py` - Add contributor cost routes
- `routes/public.py` - Add `/trip-cost` route
- `routes/api.py` - Add `/api/trip-costs` endpoint
- `templates/base.html` - Add navbar link

### Why It's Pending

❌ **No implementation found:**
- No `TripCost`, `AttractionCost`, `TransportOption`, `FoodOption`, `AccommodationOption`, or `MiscCost` models in `models.py`
- No `/trip-cost` route in public routes
- No cost management templates exist
- No admin cost management pages
- Only references are in `scripts/generate_tourism_forms.py` (data collection script)

### Priority
Medium-High (capstone defense feature)

### Estimated Effort
16-22 hours (6 phases)

### Dependencies
- Business portal accommodations (✅ already implemented, can reuse)
- Admin/Contributor workflows (✅ already implemented)

### Next Steps
1. Add 5 new models to `models.py`
2. Create database migration
3. Build admin cost management interface
4. Build contributor cost management (barangay-scoped)
5. Create public trip cost estimator page with JS calculator
6. Add navbar integration
7. Seed sample pricing data
8. Test and verify
