# Spotify Most Streamed Songs Database Project

## Overview
The **Spotify Most Streamed Songs Database Project** is designed to analyze and explore the most streamed songs on Spotify using a PostgreSQL database. This project involves gathering and cleaning data related to Spotify's music catalog, including information about artists, tracks, and platforms, and organizing the data into a structured schema. The primary goal of the project is to facilitate the querying and analysis of Spotify's most popular music based on streaming metrics.

## Features
- **Database Schema**: A well-defined PostgreSQL schema that includes tables such as `Artist`, `Track`, `Artist_Track`, `Metric`, and `Platform` to store detailed information about music tracks, their performance metrics, and related platforms.
- **Data Cleaning**: Cleaning and preprocessing of raw Spotify data to ensure consistency and reliability for further analysis.
- **SQL Queries**: Performing complex queries to derive insights from the dataset, such as the most-streamed songs, top artists, and performance comparisons across different platforms.
- **Data Analysis**: Statistical analysis of streaming trends, artist popularity, and metrics across different regions and time periods.

## Data Structure
- **Artist**: Contains information about the artists, including name, genre, and country.
- **Track**: Stores track details such as track name, release date, and duration.
- **Artist_Track**: A many-to-many relationship table linking artists with the tracks they've released.
- **Metric**: Stores streaming metrics such as total streams, weekly streams, and engagement data.
- **Platform**: Contains data on different platforms where the songs are streamed, such as Spotify, Apple Music, etc.

## Technologies Used
- **PostgreSQL**: Used for creating and managing the relational database.
- **Python (optional)**: For data cleaning and analysis if needed using libraries like `psycopg2` for database interaction.
- **SQL**: For writing queries to analyze and retrieve data.

## Project Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/bolishakim/Spotify-Most-Streamed-Songs-Database-Project.git
