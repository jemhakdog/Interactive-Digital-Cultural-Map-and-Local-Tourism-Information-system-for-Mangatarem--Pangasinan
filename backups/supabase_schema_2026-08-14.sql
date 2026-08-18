CREATE TABLE IF NOT EXISTS public."ANALYTICS_PAGE_VIEW" (
    "id" integer DEFAULT nextval('"ANALYTICS_PAGE_VIEW_id_seq"'::regclass),
    "page_url" character varying(500) NULL,
    "user_id" integer NULL,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "session_id" character varying(100) NULL,
    "ip_address" character varying(45) NULL,
    "device_info" text NULL,
    "view_type" character varying(50) NULL,
    "item_id" integer NULL,
    "page_name" character varying(100) NULL,
    PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS public."ATTRACTION" (
    "id" integer DEFAULT nextval('"ATTRACTION_id_seq"'::regclass),
    "name" character varying(100) NOT NULL,
    "description" text NULL,
    "category" character varying(50) NULL,
    "latitude" double precision NULL,
    "longitude" double precision NULL,
    "barangay_id" integer NULL,
    "image_url" character varying(255) NULL,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "heritage_profile_id" integer NULL,
    "status" character varying(20) DEFAULT 'pending'::character varying,
    "user_id" integer NULL,
    "is_featured" boolean DEFAULT false,
    "directions" text NULL,
    "osm_alternatives" jsonb NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("barangay_id") REFERENCES public."BARANGAY_INFO"
);
CREATE TABLE IF NOT EXISTS public."ATTRACTION_REVIEW" (
    "id" integer DEFAULT nextval('"ATTRACTION_REVIEW_id_seq"'::regclass),
    "user_id" integer NULL,
    "attraction_id" integer NULL,
    "rating" integer NOT NULL,
    "comment" text NULL,
    "status" character varying(20) DEFAULT 'pending'::character varying,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "parent_id" integer NULL,
    "updated_at" timestamp without time zone NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("attraction_id") REFERENCES public."ATTRACTION",
    FOREIGN KEY ("user_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."BARANGAY_INFO" (
    "id" integer DEFAULT nextval('"BARANGAY_INFO_id_seq"'::regclass),
    "name" character varying(100) NOT NULL,
    "map_geo_json" text NULL,
    "location_data" jsonb NULL,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "mission" text NULL,
    "vision" text NULL,
    "history" text NULL,
    "cultural_assets" text NULL,
    "traditions" text NULL,
    "local_practices" text NULL,
    "unique_features" text NULL,
    "user_id" integer NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("user_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."BOOKABLE_ASSET" (
    "id" integer DEFAULT nextval('"BOOKABLE_ASSET_id_seq"'::regclass),
    "attraction_id" integer NULL,
    "heritage_profile_id" integer NULL,
    "daily_capacity" integer NULL,
    "requires_approval" boolean NULL,
    "booking_instructions" text NULL,
    "status" character varying(20) NULL,
    "created_at" timestamp without time zone NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("attraction_id") REFERENCES public."ATTRACTION",
    FOREIGN KEY ("heritage_profile_id") REFERENCES public."HERITAGE_PROFILE"
);
CREATE TABLE IF NOT EXISTS public."BOOKING_SLOT" (
    "id" integer DEFAULT nextval('"BOOKING_SLOT_id_seq"'::regclass),
    "bookable_asset_id" integer NOT NULL,
    "date" date NOT NULL,
    "total_capacity" integer NOT NULL,
    "booked_count" integer NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("bookable_asset_id") REFERENCES public."BOOKABLE_ASSET"
);
CREATE TABLE IF NOT EXISTS public."BUSINESS_VERIFICATION" (
    "id" integer DEFAULT nextval('"BUSINESS_VERIFICATION_id_seq"'::regclass),
    "user_id" integer NOT NULL,
    "permit_document_url" character varying(500) NOT NULL,
    "other_document_url" character varying(500) NULL,
    "status" character varying(20) NULL,
    "submitted_at" timestamp without time zone NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("user_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."CHAT_MESSAGE" (
    "id" integer DEFAULT nextval('"CHAT_MESSAGE_id_seq"'::regclass),
    "chat_room_id" integer NOT NULL,
    "sender_id" integer NOT NULL,
    "content" text NOT NULL,
    "created_at" timestamp without time zone NULL,
    "is_system_msg" boolean NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("chat_room_id") REFERENCES public."CHAT_ROOM",
    FOREIGN KEY ("sender_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."CHAT_PARTICIPANT" (
    "id" integer DEFAULT nextval('"CHAT_PARTICIPANT_id_seq"'::regclass),
    "chat_room_id" integer NOT NULL,
    "user_id" integer NOT NULL,
    "joined_at" timestamp without time zone NULL,
    "last_read_at" timestamp without time zone NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("chat_room_id") REFERENCES public."CHAT_ROOM",
    FOREIGN KEY ("user_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."CHAT_ROOM" (
    "id" integer DEFAULT nextval('"CHAT_ROOM_id_seq"'::regclass),
    "type" character varying(20) NOT NULL,
    "barangay_id" integer NULL,
    "establishment_id" integer NULL,
    "created_at" timestamp without time zone NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("barangay_id") REFERENCES public."BARANGAY_INFO",
    FOREIGN KEY ("establishment_id") REFERENCES public."ESTABLISHMENT"
);
CREATE TABLE IF NOT EXISTS public."DATABASE_AUDIT_LOG" (
    "id" integer GENERATED ALWAYS AS IDENTITY,
    "user_id" integer NULL,
    "action" character varying(50) NOT NULL,
    "table_name" character varying(100) NOT NULL,
    "record_id" integer NULL,
    "ip_address" character varying(45) NULL,
    "user_agent" character varying(500) NULL,
    "query_summary" character varying(500) NULL,
    "status" character varying(20) DEFAULT 'success'::character varying,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("user_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."ESTABLISHMENT" (
    "id" integer GENERATED ALWAYS AS IDENTITY,
    "name" character varying(200) NOT NULL,
    "type" character varying(30) NOT NULL,
    "description" text NULL,
    "address" character varying(500) NULL,
    "latitude" double precision NOT NULL,
    "longitude" double precision NOT NULL,
    "barangay_id" integer NULL,
    "contact_number" character varying(50) NULL,
    "email" character varying(120) NULL,
    "website" character varying(300) NULL,
    "operating_hours" jsonb NULL,
    "price_range" character varying(20) NULL,
    "amenities" jsonb NULL,
    "cover_image_url" character varying(500) NULL,
    "logo_url" character varying(500) NULL,
    "owner_id" integer NOT NULL,
    "status" character varying(20) DEFAULT 'pending'::character varying,
    "is_featured" boolean DEFAULT false,
    "rating_avg" double precision DEFAULT 0,
    "review_count" integer DEFAULT 0,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("barangay_id") REFERENCES public."BARANGAY_INFO",
    FOREIGN KEY ("owner_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."ESTABLISHMENT_MENU_ITEM" (
    "id" integer GENERATED ALWAYS AS IDENTITY,
    "establishment_id" integer NOT NULL,
    "name" character varying(200) NOT NULL,
    "description" text NULL,
    "price" numeric NULL,
    "category" character varying(50) NULL,
    "image_url" character varying(500) NULL,
    "is_available" boolean DEFAULT true,
    "is_bestseller" boolean DEFAULT false,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("establishment_id") REFERENCES public."ESTABLISHMENT"
);
CREATE TABLE IF NOT EXISTS public."ESTABLISHMENT_REVIEW" (
    "id" integer GENERATED ALWAYS AS IDENTITY,
    "user_id" integer NOT NULL,
    "establishment_id" integer NOT NULL,
    "rating" integer NOT NULL,
    "comment" text NULL,
    "status" character varying(20) DEFAULT 'pending'::character varying,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "parent_id" integer NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("establishment_id") REFERENCES public."ESTABLISHMENT",
    FOREIGN KEY ("parent_id") REFERENCES public."ESTABLISHMENT_REVIEW",
    FOREIGN KEY ("user_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."ESTABLISHMENT_ROOM" (
    "id" integer GENERATED ALWAYS AS IDENTITY,
    "establishment_id" integer NOT NULL,
    "name" character varying(100) NOT NULL,
    "description" text NULL,
    "price_per_night" numeric NULL,
    "capacity" integer DEFAULT 2,
    "amenities" jsonb NULL,
    "image_urls" jsonb NULL,
    "is_available" boolean DEFAULT true,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("establishment_id") REFERENCES public."ESTABLISHMENT"
);
CREATE TABLE IF NOT EXISTS public."EVENT" (
    "id" integer DEFAULT nextval('"EVENT_id_seq"'::regclass),
    "name" character varying(200) NOT NULL,
    "description" text NULL,
    "date" date NULL,
    "barangay_id" integer NULL,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "location" character varying(255) NULL,
    "category" character varying(50) DEFAULT 'Civic'::character varying,
    "status" character varying(20) DEFAULT 'pending'::character varying,
    "user_id" integer NULL,
    "image_url" character varying(500) NULL,
    "latitude" double precision NULL,
    "longitude" double precision NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("barangay_id") REFERENCES public."BARANGAY_INFO"
);
CREATE TABLE IF NOT EXISTS public."GALLERY_ITEM" (
    "id" integer DEFAULT nextval('"GALLERY_ITEM_id_seq"'::regclass),
    "type" character varying(20) NOT NULL,
    "url" character varying(500) NOT NULL,
    "caption" text NULL,
    "user_id" integer NULL,
    "status" character varying(20) DEFAULT 'pending'::character varying,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("user_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."HERITAGE_PROFILE" (
    "id" integer DEFAULT nextval('"HERITAGE_PROFILE_id_seq"'::regclass),
    "form_control_number" character varying(100) NULL,
    "name_of_asset" character varying(200) NOT NULL,
    "common_name" character varying(200) NULL,
    "asset_type" character varying(100) NULL,
    "barangay_id" integer NULL,
    "location_details" text NULL,
    "contact_person" character varying(200) NULL,
    "contact_number" character varying(50) NULL,
    "ownership_type" character varying(50) NULL,
    "owner_administrator" character varying(200) NULL,
    "usage_status" character varying(50) NULL,
    "latitude" double precision NULL,
    "longitude" double precision NULL,
    "conservation_status" text NULL,
    "status" character varying(20) DEFAULT 'draft'::character varying,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "significance" text NULL,
    "mapper_name" character varying(200) NULL,
    "date_profiled" date NULL,
    "user_id" integer NULL,
    "form_data" json NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("barangay_id") REFERENCES public."BARANGAY_INFO"
);
CREATE TABLE IF NOT EXISTS public."MAP_FEEDBACK" (
    "id" integer DEFAULT nextval('"MAP_FEEDBACK_id_seq"'::regclass),
    "attraction_id" integer NULL,
    "feedback_type" character varying(50) NOT NULL,
    "message" text NOT NULL,
    "status" character varying(20) NULL,
    "created_at" timestamp without time zone NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("attraction_id") REFERENCES public."ATTRACTION"
);
CREATE TABLE IF NOT EXISTS public."NEWSLETTER_HISTORY" (
    "id" integer DEFAULT nextval('"NEWSLETTER_HISTORY_id_seq"'::regclass),
    "subject" character varying(200) NOT NULL,
    "content" text NOT NULL,
    "recipient_count" integer NULL,
    "sent_at" timestamp without time zone NULL,
    PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS public."NEWSLETTER_SUBSCRIBER" (
    "id" integer DEFAULT nextval('"NEWSLETTER_SUBSCRIBER_id_seq"'::regclass),
    "email" character varying(120) NOT NULL,
    "is_active" boolean DEFAULT true,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS public."PASSWORD_RESET_TOKEN" (
    "id" integer DEFAULT nextval('"PASSWORD_RESET_TOKEN_id_seq"'::regclass),
    "user_id" integer NULL,
    "token" character varying(128) NOT NULL,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "expires_at" timestamp with time zone NULL,
    "used" boolean DEFAULT false,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("user_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."RESERVATION" (
    "id" integer DEFAULT nextval('"RESERVATION_id_seq"'::regclass),
    "user_id" integer NOT NULL,
    "booking_slot_id" integer NOT NULL,
    "party_size" integer NOT NULL,
    "primary_contact" character varying(100) NULL,
    "special_requests" text NULL,
    "status" character varying(20) NULL,
    "qr_code_token" character varying(20) NULL,
    "created_at" timestamp without time zone NULL,
    "updated_at" timestamp without time zone NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("booking_slot_id") REFERENCES public."BOOKING_SLOT",
    FOREIGN KEY ("user_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."REVIEW_PHOTO" (
    "id" integer DEFAULT nextval('"REVIEW_PHOTO_id_seq"'::regclass),
    "review_id" integer NOT NULL,
    "url" character varying(500) NOT NULL,
    "created_at" timestamp without time zone NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("review_id") REFERENCES public."ATTRACTION_REVIEW"
);
CREATE TABLE IF NOT EXISTS public."USER" (
    "id" integer GENERATED ALWAYS AS IDENTITY,
    "username" character varying(80) NOT NULL,
    "email" character varying(120) NOT NULL,
    "password" character varying(255) NOT NULL,
    "role" character varying(20) DEFAULT 'user'::character varying,
    "barangay_id" integer NULL,
    "is_approved" boolean DEFAULT false,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "is_superuser" boolean DEFAULT false,
    PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS public."USER_EVENT_INTEREST" (
    "id" integer DEFAULT nextval('"USER_EVENT_INTEREST_id_seq"'::regclass),
    "user_id" integer NULL,
    "event_id" integer NULL,
    "status" character varying(20) DEFAULT 'interested'::character varying,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("event_id") REFERENCES public."EVENT",
    FOREIGN KEY ("user_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."USER_FAVORITE_ATTRACTION" (
    "id" integer DEFAULT nextval('"USER_FAVORITE_ATTRACTION_id_seq"'::regclass),
    "user_id" integer NULL,
    "attraction_id" integer NULL,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("attraction_id") REFERENCES public."ATTRACTION",
    FOREIGN KEY ("user_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."USER_FAVORITE_ESTABLISHMENT" (
    "id" integer DEFAULT nextval('"USER_FAVORITE_ESTABLISHMENT_id_seq"'::regclass),
    "user_id" integer NOT NULL,
    "establishment_id" integer NOT NULL,
    "created_at" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS public."USER_NOTIFICATION" (
    "id" integer DEFAULT nextval('"USER_NOTIFICATION_id_seq"'::regclass),
    "user_id" integer NOT NULL,
    "title" character varying(200) NOT NULL,
    "message" text NOT NULL,
    "link" character varying(200) NULL,
    "is_read" boolean NULL,
    "created_at" timestamp without time zone NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("user_id") REFERENCES public."USER"
);
CREATE TABLE IF NOT EXISTS public."VISITOR_LOG" (
    "id" integer DEFAULT nextval('"VISITOR_LOG_id_seq"'::regclass),
    "target_type" character varying(255) NULL,
    "target_id" integer NULL,
    "visitor_count" integer NULL,
    "visitor_name" character varying(255) NULL,
    "visitor_age" integer NULL,
    "visitor_address" character varying(255) NULL,
    "is_system_user" boolean NULL,
    "visit_date" timestamp without time zone NULL,
    "logged_by" integer NULL,
    "visitor_user_id" integer NULL,
    "notes" text NULL,
    "created_at" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id")
);
