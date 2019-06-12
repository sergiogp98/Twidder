create table users(
  email varchar(50),
  password varchar(22),
  firstname varchar(10),
  familyname varchar(30),
  gender varchar(6),
  city varchar(20),
  country varchar(20),
  primary key(email)
);

create table loggued(
  email varchar(50),
  token varchar(30),
  primary key(email)
);

create table messages(
  id integer primary key autoincrement,
  email_sender varchar(50),
  message varchar(240),
  email_receiver varchar(50)
);
