-- ============================================================
-- Knitting Project Tracker Database Schema
-- Last Updated: 2026-08-21
-- Author: Anna Khoriakova
-- Description: Schema for tracking knitting projects,
--              patterns, yarns, needles, and project-yarn relationships
-- ============================================================

-- ============================================================
-- TABLES
-- ============================================================

-- ------------------------------------------------------------
-- Table: PATTERN
-- Description: Stores knitting pattern information
-- ------------------------------------------------------------
CREATE TABLE PATTERN (
    pattern_id      INTEGER PRIMARY KEY AUTOINCREMENT,  -- Surrogate PK
    pattern_name    TEXT NOT NULL,                      -- Name of the pattern
    designer        TEXT                                -- Pattern designer
);

-- ------------------------------------------------------------
-- Table: NEEDLE
-- Description: Stores needle information
-- ------------------------------------------------------------
CREATE TABLE NEEDLE (
    needle_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    needle_size_mm   REAL NOT NULL,                    -- Size in millimeters (e.g., 4.0)
    needle_type      TEXT NOT NULL,                    -- Circular, Straight, DPN, Interchangeable
    needle_material  TEXT,                             -- Wood, Metal, Bamboo, Plastic
    needle_length    TEXT,                             -- Length in inches (e.g., "24", "32")
    needle_brand     TEXT                              -- Needle brand (e.g., KnitPro)
);

-- ------------------------------------------------------------
-- Table: YARN
-- Description: Stores yarn information
-- ------------------------------------------------------------
CREATE TABLE YARN (
    yarn_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    yarn_brand       TEXT NOT NULL,                    -- Brand name (e.g., "Malabrigo")
    yarn_line        TEXT,                             -- Line/product name (e.g., "Rios")
    colour_name      TEXT,                             -- Colourway name
    dye_lot          TEXT,                             -- For matching yarn dye lots
    weight_category  TEXT,                             -- DK, Worsted, Fingering, etc.
    total_yardage    INTEGER                           -- Yards per skein
);

-- ------------------------------------------------------------
-- Table: PROJECT
-- Description: Main project tracking table
-- ------------------------------------------------------------
CREATE TABLE PROJECT (
    project_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name    TEXT NOT NULL,                    -- Project name (e.g., "Aran Sweater")
    start_date      TEXT,                             -- ISO date format: YYYY-MM-DD
    end_date        TEXT,                             -- NULL if still in progress
    status          TEXT NOT NULL CHECK (             -- Status with allowed values
        status IN ('Planning', 'WIP', 'Blocking', 'Finished', 'Frogged', 'Abandoned')
    ) DEFAULT 'Planning',
    recipient       TEXT,                             -- Who it's for ("Me", "Gift", etc.)
    
    -- Foreign Keys
    pattern_id      INTEGER NOT NULL,                 -- A project must follow a pattern
    needle_id       INTEGER NOT NULL,                 -- A project must have a primary needle
    
    -- Foreign Key Constraints
    FOREIGN KEY (pattern_id) REFERENCES PATTERN(pattern_id) ON DELETE RESTRICT,
    FOREIGN KEY (needle_id) REFERENCES NEEDLE(needle_id) ON DELETE RESTRICT
);

-- ------------------------------------------------------------
-- Table: PROJECT_YARN (Weak Entity)
-- Description: Links projects to yarns
--              Also tracks how many skeins were used
-- ------------------------------------------------------------
CREATE TABLE PROJECT_YARN (
    project_id      INTEGER NOT NULL,                -- FK to PROJECT (partial PK)
    yarn_id         INTEGER NOT NULL,                -- FK to YARN (partial PK)
    skeins_used     INTEGER DEFAULT 1 CHECK (        -- Number of skeins used in this project
        skeins_used > 0
    ),
    
    -- Composite Primary Key
    PRIMARY KEY (project_id, yarn_id),
    
    -- Foreign Key Constraints
    FOREIGN KEY (project_id) REFERENCES PROJECT(project_id) ON DELETE CASCADE,
    FOREIGN KEY (yarn_id) REFERENCES YARN(yarn_id) ON DELETE RESTRICT
);

-- ============================================================
-- INDEXES (for performance)
-- ============================================================

-- For faster lookups on foreign keys
CREATE INDEX idx_project_pattern_id ON PROJECT(pattern_id);
CREATE INDEX idx_project_needle_id ON PROJECT(needle_id);
CREATE INDEX idx_project_status ON PROJECT(status);          -- For filtering active projects
CREATE INDEX idx_project_yarn_project ON PROJECT_YARN(project_id);
CREATE INDEX idx_project_yarn_yarn ON PROJECT_YARN(yarn_id);
