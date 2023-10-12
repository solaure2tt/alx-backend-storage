-- SQL script that creates a table users
-- id, integer, never null, auto increment and primary key
-- email, string (255 characters), never null and unique
-- name, string (255 characters)
CREATE TABLE IF NOT EXISTS users(
	id int NOT NULL AUTO_INCREMENT,
	email varchar(255) NOT NULL UNIQUE,
	name varchar(255),
	PRIMARY KEY(id)
);

