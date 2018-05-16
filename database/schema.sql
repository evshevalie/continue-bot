CREATE TABLE users_banned (
  id INT PRIMARY KEY NOT NULL
);

CREATE TABLE users_kicked (
  id INT PRIMARY KEY NOT NULL,
  unkick_time TEXT NOT NULL
);

CREATE TABLE admins (
  id INT PRIMARY KEY NOT NULL
);
