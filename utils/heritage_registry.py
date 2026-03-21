"""
Heritage Type Registry — single source of truth for heritage route handlers.

Maps URL slugs to models, labels, and field definitions. Used by admin routes,
API routes, and public routes to avoid duplicating type logic.
"""
from heritage_models.built_heritage import BUILT_HERITAGE_DETAIL as BuiltHeritage
from heritage_models.natural_heritage import NATURAL_HERITAGE_DETAIL as NaturalHeritage
from heritage_models.movable_heritage import MOVABLE_HERITAGE_DETAIL as MovableHeritage
from heritage_models.intangible_heritage import INTANGIBLE_HERITAGE_DETAIL as IntangibleHeritage
from heritage_models.personality_profile import PERSONALITY_DETAIL as PersonalityProfile
from heritage_models.cultural_institution import INSTITUTION_DETAIL as CulturalInstitution
from heritage_models.lgu_culture_program import LGU_PROGRAM_DETAIL as LGUCultureProgram


HERITAGE_TYPES = {
    "built": {
        "model": BuiltHeritage,
        "label": "Built Heritage",
        "label_plural": "Built Heritage Sites",
        "form": "02",
        "has_coords": True,
        "name_field": "name",
        "fields": [
            ("form_control_number", "Form Control Number", "text", False),
            ("name", "Name of Heritage", "text", True),
            ("category", "Category", "text", True),
            ("address", "Address/Location", "text", True),
            ("dates", "Relevant Dates", "text", False),
            ("ownership", "Ownership", "text", False),
            ("latitude", "Latitude", "number", False),
            ("longitude", "Longitude", "number", False),
            ("description", "Physical Description", "textarea", False),
            ("stories", "Associated Stories", "textarea", False),
            ("significance", "Significance", "textarea", False),
            ("protection_status", "Protection Status", "text", False),
            ("constraints_threats", "Constraints & Threats", "textarea", False),
            ("conservation_measures", "Conservation Measures", "textarea", False),
            ("key_informants", "Key Informants", "json", False),
            ("reference_sources", "Reference Sources", "textarea", False),
            ("mapper_name", "Mapper/Profiler Name", "text", False),
            ("date_profiled", "Date Profiled", "date", False),
        ],
    },
    "natural": {
        "model": NaturalHeritage,
        "label": "Natural Heritage",
        "label_plural": "Natural Heritage Sites",
        "form": "01A",
        "has_coords": True,
        "name_field": "name",
        "fields": [
            ("form_control_number", "Form Control Number", "text", False),
            ("name", "Name of Site", "text", True),
            ("category", "Category", "text", True),
            ("location", "Location", "text", True),
            ("area_hectares", "Area (hectares)", "number", False),
            ("ownership", "Ownership/Jurisdiction", "text", False),
            ("latitude", "Latitude", "number", False),
            ("longitude", "Longitude", "number", False),
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
        ],
    },
    "movable": {
        "model": MovableHeritage,
        "label": "Movable Heritage",
        "label_plural": "Movable Heritage Items",
        "form": "03",
        "has_coords": True,
        "name_field": "name",
        "fields": [
            ("form_control_number", "Form Control Number", "text", False),
            ("name", "Name of Object", "text", True),
            ("type_of_object", "Type of Object", "text", False),
            ("category", "Category", "text", True),
            ("location", "Location", "text", True),
            ("ownership", "Ownership", "text", False),
            ("latitude", "Latitude", "number", False),
            ("longitude", "Longitude", "number", False),
            ("description", "Physical Description", "textarea", False),
            ("date_produced", "Date Produced", "text", False),
            ("medium_material", "Medium/Material", "text", False),
            ("dimension", "Dimensions", "text", False),
            ("stories", "Associated Stories", "textarea", False),
            ("significance", "Significance", "textarea", False),
            ("status_condition", "Status/Condition", "text", False),
            ("constraints_threats", "Constraints & Threats", "textarea", False),
            ("conservation_measures", "Conservation Measures", "textarea", False),
            ("key_informants", "Key Informants", "json", False),
            ("reference_sources", "Reference Sources", "textarea", False),
            ("mapper_name", "Mapper/Profiler Name", "text", False),
            ("date_profiled", "Date Profiled", "date", False),
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
            ("form_control_number", "Form Control Number", "text", False),
            ("name", "Name", "text", True),
            ("category", "Category", "text", True),
            ("geographical_range", "Geographical Range", "textarea", False),
            ("related_domains", "Related Domains", "json", False),
            ("description", "Description", "textarea", False),
            ("culture_bearers", "Culture Bearers", "textarea", False),
            ("transmission_mode", "Mode of Transmission", "textarea", False),
            ("objects_used", "Objects Used", "json", False),
            ("stories", "Associated Stories", "textarea", False),
            ("significance", "Significance", "textarea", False),
            ("practice_status", "Practice Status", "text", False),
            ("constraints_threats", "Constraints & Threats", "textarea", False),
            ("safeguarding_measures", "Safeguarding Measures", "json", False),
            ("safeguarding_description", "Safeguarding Description", "textarea", False),
            ("key_informants", "Key Informants", "json", False),
            ("reference_sources", "Reference Sources", "textarea", False),
            ("mapper_name", "Mapper/Profiler Name", "text", False),
            ("date_profiled", "Date Profiled", "date", False),
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
            ("form_control_number", "Form Control Number", "text", False),
            ("name", "Full Name", "text", True),
            ("dates_of_birth_death", "Dates of Birth/Death", "text", False),
            ("address", "Address", "text", False),
            ("prominence_field", "Field of Prominence", "text", True),
            ("biography", "Biography", "textarea", False),
            ("achievements", "Works & Achievements", "json", False),
            ("significance", "Significance", "textarea", False),
            ("key_informants", "Key Informants", "json", False),
            ("reference_sources", "Reference Sources", "textarea", False),
            ("mapper_name", "Mapper/Profiler Name", "text", False),
            ("date_profiled", "Date Profiled", "date", False),
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
            ("form_control_number", "Form Control Number", "text", False),
            ("name", "Institution Name", "text", True),
            ("address", "Address", "text", False),
            ("latitude", "Latitude", "number", False),
            ("longitude", "Longitude", "number", False),
            ("type_of_institution", "Institution Type", "text", True),
            ("mandate", "Mandate & Description", "textarea", False),
            ("history", "History/Milestones", "textarea", False),
            ("stories", "Stories", "textarea", False),
            ("significance", "Significance", "textarea", False),
            ("condition", "Condition Status", "textarea", False),
            ("constraints_threats", "Constraints & Threats", "textarea", False),
            ("safeguarding_measures", "Safeguarding Measures", "textarea", False),
            ("key_informants", "Key Informants", "json", False),
            ("reference_sources", "Reference Sources", "textarea", False),
            ("mapper_name", "Mapper/Profiler Name", "text", False),
            ("date_profiled", "Date Profiled", "date", False),
        ],
    },
    "program": {
        "model": LGUCultureProgram,
        "label": "LGU Culture Program",
        "label_plural": "LGU Culture Programs",
        "form": "07",
        "has_coords": False,
        "name_field": "program_name",
        "fields": [
            ("form_control_number", "Form Control Number", "text", False),
            ("program_name", "Program Name", "text", True),
            ("lgu_name", "LGU Name", "text", True),
            ("vision", "Vision Statement", "textarea", False),
            ("mission", "Mission Statement", "textarea", False),
            ("goals", "Goal Statements", "textarea", False),
            ("date_created", "Date Created/Adoption", "date", False),
            ("history", "Brief History", "textarea", False),
            ("chief_executives", "Chief Executives", "json", False),
            ("policies", "Major Policies/Resolutions", "json", False),
            ("strategies", "Program Strategies", "textarea", False),
            ("budget", "Annual Investments/Budget", "json", False),
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
    fallback_id = getattr(item, 'heritage_profile_id', 'Unknown')
    return getattr(item, config["name_field"], f"Item {fallback_id}")
