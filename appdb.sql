DROP TABLE posts;
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INT NOT NULL,
    title VARCHAR NOT NULL,
    published_date VARCHAR NOT NULL,
    content TEXT
);

DROP TABLE users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name VARCHAR NOT NULL,
    full_name VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);