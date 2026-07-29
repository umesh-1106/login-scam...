-- ===========================================
-- Create Database
-- ===========================================
CREATE DATABASE IF NOT EXISTS attendance_system;
USE attendance_system;

-- ===========================================
-- Users Table
-- ===========================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- Admin Table
-- ===========================================
CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- ===========================================
-- Default Admin Account
-- Username: admin
-- Password: admin123
-- NOTE: Replace the password hash after creating
-- a secure admin account in production.
-- ===========================================

INSERT INTO admin (username, password)
VALUES (
    'admin',
    'pbkdf2:sha256:600000$example$examplehashedpassword'
)
ON DUPLICATE KEY UPDATE username = username;

-- ===========================================
-- Attendance Table (Optional)
-- ===========================================
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    status ENUM('Present','Absent') DEFAULT 'Present',
    attendance_date DATE NOT NULL,
    attendance_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_attendance_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- ===========================================
-- View Registered Users
-- ===========================================
SELECT * FROM users;

-- ===========================================
-- View Attendance
-- ===========================================
SELECT * FROM attendance;
