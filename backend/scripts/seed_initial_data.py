"""Idempotent initial data seeder for Mangatarem Tourism Platform."""
from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from sqlalchemy import select
from werkzeug.security import generate_password_hash

from backend.app.core.database import async_session_factory
from backend.app.models.attractions import Attraction
from backend.app.models.barangay import BarangayInfo
from backend.app.models.business import Establishment
from backend.app.models.chat import ChatRoom
from backend.app.models.events import Event
from backend.app.models.user import User

MANGATAREM_BARANGAYS = [
    "Andangin",
    "Arellano Street (Poblacion)",
    "Bantay",
    "Bantocaling",
    "Baracbac",
    "Peania Pedania (Bedania)",
    "Bogtong Bolo",
    "Bogtong Bunao",
    "Bogtong Centro",
    "Bogtong Niog",
    "Bogtong Silag",
    "Buaya",
    "Buenlag",
    "Bueno",
    "Bunagan",
    "Bunlalacao",
    "Burgos Street (Poblacion)",
    "Cabaluyan 1st",
    "Cabaluyan 2nd",
    "Cabarabuan",
    "Cabaruan",
    "Cabayaoasan",
    "Cabayugan",
    "Cacaoiten",
    "Calomboyan Norte",
    "Calomboyan Sur",
    "Calvo (Poblacion)",
    "Casilagan",
    "Catarataraan",
    "Caturay Norte",
    "Caturay Sur",
    "Caviernesan",
    "Dorongan Ketaket",
    "Dorongan Linmansangan",
    "Dorongan Punta",
    "Dorongan Sawat",
    "Dorongan Valerio",
    "General Luna (Poblacion)",
    "Historia",
    "Lawak Langka",
    "Linmansangan",
    "Lopez (Poblacion)",
    "Mabini (Poblacion)",
    "Macarang",
    "Malabobo",
    "Malibong",
    "Malunec",
    "Maravilla (Poblacion)",
    "Maravilla-Arellano Ext. (Pob)",
    "Muelang",
    "Naguilayan East",
    "Naguilayan West",
    "Nancasalan Cabison-Bulaney-Niog",
    "Olegario-Caoile (Poblacion)",
    "Olo Cacamposan",
    "Olo Cafabrosan",
    "Olo Cagarlitan",
    "Osmeña (Poblacion)",
    "Pacalat",
    "Pampano",
    "Parian",
    "Paul",
    "Pogon-Aniat",
    "Pogon-Lomboy (Poblacion)",
    "Ponglo-Baleg",
    "Ponglo-Muelag",
    "Quetegan",
    "Quezon (Poblacion)",
    "Salavante",
    "Sapang",
    "Sonson Ongkit",
    "Suaco",
    "Tagac",
    "Takipan",
    "Talogtog",
    "Tococ Barikir",
    "Torre 1st",
    "Torre 2nd",
    "Torres Bugallon (Poblacion)",
    "Umangan",
    "Zamora (Poblacion)",
]

