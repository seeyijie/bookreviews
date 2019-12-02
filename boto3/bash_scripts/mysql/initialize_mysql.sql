/*To import data from a csv into MySQL, we first have to select a database.
Then, we have to create a table within that database with a schema of our choosing.
Finally we have to run a command to load the data from our local PC into the table inside our local database*/
use 50043_DB;

/* create a table for storing user data*/
drop table if exists users;
create table users(
    id varchar(100) NOT NULL,
    name varchar(100) NOT NULL,
    email varchar(100) primary key,
    password varchar(100) NOT NULL
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

drop table if exists title;
create table title(
    asin varchar(100) primary key,
    title varchar(1000)
);

load data local infile "/home/ubuntu/bookreviews/data_store/kindle_reviews.csv" into table reviews fields terminated by ',' enclosed by '"' escaped by '"' lines terminated by '\n' ignore 1 rows;
load data local infile "/home/ubuntu/bookreviews/extra_data/kindle_cover_texts.csv" into table title fields terminated by ',' enclosed by '"' escaped by '"' lines terminated by '\n' ignore 1 rows;

update reviews set reviewTime = str_to_date(reviewTime,'%m %d, %Y');