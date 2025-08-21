<?php
$db = new SQLite3('app.db');

$db->exec('CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, 
    email TEXT, 
    display_name TEXT, 
    age INTEGER, 
    location TEXT, 
    bio TEXT, 
    newsletter TEXT,
    category TEXT
)');

$db->exec('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)');

$db->exec('CREATE TABLE IF NOT EXISTS important (id INTEGER PRIMARY KEY, name TEXT, memo TEXT)');

$db->exec("INSERT OR REPLACE INTO users (id, email, display_name, age, location, bio, newsletter, category) VALUES 
    (1, 'user@example.com', 'user', 25, 'San Francisco', 'Just a regular user', 'weekly', 'popular')");

$db->exec("INSERT OR IGNORE INTO products (name, category, price) VALUES 
    ('Phone', 'electronics', 999.99),
    ('Laptop', 'electronics', 1299.99),
    ('Headphones', 'electronics', 199.99),
    ('T-Shirt', 'clothing', 29.99),
    ('Jeans', 'clothing', 79.99),
    ('Sneakers', 'clothing', 129.99)");

$db->exec("INSERT OR IGNORE INTO important (name, memo) VALUES 
    ('flag', 'grey{zammy_zamn_zamnnnnnnnnnnnnnnnnnnnnnnnnnnnn}')");

$db->close();
?>