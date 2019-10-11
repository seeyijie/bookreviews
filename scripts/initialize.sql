/*To import data from a csv into MySQL, we first have to select a database.
Then, we have to create a table within that database with a schema of our choosing.
Finally we have to run a command to load the data from our local PC into the table inside our local database*/
use 50043_DB;

/* create a table for importing the data into*/
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

/* imports the csv file into the table. excludes the column names (make sure csv file is in the same directory)*/
load data local infile "kindle_reviews.csv" into table reviews fields terminated by ',' enclosed by '"' escaped by '"' lines terminated by '\n' ignore 1 rows;