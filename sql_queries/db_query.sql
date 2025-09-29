-- Create the database
CREATE DATABASE finnhub_data CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE finnhub_data;

-- Table: finnhub_data.stock_quotes
CREATE TABLE finnhub_data.stock_quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    current_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    open_price FLOAT,
    prev_close_price FLOAT,
    INDEX(symbol)
);

-- Table: finnhub_data.company_profiles
CREATE TABLE finnhub_data.company_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(255),
    exchange VARCHAR(50),
    industry VARCHAR(100),
    logo VARCHAR(255),
    data JSON,
    INDEX(symbol)
);

-- Table: finnhub_data.market_news
CREATE TABLE finnhub_data.market_news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20),
    headline VARCHAR(255),
    source VARCHAR(255),
    url VARCHAR(255),
    datetime INT
);

-- Table: finnhub_data.earnings_calendar
CREATE TABLE finnhub_data.earnings_calendar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    date DATE,
    eps_estimate FLOAT,
    eps_actual FLOAT,
    revenue_estimate FLOAT,
    revenue_actual FLOAT,
    data JSON,
    INDEX(symbol)
);

-- Table: finnhub_data.ipo_calendar
CREATE TABLE finnhub_data.ipo_calendar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20),
    company VARCHAR(255),
    date DATE,
    exchange VARCHAR(50),
    price_range VARCHAR(50),
    shares INT,
    expected_amount FLOAT,
    data JSON
);

-- Table: finnhub_data.economic_events
CREATE TABLE finnhub_data.economic_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(100),
    event VARCHAR(255),
    impact VARCHAR(50),
    actual VARCHAR(50),
    forecast VARCHAR(50),
    previous VARCHAR(50),
    date DATE,
    data JSON
);

-- Table: finnhub_data.countries
CREATE TABLE finnhub_data.countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    currency VARCHAR(100),
    timezone VARCHAR(50),
    data JSON
);
