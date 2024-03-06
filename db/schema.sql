-- CREATE DATABASE sudoku;
USE sudoku;

DROP TABLE IF EXISTS leaderboard;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(162) NOT NULL
);

CREATE TABLE leaderboard (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    score INT NOT NULL
    -- FOREIGN KEY (user_id) REFERENCES users(id)
);