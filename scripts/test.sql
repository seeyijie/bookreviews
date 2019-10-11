use 50043_DB;
drop table if exists Regist;
create TABLE Regist (
    UserID integer unique,
    Car varchar(100) unique,
    primary key (UserID, Car)
);


