-- ==========================================
-- SQLite Database
-- Attendance Management System
-- ==========================================

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Sample User (optional)
-- Password: 123456 (replace with a hashed password if you insert manually)

INSERT INTO users (name, mobile, email, password)
VALUES (
    'Test User',
    '9876543210',
    'test@example.com',
    'pbkdf2:sha256:600000$example$examplehashedpassword'
);
