-- Drop tables if they exist
DROP TABLE IF EXISTS Platform;
DROP TABLE IF EXISTS Metric;
DROP TABLE IF EXISTS Artist_Track;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Artist;

-- Create Artist Table
CREATE TABLE Artist (
    Artist_ID VARCHAR(100) PRIMARY KEY,
    Artist_Name VARCHAR(255) NOT NULL
);

-- Create Track Table
CREATE TABLE Track (
    Track_ID VARCHAR(100) PRIMARY KEY,
    Track_Name VARCHAR(255) NOT NULL,
    Streams BIGINT,
    Released_Day INT,
    Released_Month INT,
    Released_Year INT,
    Cover_URL VARCHAR(255)
);

-- Create Artist-Track Table (Many-to-Many Relationship)
CREATE TABLE Artist_Track (
    Artist_ID VARCHAR(100),
    Track_ID VARCHAR(100),
    PRIMARY KEY (Artist_ID, Track_ID),
    FOREIGN KEY (Artist_ID) REFERENCES Artist(Artist_ID),
    FOREIGN KEY (Track_ID) REFERENCES Track(Track_ID)
);

-- Create Metric Table with relationship to Track
CREATE TABLE Metric (
    Metric_ID VARCHAR(100) PRIMARY KEY,
    Track_ID VARCHAR(100),
    Danceability_Percent FLOAT,
    Valence_Percent FLOAT,
    Energy_Percent FLOAT,
    Acousticness_Percent FLOAT,
    Instrumentalness_Percent FLOAT,
    Liveness_Percent FLOAT,
    Speechiness_Percent FLOAT,
    BPM INT,
    Mode VARCHAR(10),
    FOREIGN KEY (Track_ID) REFERENCES Track(Track_ID)
);

-- Create Platform Table
CREATE TABLE Platform (
    Platform_ID VARCHAR(100) PRIMARY KEY,
    Track_ID VARCHAR(100),
    Platform_Name VARCHAR(50) NOT NULL,
    In_Playlists INT,
    In_Charts INT,
    FOREIGN KEY (Track_ID) REFERENCES Track(Track_ID)
);


-- Copy Artist Table
COPY artist 
FROM '/Users/Desktop/Databases Tables/artist_table.csv' 
CSV HEADER DELIMITER ',';

-- Copy Track Table
COPY track  
FROM '/Users/Desktop/Databases Tables/track_table.csv' 
CSV HEADER DELIMITER ',';

-- Copy Artist-Track Table
COPY Artist_Track  
FROM '/Users/Desktop/Databases Tables/artist_track_table.csv' 
CSV HEADER DELIMITER ',';

-- Copy Mertic Table
COPY metric
FROM '/Users/Desktop/Databases Tables/metric_table.csv' 
CSV HEADER DELIMITER ',';

-- Copy Platform Table
COPY platform
FROM '/Users/Desktop/Databases Tables/platform_table.csv' 
CSV HEADER DELIMITER ',';