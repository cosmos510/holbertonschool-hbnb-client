-- Script to recreate the database tables

-- Table `users`
CREATE TABLE users (
    id VARCHAR(256) PRIMARY KEY NOT NULL,
    email VARCHAR(256) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table `reviews`
CREATE TABLE reviews (
    id VARCHAR(256) PRIMARY KEY NOT NULL,
    user_id VARCHAR(256) NOT NULL,
    place_id VARCHAR(50) NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT(500),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id)
);

-- Table `places`
CREATE TABLE places (
    id VARCHAR(256) PRIMARY KEY NOT NULL,
    name VARCHAR(256) NOT NULL,
    description TEXT(1024) NOT NULL,
    address TEXT(256) NOT NULL,
    city_id VARCHAR(256) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    host_id VARCHAR NOT NULL,
    num_rooms INTEGER NOT NULL,
    num_bathrooms INTEGER NOT NULL,
    price_per_night FLOAT NOT NULL,
    max_guests INTEGER NOT NULL,
    amenity_ids VARCHAR(256)  
);

-- Table `countries`
CREATE TABLE countries (
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(30) NOT NULL,
    code VARCHAR(10) NOT NULL
);

-- Table `cities`
CREATE TABLE cities (
    id VARCHAR(256) PRIMARY KEY NOT NULL,
    name VARCHAR(128) NOT NULL,
    country_id VARCHAR(60) NOT NULL,
    uniq_id VARCHAR(60) NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);

-- Table `amenities`
CREATE TABLE amenities (
    id VARCHAR(256) PRIMARY KEY NOT NULL,
    name VARCHAR(128) NOT NULL
);

-- JUNCTION table `place_amenities`
CREATE TABLE place_amenities (
    place_id VARCHAR,
    amenity_id VARCHAR,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);