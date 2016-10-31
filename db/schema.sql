-- Table emissions: integer id primary key has autoincrement default by sqlite.
-- DROP TABLE IF EXISTS emissions;
CREATE TABLE IF NOT EXISTS emissions (
    id INTEGER PRIMARY KEY,
    vehicleId TEXT NOT NULL,
    vehicleType TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    timestamp REAL NOT NULL,
    heading INTEGER NOT NULL
);