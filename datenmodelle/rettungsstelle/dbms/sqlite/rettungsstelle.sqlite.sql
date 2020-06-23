--Created from <ent>
create table if not exists mission(
    missionNr    text  not null primary key
,   beginTime    text  not null
,   endTime      text  not null
,   missionPlace text  not null
,   missionDesc  text  not null
,   reportType   text  not null
,   reportTime   text  not null
);

--Created from <ent>
create table if not exists trip(
    licencePlate  text  not null
,   missionNr     text  not null
,   employeeNr    text  not null
,   startAddress  text  not null
,   targetAddress text  not null
,   distance      text  not null
,   beginn        text  not null
,   ends          text  not null
,   missionNr1    text  not null
);

--Created from <ent>
create table if not exists person(
    name     text  not null
,   address  text  not null
,   birthday text  not null
,   gender   text  not null
);

--Created from <ent>
create table if not exists employee(
    employeeNr   text  not null primary key
,   rank         text  not null
,   schooling    text  not null
,   licencePlate text  not null
,   missionNr1   text  not null
);

--Created from <ent>
create table if not exists patient(
    SSN          text  not null primary key
,   KVA          text  not null
,   missionDesc  text  not null
,   licencePlate text  not null
,   missionNr1   text  not null
);

--Created from <ent>
create table if not exists car(
    licencePlate text  not null primary key
,   brand        text  not null
,   model        text  not null
,   equipment    text  not null
,   address      text  not null
);

--Created from <ent>
create table if not exists garage(
    address      text  not null primary key
,   licencePlate text  not null references car (licencePlate)
,   carNr        text  not null
);

--Created from a m:n relation
create table if not exists joins(
    employee_employeeNr text  not null primary key references employee (employeeNr)
);

