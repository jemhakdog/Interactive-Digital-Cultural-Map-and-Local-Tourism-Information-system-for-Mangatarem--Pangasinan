# Scripts Directory

This directory contains utility scripts for development, debugging, and maintenance tasks.

## Available Scripts

### `debug_template.py`
Debugging utility for template rendering issues. Use this to test and troubleshoot Jinja2 template problems.

### `fix_index.py`
Index fixing utility. Repairs and rebuilds database indices if needed.

### `pocketbasesample.py`
Sample script demonstrating PocketBase integration. Reference implementation for PocketBase client usage.

### `seed_events.py`
Database seeding script for events. Populates the database with sample event data for testing and development.

## Usage

Run any script from the project root directory:

```powershell
python scripts/script_name.py
```

Example:
```powershell
python scripts/seed_events.py
```

## Notes

- These scripts are intended for development and maintenance use only
- Do not run in production unless you understand what they do
- Some scripts may modify the database
