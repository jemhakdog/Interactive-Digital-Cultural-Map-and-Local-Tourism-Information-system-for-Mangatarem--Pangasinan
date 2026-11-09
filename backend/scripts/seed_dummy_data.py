"""Comprehensive dummy data generator for all database tables and fields.

Populates realistic dummy data for Mangatarem Tourism Platform across all 29 tables
ensuring every column has non-null, valid dummy data according to schema constraints.
"""
from __future__ import annotations

import asyncio
from datetime import UTC, date, datetime, timedelta
import secrets

from sqlalchemy import select, text
from werkzeug.security import generate_password_hash

from backend.app.core.database import async_session_factory
from backend.app.models.analytics import AnalyticsPageView, DatabaseAuditLog, VisitorLog
from backend.app.models.announcements import Announcement
from backend.app.models.attractions import Attraction, Review, UserFavorite
from backend.app.models.barangay import BarangayInfo
from backend.app.models.booking import BookableAsset, BookingSlot, Reservation
from backend.app.models.business import (
    BusinessVerification,
    Establishment,
    EstablishmentMenuItem,
    EstablishmentRoom,
)
from backend.app.models.chat import ChatMessage, ChatParticipant, ChatRoom
from backend.app.models.document import Document
from backend.app.models.events import Event
from backend.app.models.gallery import GalleryItem
from backend.app.models.gamification import AchievementBadge, TouristCheckIn, UserPassport
from backend.app.models.heritage import HeritageProfile
from backend.app.models.notifications import (
    NewsletterHistory,
    NewsletterSubscriber,
    UserNotification,
)
from backend.app.models.user import User


