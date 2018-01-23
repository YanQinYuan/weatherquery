drop table if exists "users";
create table "users" (
  id serial primary key,
  username varchar(64) not null unique,
  password varchar(128) not null
);


drop table if exists history;
create table history (
  id serial primary key,
  user_id integer not null,
  city varchar(64) not null,
  result varchar(256) not null,
  query_time timestamp
);

DROP TABLE if exists "weather";
CREATE TABLE "weather"(
	day varchar(64),
	city varchar(64),
	weather varchar(64),
	temp varchar(64)
	);