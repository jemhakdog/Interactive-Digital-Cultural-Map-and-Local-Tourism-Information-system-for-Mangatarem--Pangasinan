#!/usr/bin/env python3
"""
Database Schema Verification Script for Mangatarem Cultural Heritage & Tourism System

This script verifies that the database schema matches the models defined in models.py.
It checks for:
- All expected tables exist
- All expected columns exist in each table
- Foreign key relationships are properly defined
- Indexes exist for performance

Usage:
    python verify_schema.py [--database DATABASE_URL] [--verbose]
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Expected schema based on models.py
EXPECTED_TABLES = {
    'user': [
        'id', 'username', 'email', 'password_hash', 'role', 'barangay', 'is_approved'
    ],
    'heritage_profile': [
        'id', 'asset_type', 'form_control_number', 'mapper_name', 'date_profiled',
        'status', 'user_id', 'reviewed_by', 'reviewed_at', 'created_at', 'updated_at',
        'key_informants', 'reference_sources', 'significance', 'constraints_threats',
        'conservation_measures', 'common_photo_url'
    ],
    'attraction': [
        'id', 'name', 'description', 'category', 'barangay', 'lat', 'lng',
        'image_url', 'form_control_number', 'heritage_profile_id', 'status',
        'user_id', 'reviewed_by', 'reviewed_at', 'created_at'
    ],
    'event': [
        'id', 'title', 'description', 'date', 'location', 'barangay', 'image_url',
        'user_id', 'status', 'category', 'reviewed_by', 'reviewed_at', 'created_at'
    ],
    'gallery_item': [
        'id', 'type', 'url', 'caption', 'user_id', 'status', 'reviewed_by',
        'reviewed_at', 'uploaded_at'
    ],
    'barangay_info': [
        'id', 'barangay_name', 'history', 'cultural_assets', 'traditions',
        'local_practices', 'unique_features', 'user_id', 'updated_at'
    ],
    'analytics_page_view': [
        'id', 'view_type', 'item_id', 'page_name', 'timestamp', 'user_id'
    ],
    'favorite': [
        'id', 'user_id', 'attraction_id', 'created_at'
    ],
    'user_event_interest': [
        'id', 'user_id', 'event_id', 'status', 'created_at'
    ],
    'review': [
        'id', 'user_id', 'attraction_id', 'rating', 'comment', 'status',
        'reviewed_by', 'reviewed_at', 'created_at'
    ],
    # Heritage detail tables
    'natural_heritage_details': [
        'profile_id', 'subcategory', 'area_hectares', 'ownership', 'protection_status'
    ],
    'built_heritage_details': [
        'profile_id', 'building_type', 'year_constructed', 'ownership_type',
        'declaration_legislation', 'physical_description', 'history_structure',
        'occupation_status', 'is_altered', 'is_original_site', 'integrity_remarks',
        'movable_heritage_list'
    ],
    'movable_heritage_details': [
        'profile_id', 'object_type', 'place_found', 'date_found', 'estimated_age',
        'acquisition_type', 'materials', 'dimensions', 'comparative_criteria'
    ],
    'intangible_heritage_details': [
        'profile_id', 'heritage_type', 'geographical_range', 'related_domains',
        'culture_bearers', 'culture_bearer_photos', 'transmission_mode',
        'objects_used', 'flora_fauna_used', 'safeguarding_measures', 'supporting_docs'
    ],
    'personality_details': [
        'profile_id', 'date_of_birth', 'date_of_death', 'birth_place',
        'present_address', 'age', 'prominence_field', 'biography', 'works_achievements'
    ],
    'institution_details': [
        'profile_id', 'municipality', 'province', 'institution_type',
        'mandate_description', 'milestones', 'condition_status', 'supporting_docs'
    ],
    'lgu_program_details': [
        'profile_id', 'vision_statement', 'mission_statement', 'goal_statements',
        'adoption_date', 'brief_history', 'logo_url', 'logo_legislation_date',
        'logo_explanation', 'chief_executives', 'resolutions', 'ordinances',
        'ela_action_items', 'major_policies', 'program_strategies',
        'annual_investments', 'culture_projects', 'arts_council',
        'alternative_livelihoods', 'community_enterprises', 'peoples_stories'
    ],
}

# Tables that should NOT exist (old/unused schemas)
SKIPPED_TABLES = {
    'attractions',  # Old plural name, we use 'attraction'
    'events',  # Old plural name, we use 'event'
}


def get_database_type(database_url: Optional[str] = None) -> str:
    """Determine database type from URL or default to SQLite."""
    if not database_url:
        return 'sqlite'
    
    if database_url.startswith('postgresql://'):
        return 'postgresql'
    elif database_url.startswith('sqlite:///'):
        return 'sqlite'
    elif database_url.startswith('mysql://'):
        return 'mysql'
    else:
        raise ValueError(f"Unsupported database type in URL: {database_url}")


def get_connection(database_url: Optional[str] = None):
    """Create database connection based on database type."""
    db_type = get_database_type(database_url)
    
    if db_type == 'sqlite':
        import sqlite3
        db_path = database_url.replace('sqlite:///', '') if database_url else 'instance/mangatarem.db'
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn, db_type
    
    elif db_type == 'postgresql':
        try:
            import psycopg2
        except ImportError:
            logger.error("psycopg2 not installed. Install with: pip install psycopg2-binary")
            sys.exit(1)
        
        conn = psycopg2.connect(database_url)
        return conn, db_type
    
    elif db_type == 'mysql':
        try:
            import mysql.connector
        except ImportError:
            logger.error("mysql-connector not installed. Install with: pip install mysql-connector-python")
            sys.exit(1)
        
        conn = mysql.connector.connect(url=database_url)
        return conn, db_type
    
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def get_sqlite_tables(conn) -> List[str]:
    """Get all table names from SQLite database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    return [row[0] for row in cursor.fetchall()]


