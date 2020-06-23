//Database Rettungsstelle

//Created from <ent>
var mission real relation
{
    missionNr char
,   beginTime char
,   endTime char
,   missionPlace char
,   missionDesc char
,   reportType char
,   reportTime char
} key{missionNr};

//Created from <ent>
var trip real relation
{
    licencePlate char
,   missionNr char
,   employeeNr char
,   startAddress char
,   targetAddress char
,   distance char
,   beginn char
,   ends char
,   missionNr1 char
}key{};

//Created from <ent>
var person real relation
{
    name char
,   address char
,   birthday char
,   gender char
}key{};

//Created from <ent>
var employee real relation
{
    employeeNr char
,   rank char
,   schooling char
,   licencePlate char
,   missionNr1 char
} key{employeeNr};

//Created from <ent>
var patient real relation
{
    SSN char
,   KVA char
,   missionDesc char
,   licencePlate char
,   missionNr1 char
} key{SSN};

//Created from <ent>
var car real relation
{
    licencePlate char
,   brand char
,   model char
,   equipment char
,   address char
} key{licencePlate};

//Created from <ent>
var garage real relation
{
    address char
,   licencePlate char
,   carNr char
} key{address};

constraint fk_garage_car_on_licencePlate garage{licencePlate} <= car {licencePlate};

//Created from a m:n relation
var joins real relation
{
    employee_employeeNr char
} key{employee_employeeNr};

constraint fk_joins_employee_on_employee_employeeNr (joins rename {employee_employeeNr as employeeNr}) {employeeNr} <= employee {employeeNr};

