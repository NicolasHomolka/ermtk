--Created from <ent>
create table BoardKarte
(
    fnr varchar(300) primary key
,   datum varchar(300)
,   abflughafen varchar(300)
,   ankunftsflughafen varchar(300)
,   name varchar(300)
,   sitz varchar(300)
);

--Created from <ent>
create table Passagier
(
    fnr varchar(300) references BoardKarte (fnr)
,   pnr varchar(300)
,   name varchar(300)
,   anrede varchar(300)
,   titel varchar(300)
,   primary key(fnr,pnr)
);

--Created from <ent>
create table Ticket
(
    fnr varchar(300)
,   pnr varchar(300)
,   tnr varchar(300)
,   ausgabedatum varchar(300)
,   preis varchar(300)
,   waehrung varchar(300)
,   vertriebsbuero varchar(300)
,   primary key(fnr,pnr,tnr)
,   foreign key(fnr, pnr) references Passagier(fnr,pnr)
);

--Created from <ent>
create table Flugzeugtyp
(
    typidentifikation varchar(300) primary key
,   hersteller varchar(300)
,   reichweite varchar(300)
);

--Created from <ent>
create table Flugzeug
(
    flugzeugnummer varchar(300)
,   interregnummer varchar(300)
,   name varchar(300)
,   startDatum varchar(300)
,   primary key(flugzeugnummer,interregnummer)
);

--Created from <ent>
create table Fluggesellschaft
(
    orgCode varchar(300) primary key
,   name varchar(300)
,   hauptsitz varchar(300)
);

--Created from <ent>
create table Flughafen
(
    flughafennr varchar(300) primary key
,   name varchar(300)
,   stadt varchar(300)
,   land varchar(300)
,   kapazitaet varchar(300)
);

--Created from a m:n relation
create table Sitzplatz
(
    BoardKarte_fnr varchar(300) references BoardKarte (fnr)
,   Flugzeugtyp_typidentifikation varchar(300) references Flugzeugtyp (typidentifikation)
,   klasse varchar(300)
,   ort varchar(300)
,   primary key(BoardKarte_fnr,Flugzeugtyp_typidentifikation,klasse,ort)
);

--Created from a m:n relation
create table Flug
(
    Ticket_fnr varchar(300)
,   Ticket_pnr varchar(300)
,   Ticket_tnr varchar(300)
,   Fluggesellschaft_orgCode varchar(300) references Fluggesellschaft (orgCode)
,   Flughafen_flughafennr varchar(300) references Flughafen (flughafennr)
,   primary key(Ticket_fnr,Ticket_pnr,Ticket_tnr,Fluggesellschaft_orgCode,Flughafen_flughafennr)
,   foreign key(Ticket_fnr, Ticket_pnr, Ticket_tnr) references Ticket(fnr,pnr,tnr)
);

drop table if exists Flug;
drop table if exists Sitzplatz;
drop table if exists Flughafen;
drop table if exists Fluggesellschaft;
drop table if exists Flugzeug;
drop table if exists Flugzeugtyp;
drop table if exists Ticket;
drop table if exists Passagier;
drop table if exists BoardKarte;
