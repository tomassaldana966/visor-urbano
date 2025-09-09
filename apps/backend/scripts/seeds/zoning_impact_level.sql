INSERT INTO zoning_impact_level (id, impact_level, municipality_id, geom)
VALUES (
    1,
    2, 
    19,
    ST_GeomFromText(
        'POLYGON((202000 3520000, 202500 3520000, 202500 3520500, 202000 3520500, 202000 3520000))',
        32613
    )
);