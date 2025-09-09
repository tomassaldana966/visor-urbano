-- Seed data for procedure_registrations table

-- Record 1: Minimal data (only area and other required fields or fields with defaults)
INSERT INTO procedure_registrations (reference, area, business_sector, procedure_type, procedure_origin, historical_id, bbox, geom, municipality_id)
VALUES (
    'REF-001', -- reference
    120.5,  -- area
    'Retail', -- business_sector
    'New License', -- procedure_type
    'Online', -- procedure_origin
    NULL, -- historical_id
    NULL, -- bbox
    NULL,   -- geom (GeoJSON string)
    1 -- municipality_id (assuming a municipality with id 1 exists)
);

-- Record 2: All fields populated
INSERT INTO procedure_registrations (reference, area, business_sector, procedure_type, procedure_origin, historical_id, bbox, geom, municipality_id)
VALUES (
    'REF-002', -- reference
    250.75, -- area
    'Restaurant', -- business_sector
    'Renewal', -- procedure_type
    'Counter', -- procedure_origin
    101, -- historical_id
    '-106.15,28.55,-105.95,28.75', -- Example bbox for Chihuahua area
    ST_Transform(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-106.15, 28.55], [-105.95, 28.55], [-105.95, 28.75], [-106.15, 28.75], [-106.15, 28.55]]]}'), 32613), -- Transform from WGS84 (4326) to UTM Zone 13N (32613)
    1 -- municipality_id (assuming 1 is Chihuahua)
);

-- Record 3: For testing updates
INSERT INTO procedure_registrations (reference, area, business_sector, procedure_type, procedure_origin, historical_id, bbox, geom, municipality_id)
VALUES (
    'REF-003', -- reference
    85.0,   -- area
    'Services', -- business_sector
    'Permit', -- procedure_type
    'Online', -- procedure_origin
    NULL, -- historical_id
    NULL, -- bbox
    NULL,   -- geom (GeoJSON string) - to be updated
    2 -- municipality_id (assuming a municipality with id 2 exists)
);

-- Record 4: With specific geometry for geometry endpoint testing
INSERT INTO procedure_registrations (reference, area, business_sector, procedure_type, procedure_origin, historical_id, bbox, geom, municipality_id)
VALUES (
    'REF-004', -- reference
    300.0,  -- area
    'Industrial', -- business_sector
    'New License', -- procedure_type
    'Counter', -- procedure_origin
    102, -- historical_id
    '-106.08,28.62,-106.06,28.64', -- bbox updated for Chihuahua coordinates
    ST_Transform(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-106.08, 28.62], [-106.06, 28.62], [-106.06, 28.64], [-106.08, 28.64], [-106.08, 28.62]]]}'), 32613), -- Transform small Polygon in Chihuahua from WGS84 to UTM Zone 13N
    1 -- municipality_id (assuming 1 is Chihuahua)
);

-- Record 5: Another record for general listing and pagination tests
INSERT INTO procedure_registrations (reference, area, business_sector, procedure_type, procedure_origin, historical_id, bbox, geom, municipality_id)
VALUES (
    'REF-005', -- reference
    175.0,  -- area
    'Office', -- business_sector
    'Modification', -- procedure_type
    'Online', -- procedure_origin
    NULL, -- historical_id
    NULL, -- bbox
    NULL,   -- geom (GeoJSON string)
    2 -- municipality_id
);

-- Record 6: For testing filtering by municipality_id
INSERT INTO procedure_registrations (reference, area, business_sector, procedure_type, procedure_origin, historical_id, bbox, geom, municipality_id)
VALUES (
    'REF-006', -- reference
    50.25,  -- area
    'Retail', -- business_sector
    'New License', -- procedure_type
    'Counter', -- procedure_origin
    103, -- historical_id
    NULL, -- bbox
    NULL,   -- geom (GeoJSON string)
    3 -- municipality_id (assuming a municipality with id 3 exists)
);
