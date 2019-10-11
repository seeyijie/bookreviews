drop table if exists reviews;

CREATE TABLE reviews(
id integer not null,
asin varchar(100),
helpful varchar(100),
overall integer,
dock_count smallint,
reviewText varchar(255),
reviewTime date,
reviewerID varchar(100),
reviewerName varchar(100),
summary varchar(255),
PRIMARY KEY (id)
);

load data local infile "kindle_reviews.csv" into table reviews fields terminated by ',' enclosed by '"' escaped by '"' lines terminated by '\n' ignore 1 rows;