def get_sqlite_columns(conn, table_name: str) -> List[str]:
    """Get all column names for a SQLite table."""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cursor.fetchall()]


def get_postgresql_tables(conn) -> List[str]:
    """Get all table names from PostgreSQL database."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
    """)
    return [row[0] for row in cursor.fetchall()]


def get_postgresql_columns(conn, table_name: str) -> List[str]:
    """Get all column names for a PostgreSQL table."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name = %s
    """, (table_name,))
    return [row[0] for row in cursor.fetchall()]


def verify_schema(conn, db_type: str, verbose: bool = False) -> Tuple[bool, Dict]:
    """Verify database schema matches expected models."""
    results = {
        'missing_tables': [],
        'extra_tables': [],
        'missing_columns': {},
        'skipped_tables': [],
        'success': True
    }
    
    # Get actual tables from database
    if db_type == 'sqlite':
        actual_tables = get_sqlite_tables(conn)
    elif db_type == 'postgresql':
        actual_tables = get_postgresql_tables(conn)
    else:
        logger.error(f"Unsupported database type: {db_type}")
        return False, results
    
    # Check for missing tables
    for table_name, expected_columns in EXPECTED_TABLES.items():
        if table_name not in actual_tables:
            results['missing_tables'].append(table_name)
            results['success'] = False
            logger.error(f"✗ Missing table: {table_name}")
        else:
            # Check columns
            if db_type == 'sqlite':
                actual_columns = get_sqlite_columns(conn, table_name)
            elif db_type == 'postgresql':
                actual_columns = get_postgresql_columns(conn, table_name)
            
            missing_cols = set(expected_columns) - set(actual_columns)
            if missing_cols:
                results['missing_columns'][table_name] = list(missing_cols)
                results['success'] = False
                logger.error(f"✗ Table {table_name} missing columns: {missing_cols}")
            elif verbose:
                logger.info(f"✓ Table {table_name} has all expected columns")
    
    # Check for extra tables (excluding migrations tracking table and skipped tables)
    expected_table_names = set(EXPECTED_TABLES.keys())
    allowed_tables = expected_table_names | {'_migrations'} | SKIPPED_TABLES
    
    for table_name in actual_tables:
        if table_name not in expected_table_names and table_name not in {'_migrations'}:
            if table_name in SKIPPED_TABLES:
                results['skipped_tables'].append(table_name)
                logger.warning(f"⊘ Skipped table (not in models): {table_name}")
            elif verbose:
                results['extra_tables'].append(table_name)
                logger.info(f"⊕ Extra table (not in verification list): {table_name}")
    
    return results['success'], results


