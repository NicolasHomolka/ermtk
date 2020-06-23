drop table if exists joins;
drop table if exists garage;
drop table if exists car;
drop table if exists patient;
drop table if exists employee;
drop table if exists person;
drop table if exists trip;
drop table if exists mission;

#Created from <ent>
create table mission(
    missionNr    varchar(132)  not null primary key
,   beginTime    varchar(132)  not null
,   endTime      varchar(132)  not null
,   missionPlace varchar(132)  not null
,   missionDesc  varchar(132)  not null
,   reportType   varchar(132)  not null
,   reportTime   varchar(132)  not null
);

#Created from <ent>
create table trip(
    licencePlate  varchar(132)  not null
,   missionNr     varchar(132)  not null
,   employeeNr    varchar(132)  not null
,   startAddress  varchar(132)  not null
,   targetAddress varchar(132)  not null
,   distance      varchar(132)  not null
,   beginn        varchar(132)  not null
,   ends          varchar(132)  not null
,   missionNr1    varchar(132)  not null
);

#Created from <ent>
create table person(
    name     varchar(132)  not null
,   address  varchar(132)  not null
,   birthday varchar(132)  not null
,   gender   varchar(132)  not null
);

#Created from <ent>
create table employee(
    employeeNr   varchar(132)  not null primary key
,   rank         varchar(132)  not null
,   schooling    varchar(132)  not null
,   licencePlate varchar(132)  not null
,   missionNr1   varchar(132)  not null
);

#Created from <ent>
create table patient(
    SSN          varchar(132)  not null primary key
,   KVA          varchar(132)  not null
,   missionDesc  varchar(132)  not null
,   licencePlate varchar(132)  not null
,   missionNr1   varchar(132)  not null
);

#Created from <ent>
create table car(
    licencePlate varchar(132)  not null primary key
,   brand        varchar(132)  not null
,   model        varchar(132)  not null
,   equipment    varchar(132)  not null
,   address      varchar(132)  not null
);

#Created from <ent>
create table garage(
    address      varchar(132)  not null primary key
,   licencePlate varchar(132)  not null references car (licencePlate)
,   carNr        varchar(132)  not null
);

#Created from a m:n relation
create table joins(
    employee_employeeNr varchar(132)  not null primary key references employee (employeeNr)
);

