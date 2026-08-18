# Duplicate Import Libraries Report

## Summary

Analysis of the `templates/` folder revealed the following duplicated import libraries. Duplicates are defined as the same library URL being imported in multiple HTML files.

## Duplicated CSS Imports

- **aos.css** (`https://unpkg.com/aos@next/dist/aos.css`)
  - Imported in: `templates/index.html`, `templates/barangays.html`

- **home-heritage.css** (`{{ url_for('static', filename='css/home-heritage.css') }}`)
  - Imported in: `templates/index.html`, `templates/barangays.html`

## Duplicated JS Imports

- **aos.js** (`https://unpkg.com/aos@next/dist/aos.js`)
  - Imported in: `templates/barangays.html`, `templates/index.html`

## Potential Issues

- The Leaflet library is imported with different versions across files:
  - Version 1.7.1 in `templates/barangays.html`
  - Version 1.9.4 in `templates/map.html`
  - This may lead to version conflicts or inconsistent behavior.

No duplicate imports were found within individual files.
## Summary

Analysis of the `templates/` folder revealed the following duplicated import libraries. Duplicates are defined as the same library URL being imported in multiple HTML files.

## Duplicated CSS Imports

- **aos.css** (`https://unpkg.com/aos@next/dist/aos.css`)
  - Imported in: `templates/index.html`, `templates/barangays.html`

- **home-heritage.css** (`{{ url_for('static', filename='css/home-heritage.css') }}`)
  - Imported in: `templates/index.html`, `templates/barangays.html`

## Duplicated JS Imports

- **aos.js** (`https://unpkg.com/aos@next/dist/aos.js`)
  - Imported in: `templates/barangays.html`, `templates/index.html`

## Potential Issues

- The Leaflet library is imported with different versions across files:
  - Version 1.7.1 in `templates/barangays.html`
  - Version 1.9.4 in `templates/map.html`
  - This may lead to version conflicts or inconsistent behavior.

No duplicate imports were found within individual files.
