drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username char(64) not null unique,
  password char(128) not null
);


drop table if exists history;
create table history (
  id integer primary key autoincrement,
  user_id integer not null,
  city char(64) not null,
  result char(128) not null,
  query_time datetime not null
);
