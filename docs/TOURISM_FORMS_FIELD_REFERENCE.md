# Tourism Forms Database Schema - Field Reference

## Overview

This document provides a comprehensive field reference for all tourism heritage models. Use this as a guide when filling out forms or building API endpoints.

---

## Table of Contents

1. [NaturalHeritage](#naturalheritage) - Form 01A
2. [Attraction (Enhanced)](#attraction-enhanced) - Forms 02A & 03A
3. [IntangibleHeritage](#intangibleheritage) - Form 04A
4. [PersonalityProfile](#personalityprofile) - Form 05
5. [CulturalInstitution](#culturalinstitution) - Form 06
6. [LGUCultureProgram](#lgucultureprogram) - Form 07

---

## NaturalHeritage

**Source**: Form 01A - Natural Resources and Land Formations

### Fields

| Field Name | Type | Required | Description | Example |
|------------|------|----------|-------------|---------|
| `name` | String(200) | Yes | Name of natural heritage site | "Mount Balungao" |
| `subcategory` | String(50) | Yes | Type of land formation | "mountain", "cave", "valley" |
| `location` | String(200) | Yes | Geographic location | "Barangay Balungao" |
| `area_hectares` | Float | No | Area in hectares | 150.5 |
| `ownership` | String(200) | No | Ownership or jurisdiction | "Mangatarem LGU" |
| `lat` | Float | No | Latitude for mapping | 15.8123 |
| `lng` | Float | No | Longitude for mapping | 120.4567 |
| `description` | Text | No | Physical features description | |
| `stories` | Text | No | Associated legends/stories | |
| `significance` | Text | No | Historical/cultural significance | |
| `protection_status` | String(100) | No | Conservation status | "Protected area" |
| `constraints_threats` | Text | No | Current threats or issues | |
| `conservation_measures` | Text | No | Active conservation efforts | |
| `key_informants` | JSON | No | Array of informant details | `[{"name": "Juan Dela Cruz", "role": "Elder"}]` |
| `reference_sources` | Text | No | References and citations | |
| `mapper_name` | String(200) | No | Who profiled this | "Tourism Office Staff" |
| `date_profiled` | Date | No | When it was profiled | "2024-01-15" |
| `photo_url` | String(500) | No | Main photo URL | |

**Approval Workflow Fields**:
- `status`: "pending", "approved", "rejected"
- `user_id`: FK to User (submitter)
- `reviewed_by`: FK to User (reviewer)
- `reviewed_at`: Timestamp

---

## Attraction (Enhanced)

**Sources**: 
- Form 02A - Tangible Immovable (Buildings)
- Form 03A - Tangible Movable (Archaeological Items)

### Original Fields
*(See existing Attraction model - name, description, category, barangay, lat, lng, etc.)*

### New Heritage Fields

| Field Name | Type | Required | Form | Description |
|------------|------|----------|------|-------------|
| `heritage_type` | String(50) | No | Both | "building", "archaeological", "natural", "standard" |
| **Form 02A - Building Fields** |
| `building_type` | String(50) | No | 02A | "municipal_hall", "church", "bridge" |
| `year_constructed` | Integer | No | 02A | Year built | 1950 |
| `ownership_type` | String(20) | No | 02A | "public" or "private" |
| `declaration_legislation` | Text | No | 02A | Legal declarations |
| `physical_description` | Text | No | 02A | Exterior/interior details |
| `history_structure` | Text | No | 02A | Construction history |
| `occupation_status` | String(20) | No | 02A | "occupied" or "not_occupied" |
| `stories_associated` | Text | No | 02A | Associated stories |
| `condition` | String(20) | No | 02A | "excellent", "good", "fair", "deteriorated", "ruins" |
| `condition_remarks` | Text | No | 02A | Condition details |
| `is_altered` | Boolean | No | 02A | Structure modified? |
| `is_original_site` | Boolean | No | 02A | On original location? |
| `integrity_remarks` | Text | No | 02A | Integrity details |
| `conservation_measures` | Text | No | 02A | Conservation efforts |
| `movable_heritage_list` | JSON | No | 02A | Objects within premises |
| **Form 03A - Archaeological Fields** |
| `object_type` | String(50) | No | 03A | "stone_tools", "ceramics", "metal" |
| `place_found` | String(200) | No | 03A | Where it was discovered |
| `date_found` | Date | No | 03A | Discovery date |
| `estimated_age` | String(100) | No | 03A | Age estimate |
| `acquisition_type` | String(50) | No | 03A | How acquired |
| `materials` | String(200) | No | 03A | Materials used |
| `dimensions` | String(100) | No | 03A | Object dimensions |
| `comparative_criteria` | Text | No | 03A | Provenance, rarity notes |
| **Common Heritage Fields** |
| `significance_types` | JSON | No | Both | `["historical", "aesthetic", "spiritual"]` |
| `constraints_threats` | Text | No | Both | Threats or issues |
| `key_informants` | JSON | No | Both | Array of informants |
| `reference_sources` | Text | No | Both | Citations |
| `mapper_name` | String(200) | No | Both | Profiler name |
| `date_profiled` | Date | No | Both | Profile date |

---

## IntangibleHeritage

**Source**: Form 04A - Oral Traditions and Expressions

### Fields

| Field Name | Type | Required | Description | Example |
|------------|------|----------|-------------|---------|
| `name` | String(200) | Yes | Name of the element | "Pangasinan Folk Song" |
| `type` | String(50) | Yes | Type of heritage | "proverbs", "songs", "myths", "chants" |
| `photo_url` | String(500) | No | Reference image | |
| `geographical_range` | Text | No | Where it's practiced | "Western Pangasinan" |
| `related_domains` | JSON | No | Related cultural domains | `["performing_arts", "rituals"]` |
| `description` | Text | No | Full description of practice | |
| `culture_bearers` | Text | No | Who practices it | |
| `culture_bearer_photos` | JSON | No | Photos of practitioners | `["url1", "url2"]` |
| `transmission_mode` | Text | No | How knowledge is passed | "Oral tradition from elders" |
| `objects_used` | JSON | No | Associated objects | `[{"name": "Bamboo flute", "age": "50 years"}]` |
| `flora_fauna_used` | JSON | No | Natural resources used | `[{"name": "Bamboo", "use": "Instrument"}]` |
| `stories_associated` | Text | No | Related narratives | |
| `significance` | Text | No | Cultural significance | |
| `practice_status` | String(100) | No | Current condition | "Active", "Endangered" |
| `constraints_threats` | Text | No | Threats to practice | |
| `safeguarding_measures` | JSON | No | Preservation efforts | `["formal_education", "documentation"]` |
| `safeguarding_description` | Text | No | Details of measures | |
| `supporting_docs` | JSON | No | Documentation types | `["audio", "video", "photos"]` |

---

## PersonalityProfile

**Source**: Form 05 - Significant Personalities

### Fields

| Field Name | Type | Required | Description | Example |
|------------|------|----------|-------------|---------|
| `name` | String(200) | Yes | Full name | "Dr. Juan Dela Cruz" |
| `date_of_birth` | Date | No | Birth date | "1950-06-15" |
| `date_of_death` | Date | No | Death date (if applicable) | |
| `birth_place` | String(200) | No | Place of birth | "Mangatarem, Pangasinan" |
| `present_address` | String(300) | No | Current address (if living) | |
| `age` | Integer | No | Current age | 74 |
| `prominence_field` | String(100) | Yes | Field of expertise | "Arts", "Science", "Politics" |
| `photo_url` | String(500) | No | Portrait photo | |
| `biography` | Text | No | Life story, awards, contributions | |
| `significance` | Text | No | Historical/cultural significance | |
| `works_achievements` | JSON | No | List of works/achievements | `[{"year": 1980, "work": "Novel Title"}]` |

---

## CulturalInstitution

**Source**: Form 06 - Cultural Institutions

### Fields

| Field Name | Type | Required | Description | Example |
|------------|------|----------|-------------|---------|
| `name` | String(200) | Yes | Institution name | "Mangatarem Public Library" |
| `municipality` | String(100) | Yes | Municipality | "Mangatarem" |
| `province` | String(100) | Yes | Province | "Pangasinan" |
| `location_address` | String(300) | No | Full address | |
| `lat` | Float | No | Latitude | |
| `lng` | Float | No | Longitude | |
| `facade_photo_url` | String(500) | No | Building photo | |
| `logo_url` | String(500) | No | Institution logo | |
| `logo_description` | Text | No | Logo meaning/symbols | |
| `institution_type` | String(100) | Yes | Type | "library", "museum", "school" |
| `mandate_description` | Text | No | History, officials, contact | |
| `milestones` | Text | No | Significant achievements | |
| `stories` | Text | No | Associated narratives | |
| `significance` | Text | No | Cultural significance | |
| `condition_status` | Text | No | Current state | |
| `constraints_threats` | Text | No | Challenges faced | |
| `safeguarding_measures` | Text | No | Preservation efforts | |
| `supporting_docs` | JSON | No | Documentation | `["photos", "audio", "writeups"]` |

---

## LGUCultureProgram

**Source**: Form 07 - LGU Programs and Projects for Culture

### Fields

| Field Name | Type | Required | Description | Example |
|------------|------|----------|-------------|---------|
| `municipality` | String(100) | Yes (Unique) | Municipality name | "Mangatarem" |
| `province` | String(100) | Yes | Province | "Pangasinan" |
| `vision_statement` | Text | No | LGU vision | |
| `mission_statement` | Text | No | LGU mission | |
| `goal_statements` | Text | No | LGU goals | |
| `adoption_date` | Date | No | When adopted | |
| `brief_history` | Text | No | LGU history | |
| `logo_url` | String(500) | No | LGU emblem | |
| `logo_legislation_date` | Date | No | When logo was adopted | |
| `logo_explanation` | Text | No | Emblem meaning | |
| `chief_executives` | JSON | No | Past mayors | `[{"name": "Mayor X", "term_start": 2016, "term_end": 2019}]` |
| `resolutions` | JSON | No | Culture resolutions | `[{"year": 2023, "nature": "Heritage preservation", "number": "R-2023-01"}]` |
| `ordinances` | JSON | No | Culture ordinances | |
| `ela_action_items` | JSON | No | ELA agenda items | |
| `major_policies` | JSON | No | Key policies | `[{"date": "2023-01-15", "title": "Heritage Protection Act"}]` |
| `program_strategies` | Text | No | Development strategies | |
| `annual_investments` | JSON | No | Budget by year | `{"2023": {"programs": {"Heritage": 500000}}}` |
| `culture_projects` | JSON | No | Projects by year | `{"2023": {"Festival Revival": 200000}}` |
| `arts_council` | JSON | No | Council details | `{"creation_date": "2020-01-01", "legal_basis": "Ordinance 123"}` |
| `alternative_livelihoods` | JSON | No | Culture-based livelihoods | `[{"livelihood": "Weaving", "lgu_support": "Training"}]` |
| `community_enterprises` | JSON | No | Enterprises list | `[{"name": "Handicrafts Co-op", "nature": "Weaving", "date": "2022"}]` |
| `peoples_stories` | Text | No | Community narratives | |

---

## Common Approval Workflow

All models include these fields:

| Field | Type | Description |
|-------|------|-------------|
| `status` | String(20) | "pending", "approved", "rejected" |
| `user_id` | FK→User | Who submitted the entry |
| `reviewed_by` | FK→User | Who reviewed it |
| `reviewed_at` | DateTime | When it was reviewed |
| `created_at` | DateTime | When created |
| `updated_at` | DateTime | Last update timestamp |

---

## JSON Field Formats

### key_informants
```json
[
  {
    "name": "Juan Dela Cruz",
    "background": "Village elder, 75 years old",
    "contact": Optional
  }
]
```

### supporting_docs
```json
["audio", "video", "photos", "writeups"]
```

### works_achievements
```json
[
  {
    "year": 1980,
    "work": "Title or description",
    "award": Optional
  }
]
```
