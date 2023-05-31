CREATE TABLE users
(user_id SERIAL PRIMARY KEY,
login VARCHAR(100) UNIQUE,
password  VARCHAR(100) UNIQUE) ;

CREATE TABLE movies
(movie_id SERIAL PRIMARY KEY,
name VARCHAR(100),
date_added  DATE DEFAULT CURRENT_DATE,
extenxion VARCHAR(10) NOT NULL,
url VARCHAR(250),
user_id INT,
CONSTRAINT fk_user
    FOREIGN KEY(user_id) 
	REFERENCES users(user_id));

CREATE TABLE movies_with_detection
(movie_id SERIAL PRIMARY KEY,
name VARCHAR(100),
date_added  DATE DEFAULT CURRENT_DATE,
extenxion VARCHAR(10) NOT NULL,
url VARCHAR(250),
annotations VARCHAR(10000),
source_movie_id INT,
CONSTRAINT fk_source_movie
    FOREIGN KEY(source_movie_id) 
	REFERENCES movies(movie_id));
