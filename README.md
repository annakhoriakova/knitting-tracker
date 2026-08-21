# Knitting Project Tracker

A Python application with a relational database for tracking knitting projects, patterns, yarn inventory, and needle collections. Designed for knitters who want to organize their projects and analyze their crafting habits.

## Project Structure
```
knitting-tracker/
├── src/                     # Main source code directory
│   ├── __init__.py
│   ├── database.py          # Database connection & setup
│   ├── models.py            # Data classes
│   └── crud.py              # CRUD operations
│
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── test_database.py     # Test database connections
│   ├── test_models.py       # Test data models
│   └── test_crud.py         # Test CRUD operations
│
├── data/                    # Database files
│   └── knitting.db          # SQLite database file
│
├── knitting_schema.sql      # Database schema
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore file
├── README.md                # Project overview
└── main.py                  # Application entry point
```

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
- **YARN**: Manages yarn inventory with brand, colour, and yardage
- **PROJECT**: Main table for project tracking with foreign keys to PATTERN and NEEDLE
- **PROJECT_YARN**: Bridge table linking projects to yarns (many-to-many relationship)

The PROJECT_YARN table is a weak entity with a composite primary key consisting of project_id and yarn_id, ensuring each project-yarn combination is unique.

## Installation

### Prerequisites
- Python 3.8 or higher (recommended for best compatibility)
- pip (Python package manager)

### Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/annakhoriakova/knitting-tracker.git
cd knitting-tracker
```

### 2. Create a virtual environment

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize the database
```bash
# Ensure the schema file is in the root directory
python -c "from src.database import Database; Database()"
```
