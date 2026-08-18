#!/usr/bin/env python3
"""
Database Migration Runner for Mangatarem Cultural Heritage & Tourism System

This script executes SQL migration files against the configured database.
Supports both SQLite (local development) and PostgreSQL/Supabase (production).

Usage:
    python run_migrations.py [--database DATABASE_URL] [--dry-run]

Examples:
    # Run with SQLite (default)
    python run_migrations.py

    # Run with PostgreSQL
    python run_migrations.py --database postgresql://user:pass@localhost/dbname

    # Dry run (show what would be executed)
    python run_migrations.py --dry-run
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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
        # Use instance database or default
        db_path = database_url.replace('sqlite:///', '') if database_url else 'instance/mangatarem.db'
        # Create directory if it doesn't exist
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        logger.info(f"Connected to SQLite database: {db_path}")
        return conn
    
    elif db_type == 'postgresql':
        try:
            import psycopg2
        except ImportError:
            logger.error("psycopg2 not installed. Install with: pip install psycopg2-binary")
            sys.exit(1)
        
        conn = psycopg2.connect(database_url)
        logger.info("Connected to PostgreSQL database")
        return conn
    
    elif db_type == 'mysql':
        try:
            import mysql.connector
        except ImportError:
            logger.error("mysql-connector not installed. Install with: pip install mysql-connector-python")
            sys.exit(1)
        
        conn = mysql.connector.connect(url=database_url)
        logger.info("Connected to MySQL database")
        return conn
    
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def get_migration_files(migrations_dir: Path, db_type: str) -> List[Path]:
    """Get all SQL migration files sorted by name, filtered by database type."""
    if not migrations_dir.exists():
        logger.error(f"Migrations directory not found: {migrations_dir}")
        sys.exit(1)
    
    all_migration_files = sorted(migrations_dir.glob('*.sql'))
    
    # Filter migration files by database type
    migration_files = []
    for f in all_migration_files:
        filename = f.name
        # Skip files that are explicitly for a different database type
        if db_type == 'sqlite' and ('postgresql' in filename or 'supabase' in filename):
            continue
        if db_type == 'postgresql' and 'sqlite' in filename:
            continue
        
        migration_files.append(f)
    
    logger.info(f"Found {len(migration_files)} migration file(s) for {db_type}")
    return migration_files


def create_migrations_table(conn, db_type: str) -> None:
    """Create migrations tracking table if it doesn't exist."""
    cursor = conn.cursor()
    
    if db_type == 'sqlite':
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS _migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_name VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    elif db_type == 'postgresql':
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS _migrations (
                id SERIAL PRIMARY KEY,
                migration_name VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT NOW()
            )
        """)
    elif db_type == 'mysql':
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS _migrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                migration_name VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    conn.commit()
    logger.info("Ensured _migrations table exists")


def get_applied_migrations(conn) -> List[str]:
    """Get list of already applied migrations."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT migration_name FROM _migrations ORDER BY id")
        return [row[0] for row in cursor.fetchall()]
    except Exception:
        # Table might not exist yet
        return []


def mark_migration_applied(conn, migration_name: str, db_type: str) -> None:
    """Mark a migration as applied in the database."""
    cursor = conn.cursor()
    
    if db_type == 'sqlite':
        cursor.execute(
            "INSERT INTO _migrations (migration_name) VALUES (?)",
            (migration_name,)
        )
    elif db_type == 'postgresql':
        cursor.execute(
            "INSERT INTO _migrations (migration_name) VALUES (%s)",
            (migration_name,)
        )
    elif db_type == 'mysql':
        cursor.execute(
            "INSERT INTO _migrations (migration_name) VALUES (%s)",
            (migration_name,)
        )
    
    conn.commit()


def execute_migration(conn, migration_file: Path, dry_run: bool = False) -> bool:
    """Execute a single migration file."""
    logger.info(f"Executing migration: {migration_file.name}")
    
    # Read migration file
    with open(migration_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    if dry_run:
        logger.info(f"[DRY RUN] Would execute {len(sql_content)} bytes of SQL")
        return True
    
    # Execute migration
    cursor = conn.cursor()
    
    try:
        # Execute all statements in the migration file
        # Note: For SQLite, we use executescript which handles multiple statements
        # For PostgreSQL/MySQL, we need to split by semicolon
        db_type = get_database_type()
        
        if db_type == 'sqlite':
            cursor.executescript(sql_content)
        else:
            # Split by semicolon but handle edge cases
            statements = [s.strip() for s in sql_content.split(';') if s.strip()]
            for statement in statements:
                if not statement.startswith('--'):  # Skip pure comment lines
                    cursor.execute(statement)
        
        conn.commit()
        logger.info(f"✓ Successfully executed: {migration_file.name}")
        return True
        
    except Exception as e:
        conn.rollback()
        logger.error(f"✗ Failed to execute {migration_file.name}: {str(e)}")
        return False


def run_migrations(database_url: Optional[str] = None, dry_run: bool = False) -> Tuple[int, int]:
    """Run all pending migrations."""
    db_type = get_database_type(database_url)
    
    # Determine migrations directory
    migrations_dir = Path(__file__).parent / 'migrations'
    
    # Get all migration files (filtered by database type)
    migration_files = get_migration_files(migrations_dir, db_type)
    
    if not migration_files:
        logger.warning("No migration files found!")
        return 0, 0
    
    # Connect to database
    conn = get_connection(database_url)
    
    try:
        # Create migrations tracking table
        create_migrations_table(conn, db_type)
        
        # Get already applied migrations
        applied = get_applied_migrations(conn)
        logger.info(f"Already applied: {len(applied)} migration(s)")
        
        # Filter pending migrations
        pending = [f for f in migration_files if f.name not in applied]
        logger.info(f"Pending migrations: {len(pending)}")
        
        if not pending:
            logger.info("Database is up to date!")
            return 0, 0
        
        # Execute pending migrations
        success_count = 0
        failed_count = 0
        
        for migration_file in pending:
            success = execute_migration(conn, migration_file, dry_run)
            
            if success:
                success_count += 1
                if not dry_run:
                    mark_migration_applied(conn, migration_file.name, db_type)
            else:
                failed_count += 1
                logger.error("Migration failed! Stopping execution.")
                break
        
        # Summary
        logger.info("=" * 60)
        if dry_run:
            logger.info(f"[DRY RUN] Would apply {success_count} migration(s)")
        else:
            logger.info(f"Applied {success_count} migration(s) successfully")
            if failed_count > 0:
                logger.warning(f"Failed: {failed_count} migration(s)")
        
        return success_count, failed_count
        
    finally:
        conn.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Run database migrations for Mangatarem Cultural Heritage System'
    )
    parser.add_argument(
        '--database', '-d',
        type=str,
        default=None,
        help='Database URL (e.g., postgresql://user:pass@localhost/dbname)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be executed without applying changes'
    )
    
    args = parser.parse_args()
    
    # Use environment variable if not provided
    database_url = args.database or os.environ.get('DATABASE_URL')
    
    logger.info("=" * 60)
    logger.info("Mangatarem Cultural Heritage - Database Migration Runner")
    logger.info("=" * 60)
    logger.info(f"Database type: {get_database_type(database_url)}")
    logger.info(f"Dry run: {args.dry_run}")
    logger.info("=" * 60)
    
    success, failed = run_migrations(database_url, args.dry_run)
    
    # Exit with error code if any migrations failed
    if failed > 0:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
