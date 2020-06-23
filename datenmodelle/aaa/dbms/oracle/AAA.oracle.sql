drop tablespace Fluggesellschaften including contents;
create tablespace Fluggesellschaften
  datafile 'tbs_Fluggesellschaften'
    size 20M reuse;
--Created from <ent>
create table BoardKarte
(
    fnr varchar(400) primary key
,   datum varchar(400)
,   abflughafen varchar(400)
,   ankunftsflughafen varchar(400)
,   name varchar(400)
,   sitz varchar(400)
)
tablespace Fluggesellschaften;

--Created from <ent>
create table Passagier
(
    fnr varchar(400) references BoardKarte (fnr)
,   pnr varchar(400)
,   name varchar(400)
,   anrede varchar(400)
,   titel varchar(400)
,   primary key(fnr,pnr)
)
tablespace Fluggesellschaften;

--Created from <ent>
create table Ticket
(
    fnr varchar(400)
,   pnr varchar(400)
,   tnr varchar(400)
,   ausgabedatum varchar(400)
,   preis varchar(400)
,   waehrung varchar(400)
,   vertriebsbuero varchar(400)
,   primary key(fnr,pnr,tnr)
,   constraint fk_Passagier1
      foreign key(fnr,pnr)
      references Passagier(fnr,pnr)
)
tablespace Fluggesellschaften;

--Created from <ent>
create table Flugzeugtyp
(
    typidentifikation varchar(400) primary key
,   hersteller varchar(400)
,   reichweite varchar(400)
)
tablespace Fluggesellschaften;

--Created from <ent>
create table Flugzeug
(
    flugzeugnummer varchar(400)
,   interregnummer varchar(400)
,   name varchar(400)
,   startDatum varchar(400)
,   primary key(flugzeugnummer,interregnummer)
)
tablespace Fluggesellschaften;

--Created from <ent>
create table Fluggesellschaft
(
    orgCode varchar(400) primary key
,   name varchar(400)
,   hauptsitz varchar(400)
)
tablespace Fluggesellschaften;

--Created from <ent>
create table Flughafen
(
    flughafennr varchar(400) primary key
,   name varchar(400)
,   stadt varchar(400)
,   land varchar(400)
,   kapazitaet varchar(400)
)
tablespace Fluggesellschaften;

--Created from a m:n relation
create table Sitzplatz
(
    BoardKarte_fnr varchar(400) references BoardKarte (fnr)
,   Flugzeugtyp_typidentifikation varchar(400) references Flugzeugtyp (typidentifikation)
,   klasse varchar(400)
,   ort varchar(400)
,   primary key(BoardKarte_fnr,Flugzeugtyp_typidentifikation,klasse,ort)
)
tablespace Fluggesellschaften;

--Created from a m:n relation
create table Flug
(
    Ticket_fnr varchar(400)
,   Ticket_pnr varchar(400)
,   Ticket_tnr varchar(400)
,   Fluggesellschaft_orgCode varchar(400) references Fluggesellschaft (orgCode)
,   Flughafen_flughafennr varchar(400) references Flughafen (flughafennr)
,   primary key(Ticket_fnr,Ticket_pnr,Ticket_tnr,Fluggesellschaft_orgCode,Flughafen_flughafennr)
,   constraint fk_Ticket2
      foreign key(Ticket_fnr,Ticket_pnr,Ticket_tnr)
      references Ticket(fnr,pnr,tnr)
)
tablespace Fluggesellschaften;

drop table Flug;
drop table Sitzplatz;
drop table Flughafen;
drop table Fluggesellschaft;
drop table Flugzeug;
drop table Flugzeugtyp;
drop table Ticket;
drop table Passagier;
drop table BoardKarte;