ATTRACTIONS = [
    {
        "name": "Manleluag Spring Protected Landscape",
        "description": "A 1,935-hectare national protected landscape nestled in the foothills of the Zambales Mountain Range. Renowned for its natural sulfuric thermal hot springs, crystal-clear cold stream pools, lush dipterocarp forests, and riverside picnic cottages.",
        "category": "Nature",
        "latitude": 15.6667,
        "longitude": 120.2833,
        "image_url": "/img/manleluag_spring.webp",
        "barangay": "Malabobo",
        "is_featured": True,
        "opening_hours": "6:00 AM – 5:30 PM Daily",
        "entrance_fee": "₱30 (Adults) / ₱15 (Students & Seniors)",
        "contact_info": "mangatarem.tourism@pangasinan.gov.ph",
        "facilities": "Hot Spring Pools, Cold Stream Baths, Picnic Cottages, Restrooms, Parking",
        "directions": "Romulo Highway toward Zambales border. Turn left at Brgy. Malabobo junction.",
    },
    {
        "name": "Daang Kalikasan",
        "description": "A breathtaking 54-kilometer scenic mountain highway that traverses the undulating ridges of the Zambales Mountain Range, connecting Mangatarem to Santa Cruz, Zambales.",
        "category": "Nature",
        "latitude": 15.7000,
        "longitude": 120.2500,
        "image_url": "/img/daang_kalikasan.webp",
        "barangay": "Malabobo",
        "is_featured": True,
        "opening_hours": "6:00 AM – 6:00 PM Daily",
        "entrance_fee": "Free Entry (Public Scenic Highway)",
        "facilities": "Viewpoints, Roadside Stalls, Parking Bays",
        "directions": "From town center head southwest along Romulo Highway towards Brgy. Malabobo.",
    },
    {
        "name": "St. Raymund de Penafort Church",
        "description": "A Spanish colonial brick-and-stone Roman Catholic church originally established by Dominican missionaries in 1835. Features a Baroque and Neoclassical facade constructed from local clay bricks.",
        "category": "Historical",
        "latitude": 15.7889,
        "longitude": 120.2986,
        "image_url": "/img/st_raymund_church.webp",
        "barangay": "Arellano Street (Poblacion)",
        "is_featured": True,
        "opening_hours": "5:30 AM – 7:00 PM Daily",
        "entrance_fee": "Free Entry (Active Parish Church)",
        "contact_info": "parish.mangatarem@lingayen-dagupan.org",
        "facilities": "Parish Hall, Restrooms, Courtyard Plaza, Candle Chapel",
        "directions": "Directly located at the town center along Romulo Highway fronting the municipal plaza.",
    },
    {
        "name": "Timmanguyob Falls",
        "description": "A cascade hidden within the western mountain rainforest of Mangatarem. Features a secluded freshwater plunge pool and lush endemic forest flora.",
        "category": "Nature",
        "latitude": 15.6833,
        "longitude": 120.2667,
        "image_url": "/img/attractions/timmanguyob_falls.png",
        "barangay": "Cabaluyan 2nd",
        "is_featured": False,
        "opening_hours": "6:00 AM – 4:30 PM Daily",
        "entrance_fee": "₱20 Barangay Environmental Fee + Guide Fee",
        "facilities": "Natural Plunge Pool, Forest Trails, River Crossing Boulders",
        "directions": "Access via Barangay Cabaluyan staging area followed by a 45-minute guided river trek.",
    },
    {
        "name": "Canding (Kanding) Falls",
        "description": "A series of pristine mountain rapids, tiered cascades, and deep limestone pools surrounded by wild bamboo groves and rolling foothills.",
        "category": "Nature",
        "latitude": 15.7891,
        "longitude": 120.2928,
        "image_url": "/img/attractions/canding_falls/image_1.jpg",
        "barangay": "Arellano Street (Poblacion)",
        "is_featured": False,
        "opening_hours": "7:00 AM – 5:00 PM Daily",
        "entrance_fee": "₱20 Eco Fee",
        "facilities": "Natural Swimmable Pools, Bamboo Shade Huts, Staging Grounds",
        "directions": "From town center proceed north-west to the trail jump-off point.",
    },
    {
        "name": "Pacalat River",
        "description": "A historic waterway flowing through the heart of Mangatarem, offering scenic riverbanks, bamboo hanging bridges, and refreshing freshwater swimming.",
        "category": "Nature",
        "latitude": 15.7891,
        "longitude": 120.2928,
        "image_url": "/img/attractions/pacalat_river/image_1.jpg",
        "barangay": "Pacalat",
        "is_featured": False,
        "opening_hours": "Open 24 Hours",
        "entrance_fee": "Free Access",
        "facilities": "Riverbanks, Shaded Trees, Walking Path",
        "directions": "Accessible from the poblacion bridge and riverside embankments.",
    },
    {
        "name": "Municipal Town Plaza",
        "description": "The municipal civic and cultural center featuring the historical municipal hall, war memorial, children's park, and landscaped civic gardens.",
        "category": "Public Space",
        "latitude": 15.7885,
        "longitude": 120.2960,
        "image_url": "/img/attractions/municipal_hall/image_1.jpg",
        "barangay": "Arellano Street (Poblacion)",
        "is_featured": False,
        "opening_hours": "Open 24 Hours",
        "entrance_fee": "Free Access",
        "contact_info": "info@mangatarem.gov.ph",
        "facilities": "Open Plaza, Benches, Night Lighting, Event Stage, Children Playground",
        "directions": "Town center, Poblacion, Mangatarem, Pangasinan.",
    },
]

