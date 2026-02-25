"""
Heritage Type Registry — single source of truth for heritage route handlers.

Maps URL slugs to models, labels, and field definitions. Used by admin routes,
API routes, and public routes to avoid duplicating type logic.
"""
from heritage_models.natural_heritage import NaturalHeritage
from heritage_models.intangible_heritage import IntangibleHeritage
from heritage_models.personality_profile import PersonalityProfile
from heritage_models.cultural_institution import CulturalInstitution
from heritage_models.lgu_culture_program import LGUCultureProgram


HERITAGE_TYPES = {
    "natural": {
        "model": NaturalHeritage,
        "label": "Natural Heritage",
        "label_plural": "Natural Heritage Sites",
        "form": "01A",
        "has_coords": True,
        "name_field": "name",
        "fields": [
            # (field_name, label, field_type, required)
            ("form_control_number", "Form Control Number (Manual Link)", "text", False),
            ("name", "Name of Site", "text", True),
            ("subcategory", "Subcategory", "select", True),
            ("location", "Location", "text", True),
            ("area_hectares", "Area (hectares)", "number", False),
            ("ownership", "Ownership/Jurisdiction", "text", False),
            ("lat", "Latitude", "number", False),
            ("lng", "Longitude", "number", False),
            ("description", "Physical Description", "textarea", False),
            ("stories", "Associated Stories/Legends", "textarea", False),
            ("significance", "Significance", "textarea", False),
            ("protection_status", "Protection Status", "text", False),
            ("constraints_threats", "Constraints & Threats", "textarea", False),
            ("conservation_measures", "Conservation Measures", "textarea", False),
            ("key_informants", "Key Informants", "json", False),
            ("reference_sources", "Reference Sources", "textarea", False),
            ("mapper_name", "Mapper/Profiler Name", "text", False),
            ("date_profiled", "Date Profiled", "date", False),
            ("photo_url", "Photo URL", "text", False),
        ],
        "subcategory_choices": [
            "mountain", "cave", "valley", "river", "waterfall",
            "lake", "spring", "island", "reef", "other",
        ],
    },
    "intangible": {
        "model": IntangibleHeritage,
        "label": "Intangible Heritage",
        "label_plural": "Intangible Heritage Items",
        "form": "04A",
        "has_coords": False,
        "name_field": "name",
        "fields": [
            ("form_control_number", "Form Control Number (Manual Link)", "text", False),
            ("name", "Name", "text", True),
            ("type", "Type", "select", True),
            ("photo_url", "Photo URL", "text", False),
            ("geographical_range", "Geographical Range", "textarea", False),
            ("related_domains", "Related Domains", "json", False),
            ("description", "Description", "textarea", False),
            ("culture_bearers", "Culture Bearers", "textarea", False),
            ("culture_bearer_photos", "Culture Bearer Photos", "json", False),
            ("transmission_mode", "Mode of Transmission", "textarea", False),
            ("objects_used", "Objects Used", "json", False),
            ("flora_fauna_used", "Flora/Fauna Used", "json", False),
            ("stories_associated", "Associated Stories", "textarea", False),
            ("significance", "Significance", "textarea", False),
            ("practice_status", "Practice Status", "text", False),
            ("constraints_threats", "Constraints & Threats", "textarea", False),
            ("safeguarding_measures", "Safeguarding Measures", "json", False),
            ("safeguarding_description", "Safeguarding Description", "textarea", False),
            ("supporting_docs", "Supporting Documents", "json", False),
            ("key_informants", "Key Informants", "json", False),
            ("reference_sources", "Reference Sources", "textarea", False),
            ("mapper_name", "Mapper/Profiler Name", "text", False),
            ("date_profiled", "Date Profiled", "date", False),
        ],
        "type_choices": [
            "proverbs", "songs", "myths", "chants", "riddles",
            "poems", "folk_speech", "rituals", "festivals",
            "traditional_knowledge", "performing_arts", "other",
        ],
    },
    "personality": {
        "model": PersonalityProfile,
        "label": "Significant Personality",
        "label_plural": "Significant Personalities",
        "form": "05",
        "has_coords": False,
        "name_field": "name",
        "fields": [
            ("form_control_number", "Form Control Number (Manual Link)", "text", False),
            ("name", "Full Name", "text", True),
            ("date_of_birth", "Date of Birth", "date", False),
            ("date_of_death", "Date of Death", "date", False),
            ("birth_place", "Birth Place", "text", False),
            ("present_address", "Present Address", "text", False),
            ("age", "Age", "number", False),
            ("prominence_field", "Field of Prominence", "select", True),
            ("photo_url", "Photo URL", "text", False),
            ("biography", "Biography", "textarea", False),
            ("significance", "Significance", "textarea", False),
            ("works_achievements", "Works & Achievements", "json", False),
            ("key_informants", "Key Informants", "json", False),
            ("reference_sources", "Reference Sources", "textarea", False),
            ("mapper_name", "Mapper/Profiler Name", "text", False),
            ("date_profiled", "Date Profiled", "date", False),
        ],
        "prominence_choices": [
            "arts", "science", "politics", "education", "religion",
            "sports", "business", "community_service", "other",
        ],
    },
    "institution": {
        "model": CulturalInstitution,
        "label": "Cultural Institution",
        "label_plural": "Cultural Institutions",
        "form": "06",
        "has_coords": True,
        "name_field": "name",
        "fields": [
            ("form_control_number", "Form Control Number (Manual Link)", "text", False),
            ("name", "Institution Name", "text", True),
            ("municipality", "Municipality", "text", True),
            ("province", "Province", "text", True),
            ("location_address", "Address", "text", False),
            ("lat", "Latitude", "number", False),
            ("lng", "Longitude", "number", False),
            ("facade_photo_url", "Facade Photo URL", "text", False),
            ("logo_url", "Logo URL", "text", False),
            ("logo_description", "Logo Description", "textarea", False),
            ("institution_type", "Institution Type", "select", True),
            ("mandate_description", "Mandate & Description", "textarea", False),
            ("milestones", "Milestones", "textarea", False),
            ("stories", "Stories", "textarea", False),
            ("significance", "Significance", "textarea", False),
            ("condition_status", "Condition Status", "textarea", False),
            ("constraints_threats", "Constraints & Threats", "textarea", False),
            ("safeguarding_measures", "Safeguarding Measures", "textarea", False),
            ("supporting_docs", "Supporting Documents", "json", False),
            ("key_informants", "Key Informants", "json", False),
            ("reference_sources", "Reference Sources", "textarea", False),
            ("mapper_name", "Mapper/Profiler Name", "text", False),
            ("date_profiled", "Date Profiled", "date", False),
        ],
        "institution_type_choices": [
            "library", "museum", "school", "church", "gallery",
            "cultural_center", "archive", "theater", "other",
        ],
    },
    "program": {
        "model": LGUCultureProgram,
        "label": "LGU Culture Program",
        "label_plural": "LGU Culture Programs",
        "form": "07",
        "has_coords": False,
        "name_field": "municipality",
        "fields": [
            ("form_control_number", "Form Control Number (Manual Link)", "text", False),
            ("municipality", "Municipality", "text", True),
            ("province", "Province", "text", True),
            ("vision_statement", "Vision Statement", "textarea", False),
            ("mission_statement", "Mission Statement", "textarea", False),
            ("goal_statements", "Goal Statements", "textarea", False),
            ("adoption_date", "Adoption Date", "date", False),
            ("brief_history", "Brief History", "textarea", False),
            ("logo_url", "Logo URL", "text", False),
            ("logo_legislation_date", "Logo Legislation Date", "date", False),
            ("logo_explanation", "Logo Explanation", "textarea", False),
            ("chief_executives", "Chief Executives", "json", False),
            ("resolutions", "Resolutions", "json", False),
            ("ordinances", "Ordinances", "json", False),
            ("ela_action_items", "ELA Action Items", "json", False),
            ("major_policies", "Major Policies", "json", False),
            ("program_strategies", "Program Strategies", "textarea", False),
            ("annual_investments", "Annual Investments", "json", False),
            ("culture_projects", "Culture Projects", "json", False),
            ("arts_council", "Arts & Culture Council", "json", False),
            ("alternative_livelihoods", "Alternative Livelihoods", "json", False),
            ("community_enterprises", "Community Enterprises", "json", False),
            ("peoples_stories", "People's Stories", "textarea", False),
            ("key_informants", "Key Informants", "json", False),
            ("reference_sources", "Reference Sources", "textarea", False),
            ("mapper_name", "Mapper/Profiler Name", "text", False),
            ("date_profiled", "Date Profiled", "date", False),
        ],
    },
}

# Shared fields excluded from form input (auto-managed)
SYSTEM_FIELDS = {
    "id", "status", "user_id", "reviewed_by", "reviewed_at",
    "created_at", "updated_at",
}


def get_heritage_config(heritage_type):
    """Get heritage type config or None if invalid type."""
    return HERITAGE_TYPES.get(heritage_type)


def get_heritage_model(heritage_type):
    """Get the SQLAlchemy model class for a heritage type."""
    config = get_heritage_config(heritage_type)
    return config["model"] if config else None


def get_all_types():
    """Return list of (slug, config) for iteration."""
    return list(HERITAGE_TYPES.items())


def get_display_name(item, heritage_type):
    """Get the display name of a heritage item based on its type."""
    config = HERITAGE_TYPES[heritage_type]
    fallback_id = getattr(item, 'id', getattr(item, 'profile_id', 'Unknown'))
    return getattr(item, config["name_field"], str(fallback_id))
