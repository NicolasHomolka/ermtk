drop tablespace Rettungsstelle including contents;
create tablespace Rettungsstelle
  datafile 'tbs_Rettungsstelle'
    size 20M reuse;
--Created from <ent>
create table mission
(
    missionNr varchar(400) primary key
,   beginTime varchar(400)
,   endTime varchar(400)
,   missionPlace varchar(400)
,   missionDesc varchar(400)
,   reportType varchar(400)
,   reportTime varchar(400)
)
tablespace Rettungsstelle;

--Created from <ent>
create table trip
(
    licencePlate varchar(400)
,   missionNr varchar(400)
,   employeeNr varchar(400)
,   startAddress varchar(400)
,   targetAddress varchar(400)
,   distance varchar(400)
,   beginn varchar(400)
,   ends varchar(400)
,   missionNr1 varchar(400)
)
tablespace Rettungsstelle;

--Created from <ent>
create table person
(
    name varchar(400)
,   address varchar(400)
,   birthday varchar(400)
,   gender varchar(400)
)
tablespace Rettungsstelle;

--Created from <ent>
create table employee
(
    employeeNr varchar(400) primary key
,   rank varchar(400)
,   schooling varchar(400)
,   licencePlate varchar(400)
,   missionNr1 varchar(400)
)
tablespace Rettungsstelle;

--Created from <ent>
create table patient
(
    SSN varchar(400) primary key
,   KVA varchar(400)
,   missionDesc varchar(400)
,   licencePlate varchar(400)
,   missionNr1 varchar(400)
)
tablespace Rettungsstelle;

--Created from <ent>
create table car
(
    licencePlate varchar(400) primary key
,   brand varchar(400)
,   model varchar(400)
,   equipment varchar(400)
,   address varchar(400)
)
tablespace Rettungsstelle;

--Created from <ent>
create table garage
(
    address varchar(400) primary key
,   licencePlate varchar(400) references car (licencePlate)
,   carNr varchar(400)
)
tablespace Rettungsstelle;

--Created from a m:n relation
create table joins
(
    employee_employeeNr varchar(400) primary key references employee (employeeNr)
)
tablespace Rettungsstelle;

drop table joins;
drop table garage;
drop table car;
drop table patient;
drop table employee;
drop table person;
drop table trip;
drop table mission;