ESTABLISHMENTS = [
    {
        "name": "Daang Kalikasan Pine Ridge Cafe",
        "description": "Scenic hilltop coffee shop and dining stopover offering fresh brewed mountain coffee, native puto, and panoramic views of Daang Kalikasan ridge.",
        "type": "Restaurant",
        "price_range": "₱₱",
        "latitude": 15.7015,
        "longitude": 120.2520,
        "barangay": "Malabobo",
        "address": "KM 12 Daang Kalikasan Scenic Highway",
        "contact_number": "+63 917 123 4567",
        "email": "pineridge@mangatarem.com",
    },
    {
        "name": "Manleluag Eco Mountain Lodge",
        "description": "Cozy rustic cottages and eco-camp cabins set just outside the protected thermal springs area. Family-friendly with local Pangasinan home cooking.",
        "type": "Inn / Lodging",
        "price_range": "₱₱",
        "latitude": 15.6680,
        "longitude": 120.2845,
        "barangay": "Malabobo",
        "address": "Barangay Road, Sitio Manleluag",
        "contact_number": "+63 920 987 6543",
        "email": "ecolodge@mangatarem.com",
    },
    {
        "name": "Poblacion Heritage Grill & Native Delights",
        "description": "Authentic Mangatarem carinderia and grill famous for grilled bangus, pigar-pigar, tupig, and traditional native kakanin.",
        "type": "Restaurant",
        "price_range": "₱",
        "latitude": 15.7890,
        "longitude": 120.2970,
        "barangay": "Arellano Street (Poblacion)",
        "address": "Romulo Highway corner Burgos St.",
        "contact_number": "+63 918 555 1234",
        "email": "heritagegrill@mangatarem.com",
    },
]

EVENTS = [
    {
        "name": "Mangatarem Mango & Agri-Tourism Fair",
        "description": "Annual agro-tourism festival showcasing Mangatarem's sweet carabao mangoes, farm produce, native crafts, and street performances.",
        "category": "Festival",
        "location": "Municipal Town Plaza, Poblacion",
        "latitude": 15.7885,
        "longitude": 120.2960,
        "date": datetime(2026, 4, 18, 8, 0, tzinfo=UTC),
        "barangay": "Arellano Street (Poblacion)",
    },
    {
        "name": "Feast of San Raymundo de Peñafort",
        "description": "Traditional municipal patronal town fiesta honoring San Raymundo de Peñafort with civic parades, church rites, and community reunions.",
        "category": "Religious",
        "location": "St. Raymund de Penafort Parish Church",
        "latitude": 15.7889,
        "longitude": 120.2986,
        "date": datetime(2027, 1, 23, 6, 0, tzinfo=UTC),
        "barangay": "Arellano Street (Poblacion)",
    },
    {
        "name": "Manleluag Eco-Trail & Tree Planting Walk",
        "description": "Community eco-tour and tree planting trek traversing the foothills of Manleluag Spring Protected Landscape with DENR forest rangers.",
        "category": "Eco-Tour",
        "location": "Manleluag Spring Protected Landscape",
        "latitude": 15.6667,
        "longitude": 120.2833,
        "date": datetime(2026, 6, 5, 6, 30, tzinfo=UTC),
        "barangay": "Malabobo",
    },
]


