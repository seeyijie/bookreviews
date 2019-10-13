drop table if exists review;

create table review(
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

load data local infile "kindle_reviews.csv" into table review fields terminated by ',' enclosed by '"' escaped by '"' lines terminated by '\n' ignore 1 rows;


 update review set reviewTime = str_to_date(reviewTime,'%m %d, %Y');        