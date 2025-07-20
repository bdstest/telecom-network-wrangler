-- Initial database schema for network monitoring
CREATE TABLE network_elements (
    id SERIAL PRIMARY KEY,
    element_type VARCHAR(50),
    vendor VARCHAR(50),
    location_lat DECIMAL(10,8),
    location_lon DECIMAL(11,8),
    created_at TIMESTAMP DEFAULT NOW()
);