async def seed_data():
    async with async_session_factory() as db:
        print("[1/5] Seeding 82 Barangays...")
        barangay_map: dict[str, BarangayInfo] = {}
        for b_name in MANGATAREM_BARANGAYS:
            existing_b = (await db.execute(select(BarangayInfo).where(BarangayInfo.name == b_name))).scalar_one_or_none()
            if not existing_b:
                existing_b = BarangayInfo(
                    name=b_name,
                    history=f"Barangay {b_name}, Municipality of Mangatarem, Pangasinan.",
                )
                db.add(existing_b)
                await db.flush()
            barangay_map[b_name] = existing_b

        print(f"Total Barangays available: {len(barangay_map)}")

        print("[2/5] Ensuring Admin User...")
        admin_q = await db.execute(select(User).where(User.email == "admin@mangatarem.gov.ph"))
        admin = admin_q.scalar_one_or_none()
        if not admin:
            admin = User(
                username="admin_user",
                email="admin@mangatarem.gov.ph",
                password=generate_password_hash("AdminPass123!"),
                role="admin",
                is_approved=True,
            )
            db.add(admin)
            await db.flush()

        print("[3/5] Seeding Canonical Attractions...")
        for att in ATTRACTIONS:
            existing_att = (await db.execute(select(Attraction).where(Attraction.name == att["name"]))).scalar_one_or_none()
            b_info = barangay_map.get(att["barangay"])
            b_id = b_info.id if b_info else None

            if not existing_att:
                new_att = Attraction(
                    name=att["name"],
                    description=att["description"],
                    category=att["category"],
                    latitude=att["latitude"],
                    longitude=att["longitude"],
                    image_url=att.get("image_url"),
                    barangay_id=b_id,
                    is_featured=att.get("is_featured", False),
                    physical_status="Open",
                    advisory_status="Normal",
                    opening_hours=att.get("opening_hours"),
                    entrance_fee=att.get("entrance_fee"),
                    contact_info=att.get("contact_info"),
                    facilities=att.get("facilities"),
                    directions=att.get("directions"),
                    status="approved",
                    user_id=admin.id,
                )
                db.add(new_att)

        print("[4/5] Seeding Establishments & Events...")
        for est in ESTABLISHMENTS:
            existing_est = (await db.execute(select(Establishment).where(Establishment.name == est["name"]))).scalar_one_or_none()
            b_info = barangay_map.get(est["barangay"])
            b_id = b_info.id if b_info else None

            if not existing_est:
                new_est = Establishment(
                    name=est["name"],
                    description=est["description"],
                    type=est["type"],
                    price_range=est.get("price_range"),
                    latitude=est["latitude"],
                    longitude=est["longitude"],
                    address=est.get("address"),
                    contact_number=est.get("contact_number"),
                    email=est.get("email"),
                    barangay_id=b_id,
                    owner_id=admin.id,
                    status="approved",
                )
                db.add(new_est)

        for ev in EVENTS:
            existing_ev = (await db.execute(select(Event).where(Event.name == ev["name"]))).scalar_one_or_none()
            b_info = barangay_map.get(ev["barangay"])
            b_id = b_info.id if b_info else None

            if not existing_ev:
                new_ev = Event(
                    name=ev["name"],
                    description=ev["description"],
                    category=ev["category"],
                    location=ev["location"],
                    latitude=ev.get("latitude"),
                    longitude=ev.get("longitude"),
                    date=ev["date"],
                    barangay_id=b_id,
                    status="approved",
                    user_id=admin.id,
                )
                db.add(new_ev)

        print("[5/5] Seeding General Community Chat Room...")
        general_room_q = await db.execute(select(ChatRoom).where(ChatRoom.type == "general"))
        general_room = general_room_q.scalar_one_or_none()
        if not general_room:
            general_room = ChatRoom(
                type="general",
            )
            db.add(general_room)

        await db.commit()
        print("Initial database seed completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed_data())
