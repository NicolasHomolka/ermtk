--Created from <ent>
create table mission
(
    missionNr varchar(300) primary key
,   beginTime varchar(300)
,   endTime varchar(300)
,   missionPlace varchar(300)
,   missionDesc varchar(300)
,   reportType varchar(300)
,   reportTime varchar(300)
);

--Created from <ent>
create table trip
(
    licencePlate varchar(300)
,   missionNr varchar(300)
,   employeeNr varchar(300)
,   startAddress varchar(300)
,   targetAddress varchar(300)
,   distance varchar(300)
,   beginn varchar(300)
,   ends varchar(300)
,   missionNr1 varchar(300)
);

--Created from <ent>
create table person
(
    name varchar(300)
,   address varchar(300)
,   birthday varchar(300)
,   gender varchar(300)
);

--Created from <ent>
create table employee
(
    employeeNr varchar(300) primary key
,   rank varchar(300)
,   schooling varchar(300)
,   licencePlate varchar(300)
,   missionNr1 varchar(300)
);

--Created from <ent>
create table patient
(
    SSN varchar(300) primary key
,   KVA varchar(300)
,   missionDesc varchar(300)
,   licencePlate varchar(300)
,   missionNr1 varchar(300)
);

--Created from <ent>
create table car
(
    licencePlate varchar(300) primary key
,   brand varchar(300)
,   model varchar(300)
,   equipment varchar(300)
,   address varchar(300)
);

--Created from <ent>
create table garage
(
    address varchar(300) primary key
,   licencePlate varchar(300) references car (licencePlate)
,   carNr varchar(300)
);

--Created from a m:n relation
create table joins
(
    employee_employeeNr varchar(300) primary key references employee (employeeNr)
);

drop table if exists joins;
drop table if exists garage;
drop table if exists car;
drop table if exists patient;
drop table if exists employee;
drop table if exists person;
drop table if exists trip;
drop table if exists mission;
