# Knitting Project Tracker

A SQL database schema for tracking knitting projects, patterns, yarn inventory, and needle collections. Designed for knitters who want to organize their projects and analyze their crafting habits.

## Features

- Track projects with start/end dates and status (Planning, WIP, Blocking, Finished, Frogged, Abandoned)
- Store pattern information including designer
- Manage yarn inventory with brand, colour, weight, and yardage
- Catalog needle collections with size, type, material, and length
- Link multiple yarns to a single project with skein usage tracking

## Database Schema

The database consists of five tables:

- **PATTERN**: Stores knitting pattern information
- **NEEDLE**: Tracks needle tools with size, type, and material
- **YARN**: Manages yarn inventory with brand, color, and yardage
- **PROJECT**: Main table for project tracking with foreign keys to PATTERN and NEEDLE
- **PROJECT_YARN**: Bridge table linking projects to yarns (many-to-many relationship)

The PROJECT_YARN table is a weak entity with a composite primary key consisting of project_id and yarn_id, ensuring each project-yarn combination is unique.