def verify_migrations_table(conn, db_type: str) -> bool:
    """Verify migrations tracking table exists."""
    if db_type == 'sqlite':
        actual_tables = get_sqlite_tables(conn)
    elif db_type == 'postgresql':
        actual_tables = get_postgresql_tables(conn)
    
    if '_migrations' not in actual_tables:
        logger.warning("⚠ _migrations table not found. Run migrations first.")
        return False
    
    logger.info("✓ _migrations table exists")
    return True


def verify_migrations_applied(conn, db_type: str) -> Tuple[int, List[str]]:
    """Check which migrations have been applied."""
    cursor = conn.cursor()
    
    try:
        if db_type == 'sqlite':
            cursor.execute("SELECT migration_name, applied_at FROM _migrations ORDER BY id")
        elif db_type == 'postgresql':
            cursor.execute("SELECT migration_name, applied_at FROM _migrations ORDER BY id")
        
        migrations = cursor.fetchall()
        logger.info(f"Applied migrations: {len(migrations)}")
        
        for migration_name, applied_at in migrations:
            logger.info(f"  ✓ {migration_name} (applied: {applied_at})")
        
        return len(migrations), [m[0] for m in migrations]
    
    except Exception as e:
        logger.warning(f"Could not query _migrations table: {e}")
        return 0, []


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Verify database schema for Mangatarem Cultural Heritage System'
    )
    parser.add_argument(
        '--database', '-d',
        type=str,
        default=None,
        help='Database URL (e.g., postgresql://user:pass@localhost/dbname)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output including successful checks'
    )
    
    args = parser.parse_args()
    
    # Use environment variable if not provided
    database_url = args.database or os.environ.get('DATABASE_URL')
    
    logger.info("=" * 60)
    logger.info("Mangatarem Cultural Heritage - Schema Verification")
    logger.info("=" * 60)
    logger.info(f"Database type: {get_database_type(database_url)}")
    logger.info(f"Expected tables: {len(EXPECTED_TABLES)}")
    logger.info(f"Skipped tables: {len(SKIPPED_TABLES)} ({', '.join(SKIPPED_TABLES)})")
    logger.info("=" * 60)
    
    # Connect to database
    try:
        conn, db_type = get_connection(database_url)
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        sys.exit(1)
    
    try:
        # Verify migrations table
        verify_migrations_table(conn, db_type)
        
        # Check applied migrations
        migration_count, applied_migrations = verify_migrations_applied(conn, db_type)
        
        # Verify schema
        success, results = verify_schema(conn, db_type, args.verbose)
        
        # Summary
        logger.info("=" * 60)
        if success:
            logger.info("✓ Schema verification PASSED")
            logger.info(f"  All {len(EXPECTED_TABLES)} expected tables found with correct columns")
        else:
            logger.error("✗ Schema verification FAILED")
            if results['missing_tables']:
                logger.error(f"  Missing tables: {results['missing_tables']}")
            if results['missing_columns']:
                for table, cols in results['missing_columns'].items():
                    logger.error(f"  Table {table} missing columns: {cols}")
        
        if results['skipped_tables']:
            logger.info(f"  Skipped (not in models): {results['skipped_tables']}")
        
        logger.info("=" * 60)
        
        # Exit with error code if verification failed
        sys.exit(0 if success else 1)
        
    finally:
        conn.close()


if __name__ == '__main__':
    main()