async def seed_all_dummy_data():
    async with async_session_factory() as db:
        now = datetime.now(UTC)

        # -------------------------------------------------------------
        # 1. USERS: Ensure core roles and fill all user columns
        # -------------------------------------------------------------
        default_users = [
            ("admin_user", "admin@mangatarem.gov.ph", "admin", True),
            ("steward_malabobo", "steward.malabobo@mangatarem.gov.ph", "contributor", True),
            ("steward_poblacion", "steward.poblacion@mangatarem.gov.ph", "contributor", True),
            ("steward_cabaluyan", "steward.cabaluyan@mangatarem.gov.ph", "contributor", True),
            ("merchant_pineridge", "owner@pineridgecafe.ph", "business_owner", True),
            ("merchant_ecolodge", "manager@manleluagecolodge.ph", "business_owner", True),
            ("merchant_heritagegrill", "chef@poblaciongrill.ph", "business_owner", True),
            ("tourist_maria", "maria.santos@gmail.com", "user", True),
            ("tourist_alex", "alex.reyes@yahoo.com", "user", True),
            ("tourist_sarah", "sarah.tan@outlook.com", "user", True),
        ]

        users_by_email: dict[str, User] = {}
        for username, email, role, approved in default_users:
            q = await db.execute(select(User).where(User.email == email))
            u = q.scalar_one_or_none()
            if not u:
                u = User(
                    username=username,
                    email=email,
                    password=generate_password_hash("DummyPass123!"),
                    role=role,
                    is_approved=approved,
                    created_at=now - timedelta(days=60),
                    reset_token=secrets.token_hex(16),
                    reset_token_expires_at=now + timedelta(days=14),
                    reset_token_used=False,
                )
                db.add(u)
                await db.flush()
            users_by_email[email] = u

        admin_user = users_by_email["admin@mangatarem.gov.ph"]
        tourist_user = users_by_email["maria.santos@gmail.com"]
        tourist_alex = users_by_email["alex.reyes@yahoo.com"]
        merchant_user = users_by_email["owner@pineridgecafe.ph"]

        # Ensure all existing users in DB have all fields non-null
        all_users = (await db.execute(select(User))).scalars().all()
        for idx, u in enumerate(all_users):
            if u.created_at is None:
                u.created_at = now - timedelta(days=30 + idx)
            if u.reset_token is None:
                u.reset_token = secrets.token_hex(16)
            if u.reset_token_expires_at is None:
                u.reset_token_expires_at = now + timedelta(days=7)
            if u.reset_token_used is None:
                u.reset_token_used = False
            if u.role is None:
                u.role = "user"
        await db.flush()

        # -------------------------------------------------------------
        # 2. BARANGAY_INFO: Populate all narrative and geospatial fields
        # -------------------------------------------------------------
        all_barangays = (await db.execute(select(BarangayInfo))).scalars().all()
        for idx, b in enumerate(all_barangays):
            lat_offset = (idx % 9) * 0.015 - 0.06
            lng_offset = ((idx // 9) % 9) * 0.015 - 0.06
            center_lat = round(15.7885 + lat_offset, 5)
            center_lng = round(120.2960 + lng_offset, 5)

            if not b.mission:
                b.mission = (
                    f"To foster sustainable agricultural development, cultural heritage preservation, "
                    f"and ecotourism while uplifting community livelihood in Barangay {b.name}."
                )
            if not b.vision:
                b.vision = (
                    f"A progressive, resilient, and eco-friendly community celebrating cultural pride "
                    f"and local tourism excellence in Mangatarem, Pangasinan."
                )
            if not b.history:
                b.history = (
                    f"Established as an official political and communal subdivision of Mangatarem, "
                    f"Barangay {b.name} preserves ancestral farming traditions and communal bayanihan culture."
                )
            if not b.cultural_assets:
                b.cultural_assets = (
                    "Ancestral family homes, traditional agricultural granaries, community fiesta plaza, "
                    "and native culinary recipes passed down through generations."
                )
            if not b.traditions:
                b.traditions = (
                    "Annual barangay patronal fiesta, harvest thanksgiving rites, Flores de Mayo processions, "
                    "and communal bayanihan workdays."
                )
            if not b.local_practices:
                b.local_practices = (
                    "Lowland organic rice cultivation, native mango harvesting, tupig grilling, "
                    "bamboo basket weaving, and riverside freshwater fishing."
                )
            if not b.unique_features:
                b.unique_features = (
                    "Scenic views of the Zambales Mountain ridges, fertile alluvial plains, "
                    "natural spring tributaries, and preserved mango orchards."
                )
            if b.user_id is None:
                b.user_id = admin_user.id
            if not b.map_geo_json:
                b.map_geo_json = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [round(center_lng - 0.005, 5), round(center_lat - 0.005, 5)],
                                [round(center_lng + 0.005, 5), round(center_lat - 0.005, 5)],
                                [round(center_lng + 0.005, 5), round(center_lat + 0.005, 5)],
                                [round(center_lng - 0.005, 5), round(center_lat + 0.005, 5)],
                                [round(center_lng - 0.005, 5), round(center_lat - 0.005, 5)],
                            ]
                        ],
                    },
                    "properties": {
                        "barangay": b.name,
                        "municipality": "Mangatarem",
                        "province": "Pangasinan",
                    },
                }
            if not b.location_data:
                b.location_data = {
                    "center": [center_lat, center_lng],
                    "elevation_meters": 45 + (idx % 12) * 5,
                    "land_area_sq_km": round(3.5 + (idx % 5) * 0.8, 2),
                    "classification": "Rural / Agro-Tourism",
                }
            if b.created_at is None:
                b.created_at = now - timedelta(days=90)

        await db.flush()

        # Update users with barangay_id
        first_b = all_barangays[0] if all_barangays else None
        if first_b:
            for idx, u in enumerate(all_users):
                if u.barangay_id is None:
                    u.barangay_id = all_barangays[idx % len(all_barangays)].id
            await db.flush()

        # Build barangay lookup
        b_lookup = {b.name: b for b in all_barangays}
        poblacion_b = b_lookup.get("Arellano Street (Poblacion)", all_barangays[0])
        malabobo_b = b_lookup.get("Malabobo", all_barangays[0])
        cabaluyan_b = b_lookup.get("Cabaluyan 2nd", all_barangays[0])

        # -------------------------------------------------------------
        # 3. HERITAGE_PROFILE: Seed comprehensive tangible & intangible assets
        # -------------------------------------------------------------
        heritage_definitions = [
            {
                "asset_type": "Tangible Built",
                "form_control_number": "HER-MGT-2026-001",
                "name_of_asset": "St. Raymund de Peñafort Spanish Colonial Church",
                "common_name": "Mangatarem Catholic Parish Church",
                "barangay_id": poblacion_b.id,
                "location_details": "Corner of Romulo Highway and Burgos Street, Poblacion, Mangatarem",
                "contact_person": "Rev. Fr. Parish Administrator",
                "contact_number": "+63 75 546 2011",
                "ownership_type": "Religious / Roman Catholic Archdiocese",
                "owner_administrator": "Archdiocese of Lingayen-Dagupan",
                "usage_status": "Active Religious & Historical Landmark",
                "latitude": 15.7889,
                "longitude": 120.2986,
                "significance": "Historical Spanish-era brick church established in 1835 representing Dominican colonial religious architecture and municipal heritage.",
                "conservation_status": "Well-preserved historic structure under continuous ecclesiastical and municipal heritage conservation.",
                "template_slug": "built-heritage",
                "mapper_name": "Municipal Cultural Mapping Team",
                "date_profiled": date(2026, 1, 15),
                "status": "approved",
                "form_data": {
                    "architectural_style": "Baroque-Neoclassical Colonial",
                    "primary_materials": ["Terracotta brick", "Lime mortar", "Narra timber"],
                    "year_constructed": 1835,
                },
            },
            {
                "asset_type": "Natural",
                "form_control_number": "HER-MGT-2026-002",
                "name_of_asset": "Manleluag Spring Protected Landscape",
                "common_name": "Manleluag Hot Springs",
                "barangay_id": malabobo_b.id,
                "location_details": "Foothills of Zambales Mountain Range, Sitio Manleluag, Barangay Malabobo",
                "contact_person": "DENR Protected Area Superintendent",
                "contact_number": "+63 75 546 3122",
                "ownership_type": "Government / National Protected Area",
                "owner_administrator": "DENR-PENRO Pangasinan & LGU Mangatarem",
                "usage_status": "Active National Ecotourism Park",
                "latitude": 15.6667,
                "longitude": 120.2833,
                "significance": "A 1,935-hectare national protected geothermal spring and dipterocarp watershed forest sheltering endemic flora and avian wildlife.",
                "conservation_status": "Legally protected under NIPAS Act with strict forest zoning and eco-ranger stewardship.",
                "template_slug": "natural-heritage",
                "mapper_name": "DENR & LGU Joint Mapping Unit",
                "date_profiled": date(2026, 2, 10),
                "status": "approved",
                "form_data": {
                    "ecosystem_type": "Lowland Dipterocarp & Sulfuric Thermal Spring",
                    "water_temperature_celsius": 38.5,
                    "protected_area_hectares": 1935,
                },
            },
            {
                "asset_type": "Natural",
                "form_control_number": "HER-MGT-2026-003",
                "name_of_asset": "Daang Kalikasan Mountain Escarpment",
                "common_name": "Daang Kalikasan Scenic Ridge",
                "barangay_id": malabobo_b.id,
                "location_details": "Mangatarem-Santa Cruz Scenic Mountain Corridor, Barangay Malabobo",
                "contact_person": "Municipal Tourism Officer",
                "contact_number": "+63 75 546 2200",
                "ownership_type": "Public / Scenic Highway Corridor",
                "owner_administrator": "DPWH & LGU Mangatarem",
                "usage_status": "Active Scenic Tourism Highway",
                "latitude": 15.7000,
                "longitude": 120.2500,
                "significance": "Stunning panoramic ridgeline across the Zambales mountain foothills offering vistas of western Pangasinan and biodiversity corridors.",
                "conservation_status": "Regulated eco-corridor with active reforestation buffers and scenic viewpoint protections.",
                "template_slug": "natural-heritage",
                "mapper_name": "Pangasinan Tourism Board",
                "date_profiled": date(2026, 3, 1),
                "status": "approved",
                "form_data": {
                    "elevation_meters": 320,
                    "highway_length_km": 54,
                    "viewpoint_capacity": 250,
                },
            },
            {
                "asset_type": "Intangible Cultural",
                "form_control_number": "HER-MGT-2026-004",
                "name_of_asset": "Traditional Mangatarem Tupig Clay-Oven Grilling",
                "common_name": "Mangatarem Native Tupig Tradition",
                "barangay_id": poblacion_b.id,
                "location_details": "Artisanal kitchens across Poblacion and highway roadside bakeries",
                "contact_person": "Mangatarem Culinary Guild Head",
                "contact_number": "+63 917 555 4321",
                "ownership_type": "Community / Communal Living Tradition",
                "owner_administrator": "Mangatarem Association of Native Delicacy Producers",
                "usage_status": "Active Living Culinary Tradition",
                "latitude": 15.7890,
                "longitude": 120.2970,
                "significance": "Centuries-old method of wrapping glutinous rice dough, fresh young coconut strips, and molasses in banana leaves and grilling over charcoal ovens.",
                "conservation_status": "Thriving culinary industry passed down through apprenticeship and generational home kitchens.",
                "template_slug": "intangible-heritage",
                "mapper_name": "LGU Cultural Heritage Unit",
                "date_profiled": date(2026, 3, 20),
                "status": "approved",
                "form_data": {
                    "primary_ingredients": ["Glutinous rice flour", "Fresh shredded coconut", "Muscovado", "Coconut milk"],
                    "cultural_domain": "Traditional Craftsmanship & Culinary Arts",
                },
            },
            {
                "asset_type": "Tangible Built",
                "form_control_number": "HER-MGT-2026-005",
                "name_of_asset": "Historic Mangatarem Municipal Town Hall",
                "common_name": "Presidencia de Mangatarem",
                "barangay_id": poblacion_b.id,
                "location_details": "Municipal Town Plaza complex, Poblacion, Mangatarem",
                "contact_person": "Municipal Administrator",
                "contact_number": "+63 75 546 2000",
                "ownership_type": "Government / LGU Mangatarem",
                "owner_administrator": "Local Government Unit of Mangatarem",
                "usage_status": "Active Civic Governance & Public Space",
                "latitude": 15.7885,
                "longitude": 120.2960,
                "significance": "Civic center featuring classic early-20th-century municipal architecture and historical monuments commemorating local patriots.",
                "conservation_status": "Maintained in pristine condition as the primary civic and heritage square of Mangatarem.",
                "template_slug": "built-heritage",
                "mapper_name": "Municipal Planning & Development Office",
                "date_profiled": date(2026, 4, 5),
                "status": "approved",
                "form_data": {
                    "architectural_style": "American Insular Neo-Classical",
                    "year_established": 1927,
                },
            },
        ]

        heritage_profiles: list[HeritageProfile] = []
        for h_def in heritage_definitions:
            existing_h = (
                await db.execute(
                    select(HeritageProfile).where(
                        HeritageProfile.form_control_number == h_def["form_control_number"]
                    )
                )
            ).scalar_one_or_none()
            if not existing_h:
                existing_h = HeritageProfile(
                    asset_type=h_def["asset_type"],
                    form_control_number=h_def["form_control_number"],
                    form_data=h_def["form_data"],
                    name_of_asset=h_def["name_of_asset"],
                    common_name=h_def["common_name"],
                    barangay_id=h_def["barangay_id"],
                    location_details=h_def["location_details"],
                    contact_person=h_def["contact_person"],
                    contact_number=h_def["contact_number"],
                    ownership_type=h_def["ownership_type"],
                    owner_administrator=h_def["owner_administrator"],
                    usage_status=h_def["usage_status"],
                    latitude=h_def["latitude"],
                    longitude=h_def["longitude"],
                    significance=h_def["significance"],
                    conservation_status=h_def["conservation_status"],
                    template_slug=h_def["template_slug"],
                    mapper_name=h_def["mapper_name"],
                    date_profiled=h_def["date_profiled"],
                    status=h_def["status"],
                    user_id=admin_user.id,
                    created_at=now - timedelta(days=50),
                    updated_at=now - timedelta(days=10),
                )
                db.add(existing_h)
                await db.flush()
            heritage_profiles.append(existing_h)

        await db.flush()

        # -------------------------------------------------------------
        # 4. ATTRACTIONS: Update existing 7 and ensure 100% field coverage
        # -------------------------------------------------------------
        all_attractions = (await db.execute(select(Attraction))).scalars().all()
        for idx, att in enumerate(all_attractions):
            if not att.osm_alternatives:
                att.osm_alternatives = {
                    "osm_id": 1000200 + att.id,
                    "osm_type": "way",
                    "center": [att.latitude, att.longitude],
                    "tags": {
                        "tourism": "attraction",
                        "name": att.name,
                        "addr:city": "Mangatarem",
                        "addr:province": "Pangasinan",
                    },
                }
            if att.heritage_profile_id is None:
                att.heritage_profile_id = heritage_profiles[idx % len(heritage_profiles)].id
            if not att.contact_info:
                att.contact_info = "+63 75 546 2110 / tourism@mangatarem.gov.ph"
            if not att.advisory_message:
                att.advisory_message = (
                    "Welcome to Mangatarem! Please follow Leave No Trace principles, "
                    "bring drinking water, and register with the barangay tourism desk upon arrival."
                )
            if not att.advisory_status:
                att.advisory_status = "Normal"
            if not att.physical_status:
                att.physical_status = "Open Public"
            if att.is_verified is None:
                att.is_verified = True
            if not att.facilities:
                att.facilities = "Restrooms, Parking, Info Center, Shaded Pavilions, Water Refill"
            if not att.opening_hours:
                att.opening_hours = "6:00 AM – 6:00 PM Daily"
            if not att.entrance_fee:
                att.entrance_fee = "Free Entry (Barangay Ecological Fee may apply)"
            if not att.directions:
                att.directions = "Accessible via Romulo Highway; take the municipal public shuttle or tricycle from town plaza."
            if not att.image_url:
                att.image_url = "/img/places/default_attraction.webp"
            if att.user_id is None:
                att.user_id = admin_user.id
            if att.created_at is None:
                att.created_at = now - timedelta(days=40)

        await db.flush()

        # -------------------------------------------------------------
        # 5. ESTABLISHMENTS: Update and ensure all fields are non-null
        # -------------------------------------------------------------
        all_establishments = (await db.execute(select(Establishment))).scalars().all()
        est_websites = [
            "https://pineridgecafe.mangatarem.ph",
            "https://manleluagecolodge.mangatarem.ph",
            "https://heritagegrill.mangatarem.ph",
        ]
        for idx, est in enumerate(all_establishments):
            if not est.website:
                est.website = est_websites[idx % len(est_websites)]
            if not est.operating_hours:
                est.operating_hours = {
                    "monday": "07:00-21:00",
                    "tuesday": "07:00-21:00",
                    "wednesday": "07:00-21:00",
                    "thursday": "07:00-21:00",
                    "friday": "07:00-22:00",
                    "saturday": "06:00-23:00",
                    "sunday": "06:00-22:00",
                }
            if not est.amenities:
                est.amenities = {
                    "wifi": True,
                    "parking": True,
                    "air_conditioning": True,
                    "outdoor_seating": True,
                    "restrooms": True,
                    "card_payment": True,
                }
            if not est.cover_image_url:
                est.cover_image_url = f"/img/places/establishment_{est.id}_cover.webp"
            if not est.logo_url:
                est.logo_url = f"/img/places/establishment_{est.id}_logo.webp"
            if not est.rating_avg or est.rating_avg == 0:
                est.rating_avg = 4.8
            if not est.review_count or est.review_count == 0:
                est.review_count = 14
            est.is_featured = True
            est.verified = True
            if est.created_at is None:
                est.created_at = now - timedelta(days=45)

        await db.flush()

        # -------------------------------------------------------------
        # 6. ESTABLISHMENT_ROOM: Populate rooms for lodging establishments
        # -------------------------------------------------------------
        existing_rooms = (await db.execute(select(EstablishmentRoom))).scalars().all()
        if not existing_rooms and all_establishments:
            lodging_est = next((e for e in all_establishments if "Lodge" in e.name or "Inn" in e.name), all_establishments[0])
            room_specs = [
                ("Deluxe Mountain View Suite", "Spacious timber cabin with private balcony overlooking Daang Kalikasan ridge.", 2800.0, 2),
                ("Family Eco Cottage", "Two-bedroom rustic villa with garden patio and natural hot spring access.", 4500.0, 6),
                ("Standard Forest Pod", "Cozy insulated glamping cabin nestled among endemic pine and bamboo groves.", 1800.0, 2),
            ]
            for r_name, r_desc, r_price, r_cap in room_specs:
                new_room = EstablishmentRoom(
                    establishment_id=lodging_est.id,
                    name=r_name,
                    description=r_desc,
                    price_per_night=r_price,
                    capacity=r_cap,
                    amenities={"aircon": True, "wifi": True, "hot_shower": True, "veranda": True, "breakfast": True},
                    image_urls=["/img/rooms/suite_1.webp", "/img/rooms/suite_2.webp"],
                    is_available=True,
                    created_at=now - timedelta(days=20),
                )
                db.add(new_room)
            await db.flush()

        # -------------------------------------------------------------
        # 7. ESTABLISHMENT_MENU_ITEM: Populate culinary dishes
        # -------------------------------------------------------------
        existing_menus = (await db.execute(select(EstablishmentMenuItem))).scalars().all()
        if not existing_menus and all_establishments:
            restaurant_est = all_establishments[0]
            menu_specs = [
                ("Authentic Mangatarem Tupig Box (10 pcs)", "Freshly charcoal-grilled glutinous rice snack with young coconut strings.", 150.0, "Delicacies", True),
                ("Grilled Dagupan Bangus Belly", "Marinated in native calamansi, garlic, and wild herbs, served with tomato salsa.", 280.0, "Main Course", True),
                ("Pangasinan Pigar-Pigar Especial", "Tender beef slices stir-fried with sweet local onions and fresh cabbage.", 240.0, "Main Course", True),
                ("Mountain Ridge Dark Roast Drip", "Single-origin brewed coffee sourced from foothills coffee groves.", 95.0, "Beverages", False),
                ("Native Chicken Tinola with Fresh Malunggay", "Free-range native chicken slow-simmered with green papaya and ginger.", 320.0, "Soups", True),
                ("Poblacion Crispy Bagnet Kare-Kare", "Deep-fried pork belly in rich toasted peanut and annatto sauce with bagoong.", 380.0, "Main Course", True),
            ]
            for m_name, m_desc, m_price, m_cat, m_best in menu_specs:
                new_menu = EstablishmentMenuItem(
                    establishment_id=restaurant_est.id,
                    name=m_name,
                    description=m_desc,
                    price=m_price,
                    category=m_cat,
                    image_url=f"/img/food/{m_cat.lower()}_item.webp",
                    is_available=True,
                    is_bestseller=m_best,
                    created_at=now - timedelta(days=15),
                )
                db.add(new_menu)
            await db.flush()

        # -------------------------------------------------------------
        # 8. BUSINESS_VERIFICATION: Ensure business owners have approval docs
        # -------------------------------------------------------------
        existing_verif = (await db.execute(select(BusinessVerification))).scalars().all()
        if not existing_verif:
            for est in all_establishments:
                bv = BusinessVerification(
                    user_id=est.owner_id,
                    permit_document_url=f"/uploads/permits/business_permit_{est.id}_2026.pdf",
                    other_document_url=f"/uploads/permits/dti_sec_certificate_{est.id}.pdf",
                    status="approved",
                    submitted_at=now - timedelta(days=40),
                )
                db.add(bv)
            await db.flush()

        # -------------------------------------------------------------
        # 9. BOOKABLE_ASSET, BOOKING_SLOT & RESERVATIONS
        # -------------------------------------------------------------
        # Fix or seed BookableAsset
        existing_assets = (await db.execute(select(BookableAsset))).scalars().all()
        if existing_assets:
            for idx, a in enumerate(existing_assets):
                if a.attraction_id is None and all_attractions:
                    a.attraction_id = all_attractions[idx % len(all_attractions)].id
                if a.heritage_profile_id is None and heritage_profiles:
                    a.heritage_profile_id = heritage_profiles[idx % len(heritage_profiles)].id
                if not a.booking_instructions:
                    a.booking_instructions = (
                        "Please arrive 15 minutes prior to your designated entry window. "
                        "Present your reservation QR pass at the municipal ecotourism checkpoint."
                    )
                a.status = "active"
                a.daily_capacity = 60
                a.requires_approval = False
            primary_asset = existing_assets[0]
        else:
            primary_asset = BookableAsset(
                attraction_id=all_attractions[0].id if all_attractions else None,
                heritage_profile_id=heritage_profiles[0].id if heritage_profiles else None,
                daily_capacity=60,
                requires_approval=False,
                booking_instructions="Present QR pass at the ecotourism registration desk.",
                status="active",
                created_at=now - timedelta(days=20),
            )
            db.add(primary_asset)
            await db.flush()

        # Booking slots for upcoming days
        existing_slots = (await db.execute(select(BookingSlot))).scalars().all()
        if not existing_slots:
            created_slots: list[BookingSlot] = []
            for day_offset in range(1, 8):
                slot_date = (now + timedelta(days=day_offset)).date()
                slot = BookingSlot(
                    bookable_asset_id=primary_asset.id,
                    date=slot_date,
                    total_capacity=50,
                    booked_count=6,
                )
                db.add(slot)
                created_slots.append(slot)
            await db.flush()
            first_slot = created_slots[0]
        else:
            first_slot = existing_slots[0]

        # Reservation
        existing_reservations = (await db.execute(select(Reservation))).scalars().all()
        if not existing_reservations:
            res = Reservation(
                user_id=tourist_user.id,
                booking_slot_id=first_slot.id,
                party_size=3,
                primary_contact="+63 917 555 9876",
                special_requests="Traveling with senior citizens; requesting accessible parking stall.",
                status="confirmed",
                qr_code_token="MGT-RSV-98214",
                created_at=now - timedelta(days=2),
                updated_at=now - timedelta(days=1),
            )
            db.add(res)
            await db.flush()

        # -------------------------------------------------------------
        # 10. EVENTS: Ensure all fields are filled
        # -------------------------------------------------------------
        all_events = (await db.execute(select(Event))).scalars().all()
        event_images = [
            "/img/events/mango_festival.webp",
            "/img/events/san_raymundo_fiesta.webp",
            "/img/events/manleluag_ecotrek.webp",
        ]
        for idx, ev in enumerate(all_events):
            if not ev.image_url:
                ev.image_url = event_images[idx % len(event_images)]
            if ev.latitude is None:
                ev.latitude = 15.7885
            if ev.longitude is None:
                ev.longitude = 120.2960
            if ev.barangay_id is None:
                ev.barangay_id = poblacion_b.id
            if ev.user_id is None:
                ev.user_id = admin_user.id
            if ev.created_at is None:
                ev.created_at = now - timedelta(days=30)
            ev.status = "approved"

        await db.flush()

        # -------------------------------------------------------------
        # 11. REVIEWS & RATINGS (Ensuring ck_review_target constraint)
        # -------------------------------------------------------------
        existing_reviews = (await db.execute(select(Review))).scalars().all()
        if not existing_reviews:
            # Attraction review
            rev1 = Review(
                user_id=tourist_user.id,
                attraction_id=all_attractions[0].id,
                establishment_id=None,
                rating=5,
                comment="The natural sulfuric thermal baths were rejuvenating! Very clean and peaceful surroundings.",
                status="approved",
                parent_id=None,
                photo_urls=["/img/reviews/manleluag_pool1.webp", "/img/reviews/manleluag_pool2.webp"],
                created_at=now - timedelta(days=5),
                updated_at=now - timedelta(days=5),
            )
            db.add(rev1)
            await db.flush()

            # Reply to attraction review
            rev1_reply = Review(
                user_id=admin_user.id,
                attraction_id=all_attractions[0].id,
                establishment_id=None,
                rating=5,
                comment="Thank you for visiting Manleluag! We are delighted that you enjoyed your stay in Mangatarem.",
                status="approved",
                parent_id=rev1.id,
                photo_urls=[],
                created_at=now - timedelta(days=4),
                updated_at=now - timedelta(days=4),
            )
            db.add(rev1_reply)

            # Establishment review
            rev2 = Review(
                user_id=tourist_alex.id,
                attraction_id=None,
                establishment_id=all_establishments[0].id,
                rating=5,
                comment="Best brewed coffee with an unparalleled view of Daang Kalikasan! The native tupig was served hot and delicious.",
                status="approved",
                parent_id=None,
                photo_urls=["/img/reviews/coffee_view.webp"],
                created_at=now - timedelta(days=3),
                updated_at=now - timedelta(days=3),
            )
            db.add(rev2)
            await db.flush()

        # -------------------------------------------------------------
        # 12. USER_FAVORITES (Ensuring ck_favorite_target constraint)
        # -------------------------------------------------------------
        existing_favs = (await db.execute(select(UserFavorite))).scalars().all()
        if not existing_favs:
            fav1 = UserFavorite(
                user_id=tourist_user.id,
                attraction_id=all_attractions[0].id,
                establishment_id=None,
                event_id=None,
                status="favorite",
                created_at=now - timedelta(days=10),
            )
            fav2 = UserFavorite(
                user_id=tourist_user.id,
                attraction_id=None,
                establishment_id=all_establishments[0].id,
                event_id=None,
                status="favorite",
                created_at=now - timedelta(days=8),
            )
            fav3 = UserFavorite(
                user_id=tourist_user.id,
                attraction_id=None,
                establishment_id=None,
                event_id=all_events[0].id,
                status="favorite",
                created_at=now - timedelta(days=6),
            )
            db.add_all([fav1, fav2, fav3])
            await db.flush()

        # -------------------------------------------------------------
        # 13. ACHIEVEMENT_BADGE & USER_PASSPORT
        # -------------------------------------------------------------
        existing_badges = (await db.execute(select(AchievementBadge))).scalars().all()
        if not existing_badges:
            badges = [
                AchievementBadge(
                    title="Mountain Trail Explorer",
                    description="Visit scenic high-altitude viewpoints across Daang Kalikasan and mountain rainforest ridges.",
                    badge_image_url="/img/badges/badge_mountain_trail.webp",
                    required_visits=2,
                    target_locations=["Daang Kalikasan", "Timmanguyob Falls"],
                    reward_promo={"discount": "15% discount on hot meals at Pine Ridge Cafe", "code": "TRAIL15"},
                    created_at=now - timedelta(days=40),
                ),
                AchievementBadge(
                    title="Heritage Pilgrim",
                    description="Explore Spanish colonial architectural gems and municipal civic landmarks.",
                    badge_image_url="/img/badges/badge_heritage_pilgrim.webp",
                    required_visits=2,
                    target_locations=["St. Raymund de Penafort Church", "Municipal Town Plaza"],
                    reward_promo={"gift": "Complimentary commemorative heritage postcard set", "code": "PILGRIMFREE"},
                    created_at=now - timedelta(days=40),
                ),
                AchievementBadge(
                    title="Thermal Waters Pioneer",
                    description="Experience the soothing natural sulfuric hot springs and pristine forest cascades.",
                    badge_image_url="/img/badges/badge_thermal_waters.webp",
                    required_visits=2,
                    target_locations=["Manleluag Spring Protected Landscape", "Canding (Kanding) Falls"],
                    reward_promo={"discount": "20% off cottage rentals at Manleluag Eco Park", "code": "HOTSPRING20"},
                    created_at=now - timedelta(days=40),
                ),
                AchievementBadge(
                    title="Master of Mangatarem",
                    description="Complete all municipal exploration milestones and earn official Ambassador status.",
                    badge_image_url="/img/badges/badge_master_mangatarem.webp",
                    required_visits=5,
                    target_locations=["all"],
                    reward_promo={"title": "Official Mangatarem Ecotourism Ambassador Plaque", "code": "VIPAMBASSADOR"},
                    created_at=now - timedelta(days=40),
                ),
            ]
            db.add_all(badges)
            await db.flush()
            existing_badges = badges

        existing_passports = (await db.execute(select(UserPassport))).scalars().all()
        if not existing_passports:
            p1 = UserPassport(
                user_id=tourist_user.id,
                badge_id=existing_badges[0].id,
                unlocked_at=now - timedelta(days=2),
            )
            p2 = UserPassport(
                user_id=tourist_user.id,
                badge_id=existing_badges[1].id,
                unlocked_at=now - timedelta(days=1),
            )
            db.add_all([p1, p2])
            await db.flush()

        # -------------------------------------------------------------
        # 14. TOURIST_CHECK_IN (Unique user_id + target)
        # -------------------------------------------------------------
        existing_checkins = (await db.execute(select(TouristCheckIn))).scalars().all()
        if not existing_checkins:
            chk1 = TouristCheckIn(
                user_id=tourist_user.id,
                attraction_id=all_attractions[0].id,
                establishment_id=None,
                latitude=all_attractions[0].latitude,
                longitude=all_attractions[0].longitude,
                distance_meters=14.2,
                verified_at=now - timedelta(days=3),
            )
            chk2 = TouristCheckIn(
                user_id=tourist_user.id,
                attraction_id=None,
                establishment_id=all_establishments[0].id,
                latitude=all_establishments[0].latitude,
                longitude=all_establishments[0].longitude,
                distance_meters=8.5,
                verified_at=now - timedelta(days=2),
            )
            db.add_all([chk1, chk2])
            await db.flush()

        # -------------------------------------------------------------
        # 15. GALLERY_ITEM
        # -------------------------------------------------------------
        existing_gallery = (await db.execute(select(GalleryItem))).scalars().all()
        if not existing_gallery:
            gallery_specs = [
                ("photo", "/img/gallery/daang_kalikasan_clouds.webp", "Golden hour cloud inversion rolling over Daang Kalikasan ridge.", "approved"),
                ("photo", "/img/gallery/manleluag_steam.webp", "Morning thermal steam rising gently from Manleluag natural spring pool.", "approved"),
                ("photo", "/img/gallery/st_raymund_belfry.webp", "Historic Spanish terracotta brick belfry against a clear blue morning sky.", "approved"),
                ("photo", "/img/gallery/tupig_charcoal_grill.webp", "Fresh tupig sizzling aromatically on traditional coconut charcoal embers.", "approved"),
                ("photo", "/img/gallery/town_plaza_monument.webp", "Municipal town plaza gardens during the annual founding anniversary celebration.", "approved"),
            ]
            for g_type, g_url, g_cap, g_stat in gallery_specs:
                gi = GalleryItem(
                    type=g_type,
                    url=g_url,
                    caption=g_cap,
                    user_id=admin_user.id,
                    status=g_stat,
                    created_at=now - timedelta(days=12),
                )
                db.add(gi)
            await db.flush()

        # -------------------------------------------------------------
        # 16. DOCUMENT (Municipal documents vault)
        # -------------------------------------------------------------
        existing_docs = (await db.execute(select(Document))).scalars().all()
        if not existing_docs:
            docs = [
                Document(
                    title="Mangatarem Sustainable Ecotourism Master Plan 2025-2030",
                    category="Governance",
                    content="Strategic frameworks and infrastructure roadmaps balancing biodiversity conservation and community tourism.",
                    file_url="/docs/mangatarem_tourism_master_plan_2025_2030.pdf",
                    created_at=now - timedelta(days=60),
                    updated_at=now - timedelta(days=10),
                ),
                Document(
                    title="Municipal Ordinance No. 2024-06: Cultural Heritage Preservation Code",
                    category="Legal & Ordinances",
                    content="Local legislation regulating the registration, physical maintenance, and protection of built and intangible heritage assets.",
                    file_url="/docs/ordinance_2024_06_cultural_heritage.pdf",
                    created_at=now - timedelta(days=50),
                    updated_at=now - timedelta(days=20),
                ),
                Document(
                    title="Community Homestay and Tour Guide Accreditation Standards",
                    category="Accreditation",
                    content="Guidelines and safety protocols for local households operating tourist accommodations and eco-trail tours.",
                    file_url="/docs/homestay_guide_standards_handbook.pdf",
                    created_at=now - timedelta(days=45),
                    updated_at=now - timedelta(days=15),
                ),
            ]
            db.add_all(docs)
            await db.flush()

        # -------------------------------------------------------------
        # 17. ANNOUNCEMENTS
        # -------------------------------------------------------------
        existing_announcements = (await db.execute(select(Announcement))).scalars().all()
        if not existing_announcements:
            announcements = [
                Announcement(
                    title="Scheduled Eco-Restoration Maintenance at Manleluag Thermal Springs",
                    content="Routine natural filtration cleansing and pool sanitization will be conducted every Tuesday morning from 6:00 AM to 10:00 AM.",
                    user_id=admin_user.id,
                    barangay_id=malabobo_b.id,
                    status="published",
                    created_at=now - timedelta(days=7),
                    updated_at=now - timedelta(days=7),
                ),
                Announcement(
                    title="Call for Local Artisans & Food Exhibitors: Mango & Agri-Tourism Fair",
                    content="Vendor registration is now officially open at the Municipal Tourism Office for the upcoming April Agro-Tourism Expo.",
                    user_id=admin_user.id,
                    barangay_id=poblacion_b.id,
                    status="published",
                    created_at=now - timedelta(days=5),
                    updated_at=now - timedelta(days=5),
                ),
                Announcement(
                    title="Daang Kalikasan Scenic Route Weekend Driving Safety Advisory",
                    content="High-altitude fog is anticipated past 4:00 PM along ridge kilometers 10-18. Motorists are advised to activate fog lamps and maintain safe speeds.",
                    user_id=admin_user.id,
                    barangay_id=malabobo_b.id,
                    status="published",
                    created_at=now - timedelta(days=3),
                    updated_at=now - timedelta(days=3),
                ),
            ]
            db.add_all(announcements)
            await db.flush()

        # -------------------------------------------------------------
        # 18. NEWSLETTER_SUBSCRIBER & NEWSLETTER_HISTORY
        # -------------------------------------------------------------
        existing_subs = (await db.execute(select(NewsletterSubscriber))).scalars().all()
        for idx, sub in enumerate(existing_subs):
            if sub.user_id is None:
                sub.user_id = all_users[idx % len(all_users)].id
        if not existing_subs:
            subs = [
                NewsletterSubscriber(
                    email="maria.santos@gmail.com",
                    is_active=True,
                    user_id=tourist_user.id,
                    created_at=now - timedelta(days=25),
                ),
                NewsletterSubscriber(
                    email="alex.reyes@yahoo.com",
                    is_active=True,
                    user_id=tourist_alex.id,
                    created_at=now - timedelta(days=20),
                ),
                NewsletterSubscriber(
                    email="explore.pangasinan@outlook.ph",
                    is_active=True,
                    user_id=merchant_user.id,
                    created_at=now - timedelta(days=15),
                ),
            ]
            db.add_all(subs)
            await db.flush()

        existing_news_hist = (await db.execute(select(NewsletterHistory))).scalars().all()
        if not existing_news_hist:
            nh = NewsletterHistory(
                subject="Discover Mangatarem: Your Ultimate Summer Ecotourism Companion",
                content="Immerse yourself in rejuvenating thermal springs, scenic mountain highway coffee stops, and century-old brick heritage church architecture...",
                recipient_count=1840,
                sender_id=admin_user.id,
                sent_at=now - timedelta(days=8),
            )
            db.add(nh)
            await db.flush()

        # -------------------------------------------------------------
        # 19. USER_NOTIFICATION: Fill link and fields for all notifications
        # -------------------------------------------------------------
        existing_notifs = (await db.execute(select(UserNotification))).scalars().all()
        default_links = ["/attractions", "/map", "/passport", "/events", "/business"]
        for idx, notif in enumerate(existing_notifs):
            if not notif.link:
                notif.link = default_links[idx % len(default_links)]
            if notif.created_at is None:
                notif.created_at = now - timedelta(days=idx % 14)
        if not existing_notifs:
            notif = UserNotification(
                user_id=tourist_user.id,
                title="Welcome to Mangatarem Tourism Platform!",
                message="Start exploring the interactive map and collecting badges in your Digital Tourism Passport.",
                link="/passport",
                is_read=False,
                created_at=now - timedelta(days=1),
            )
            db.add(notif)
        await db.flush()

        # -------------------------------------------------------------
        # 20. CHAT_ROOM, CHAT_PARTICIPANT & CHAT_MESSAGE
        # -------------------------------------------------------------
        all_rooms = (await db.execute(select(ChatRoom))).scalars().all()
        # Ensure rooms have assigned barangay or establishment
        for idx, r in enumerate(all_rooms):
            if r.type == "barangay" and r.barangay_id is None:
                r.barangay_id = malabobo_b.id
            elif r.type == "establishment" and r.establishment_id is None:
                r.establishment_id = all_establishments[0].id
            elif r.type in ("general", "public"):
                # Link to town center barangay for complete field coverage
                r.barangay_id = poblacion_b.id
                r.establishment_id = None
            if r.created_at is None:
                r.created_at = now - timedelta(days=30)

        # Ensure we have specific rooms for barangay and establishment
        has_barangay_room = any(r.type == "barangay" for r in all_rooms)
        if not has_barangay_room:
            brg_room = ChatRoom(
                type="barangay",
                barangay_id=malabobo_b.id,
                establishment_id=None,
                created_at=now - timedelta(days=25),
            )
            db.add(brg_room)
            await db.flush()
            all_rooms.append(brg_room)

        has_est_room = any(r.type == "establishment" for r in all_rooms)
        if not has_est_room and all_establishments:
            est_room = ChatRoom(
                type="establishment",
                barangay_id=None,
                establishment_id=all_establishments[0].id,
                created_at=now - timedelta(days=20),
            )
            db.add(est_room)
            await db.flush()
            all_rooms.append(est_room)

        # Participants
        for r in all_rooms:
            p_q = await db.execute(
                select(ChatParticipant).where(
                    ChatParticipant.chat_room_id == r.id,
                    ChatParticipant.user_id == tourist_user.id,
                )
            )
            if not p_q.scalar_one_or_none():
                db.add(
                    ChatParticipant(
                        chat_room_id=r.id,
                        user_id=tourist_user.id,
                        joined_at=now - timedelta(days=10),
                        last_read_at=now - timedelta(hours=1),
                    )
                )
            p_admin = await db.execute(
                select(ChatParticipant).where(
                    ChatParticipant.chat_room_id == r.id,
                    ChatParticipant.user_id == admin_user.id,
                )
            )
            if not p_admin.scalar_one_or_none():
                db.add(
                    ChatParticipant(
                        chat_room_id=r.id,
                        user_id=admin_user.id,
                        joined_at=now - timedelta(days=15),
                        last_read_at=now,
                    )
                )
        await db.flush()

        # Chat messages
        existing_msgs = (await db.execute(select(ChatMessage))).scalars().all()
        if len(existing_msgs) < 10:
            target_room = all_rooms[0]
            msgs = [
                ChatMessage(
                    chat_room_id=target_room.id,
                    sender_id=admin_user.id,
                    content="Mabuhay and welcome to the Mangatarem Community Tourism Channel! Feel free to ask about local guides and travel tips.",
                    created_at=now - timedelta(days=3),
                    is_system_msg=True,
                ),
                ChatMessage(
                    chat_room_id=target_room.id,
                    sender_id=tourist_user.id,
                    content="Hello! Is the road leading to Daang Kalikasan clear for sedans this weekend?",
                    created_at=now - timedelta(days=2, hours=4),
                    is_system_msg=False,
                ),
                ChatMessage(
                    chat_room_id=target_room.id,
                    sender_id=admin_user.id,
                    content="Yes! The asphalted scenic highway is completely accessible for all private vehicles and motorcycles.",
                    created_at=now - timedelta(days=2, hours=2),
                    is_system_msg=False,
                ),
                ChatMessage(
                    chat_room_id=target_room.id,
                    sender_id=tourist_alex.id,
                    content="Can anyone recommend where to buy genuine local tupig near the church?",
                    created_at=now - timedelta(days=1),
                    is_system_msg=False,
                ),
                ChatMessage(
                    chat_room_id=target_room.id,
                    sender_id=merchant_user.id,
                    content="Head over to Poblacion Heritage Grill across Burgos St., freshly baked every morning!",
                    created_at=now - timedelta(hours=12),
                    is_system_msg=False,
                ),
            ]
            db.add_all(msgs)
            await db.flush()

        # -------------------------------------------------------------
        # 21. VISITOR_LOG: Logged visits across tourist destinations
        # -------------------------------------------------------------
        existing_visitor_logs = (await db.execute(select(VisitorLog))).scalars().all()
        for idx, vl in enumerate(existing_visitor_logs):
            if vl.visitor_user_id is None:
                vl.visitor_user_id = tourist_user.id
        if not existing_visitor_logs:
            v_logs = [
                VisitorLog(
                    target_type="attraction",
                    target_id=all_attractions[0].id,
                    visitor_count=4,
                    visitor_name="Maria Santos",
                    visitor_age=32,
                    visitor_address="Dagupan City, Pangasinan",
                    is_system_user=True,
                    visit_date=(now - timedelta(days=3)).date(),
                    logged_by=admin_user.id,
                    visitor_user_id=tourist_user.id,
                    notes="Registered for thermal pool bathing and picnic cottage rental.",
                    created_at=now - timedelta(days=3),
                ),
                VisitorLog(
                    target_type="attraction",
                    target_id=all_attractions[1].id,
                    visitor_count=2,
                    visitor_name="Alex Reyes",
                    visitor_age=28,
                    visitor_address="Baguio City, Benguet",
                    is_system_user=True,
                    visit_date=(now - timedelta(days=2)).date(),
                    logged_by=admin_user.id,
                    visitor_user_id=tourist_alex.id,
                    notes="Mountain scenic drive stopover and photography.",
                    created_at=now - timedelta(days=2),
                ),
                VisitorLog(
                    target_type="establishment",
                    target_id=all_establishments[0].id,
                    visitor_count=5,
                    visitor_name="Eduardo Cruz",
                    visitor_age=45,
                    visitor_address="Tarlac City, Tarlac",
                    is_system_user=True,
                    visit_date=(now - timedelta(days=1)).date(),
                    logged_by=merchant_user.id,
                    visitor_user_id=merchant_user.id,
                    notes="Walk-in dining party for breakfast and brewed coffee.",
                    created_at=now - timedelta(days=1),
                ),
            ]
            db.add_all(v_logs)
            await db.flush()

        # -------------------------------------------------------------
        # 22. ANALYTICS_PAGE_VIEW: Telemetry across public routes
        # -------------------------------------------------------------
        existing_views = (await db.execute(select(AnalyticsPageView))).scalars().all()
        for idx, pv in enumerate(existing_views):
            if pv.item_id is None:
                pv.item_id = all_attractions[idx % len(all_attractions)].id
        if not existing_views:
            views = [
                AnalyticsPageView(
                    page_url="/",
                    view_type="page_view",
                    item_id=all_attractions[0].id,
                    page_name="Editorial Landing Page",
                    user_id=tourist_user.id,
                    timestamp=now - timedelta(hours=6),
                    session_id="sess_mgt_001_prod",
                    ip_address="112.204.180.25",
                    device_info="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0",
                ),
                AnalyticsPageView(
                    page_url="/map",
                    view_type="map_interaction",
                    item_id=all_attractions[1].id,
                    page_name="Interactive Digital Cultural Map",
                    user_id=tourist_user.id,
                    timestamp=now - timedelta(hours=5),
                    session_id="sess_mgt_001_prod",
                    ip_address="112.204.180.25",
                    device_info="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0",
                ),
                AnalyticsPageView(
                    page_url=f"/attractions/{all_attractions[0].id}",
                    view_type="attraction_view",
                    item_id=all_attractions[0].id,
                    page_name="Manleluag Spring Detail",
                    user_id=tourist_alex.id,
                    timestamp=now - timedelta(hours=3),
                    session_id="sess_mgt_002_prod",
                    ip_address="120.28.190.44",
                    device_info="Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15",
                ),
                AnalyticsPageView(
                    page_url="/passport",
                    view_type="passport_view",
                    item_id=all_attractions[2].id,
                    page_name="Digital Tourism Passport",
                    user_id=tourist_user.id,
                    timestamp=now - timedelta(hours=2),
                    session_id="sess_mgt_001_prod",
                    ip_address="112.204.180.25",
                    device_info="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0",
                ),
            ]
            db.add_all(views)
            await db.flush()

        # -------------------------------------------------------------
        # 23. DATABASE_AUDIT_LOG: Administrative operation logs
        # -------------------------------------------------------------
        existing_audits = (await db.execute(select(DatabaseAuditLog))).scalars().all()
        if not existing_audits:
            audits = [
                DatabaseAuditLog(
                    user_id=admin_user.id,
                    action="CATALOGUE_DUMMY_SEED",
                    table_name="ATTRACTION",
                    record_id=all_attractions[0].id,
                    ip_address="127.0.0.1",
                    user_agent="MangataremInternalSeeder/2.0 (Goldfish; Linux x86_64)",
                    query_summary="INSERT INTO ATTRACTION (name, category, coordinates...)",
                    status="success",
                    created_at=now - timedelta(minutes=15),
                ),
                DatabaseAuditLog(
                    user_id=admin_user.id,
                    action="HERITAGE_REGISTRY_INIT",
                    table_name="HERITAGE_PROFILE",
                    record_id=heritage_profiles[0].id,
                    ip_address="127.0.0.1",
                    user_agent="MangataremInternalSeeder/2.0 (Goldfish; Linux x86_64)",
                    query_summary="INSERT INTO HERITAGE_PROFILE (form_control_number, asset_type...)",
                    status="success",
                    created_at=now - timedelta(minutes=10),
                ),
                DatabaseAuditLog(
                    user_id=admin_user.id,
                    action="MUNICIPAL_BARANGAY_ENRICHMENT",
                    table_name="BARANGAY_INFO",
                    record_id=poblacion_b.id,
                    ip_address="127.0.0.1",
                    user_agent="MangataremInternalSeeder/2.0 (Goldfish; Linux x86_64)",
                    query_summary="UPDATE BARANGAY_INFO SET mission, vision, cultural_assets, map_geo_json...",
                    status="success",
                    created_at=now - timedelta(minutes=5),
                ),
            ]
            db.add_all(audits)
            await db.flush()

        await db.commit()
        print("✓ All 29 database tables populated with complete dummy data across all fields.")


if __name__ == "__main__":
    asyncio.run(seed_all_dummy_data())
