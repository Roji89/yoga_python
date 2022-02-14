DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS cours;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE cours (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name varchar NOT NULL,
  Day TEXT NOT NULL
);

insert into user(username,password) values
  ('roja','roja'),
  ('nazila','nazila'),
  ('justin','justin');  

insert into cours
  (Name,Day) values
  ('ashtanga yoga','saturday'),
  ('sivananda yoga','sunday'),
  ('satiaAnnada yoga','monday'),
  ('pranaYama yoga','tuesday'),
  ('Meditation yoga','wendsday');