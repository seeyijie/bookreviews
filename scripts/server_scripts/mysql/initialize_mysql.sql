/*To import data from a csv into MySQL, we first have to select a database.
Then, we have to create a table within that database with a schema of our choosing.
Finally we have to run a command to load the data from our local PC into the table inside our local database*/
use 50043_DB;

/* create a table for storing user data*/
drop table if exists users;
create table users(
    id integer primary key,
    name varchar(100),
    email varchar(100),
    password varchar(100),
    recent_login datetime
);

/* create a table for importing the data into*/
drop table if exists reviews;
create table reviews(
id integer not null auto_increment primary key,
asin varchar(100),
helpful varchar(100),
overall integer,
reviewText varchar(255),
reviewTime varchar(255),
reviewerID varchar(100),
reviewerName varchar(100),
summary varchar(255),
unixReviewTime integer
);


load data local infile "/home/ubuntu/data_store/kindle_reviews.csv" into table reviews fields terminated by ',' enclosed by '"' escaped by '"' lines terminated by '\n' ignore 1 rows;

drop table if exists title;
create table title select asin, title from reviews;

update reviews set reviewTime = str_to_date(reviewTime,'%m %d, %Y');