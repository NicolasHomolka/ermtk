drop table if exists Flug;
drop table if exists "Sitzplatz";
drop table if exists Flughafen;
drop table if exists Fluggesellschaft;
drop table if exists Flugzeug;
drop table if exists Flugzeugtyp;
drop table if exists Ticket;
drop table if exists Passagier;
drop table if exists BoardKarte;
go

--Created from <ent>
create table BoardKarte(
    fnr               varchar(132)  not null primary key
,   datum             varchar(132)  not null
,   abflughafen       varchar(132)  not null
,   ankunftsflughafen varchar(132)  not null
,   name              varchar(132)  not null
,   sitz              varchar(132)  not null
);
go

--Created from <ent>
create table Passagier(
    fnr    varchar(132)  not null references BoardKarte(fnr)
,   pnr    varchar(132)  not null
,   name   varchar(132)  not null
,   anrede varchar(132)  not null
,   titel  varchar(132)  not null
,   primary key(fnr, pnr)
);
go

--Created from <ent>
create table Ticket(
    fnr            varchar(132)  not null
,   pnr            varchar(132)  not null
,   tnr            varchar(132)  not null
,   ausgabedatum   varchar(132)  not null
,   preis          varchar(132)  not null
,   waehrung       varchar(132)  not null
,   vertriebsbuero varchar(132)  not null
,   primary key(fnr, pnr, tnr)
,   constraint fk_Passagier1
      foreign key(fnr, pnr)
      references Passagier(fnr, pnr)
);
go

--Created from <ent>
create table Flugzeugtyp(
    typidentifikation varchar(132)  not null primary key
,   hersteller        varchar(132)  not null
,   "reichweite"      varchar(132)  not null
);
go

--Created from <ent>
create table Flugzeug(
    flugzeugnummer varchar(132)  not null
,   interregnummer varchar(132)  not null
,   name           varchar(132)  not null
,   startDatum     varchar(132)  not null
,   primary key(flugzeugnummer, interregnummer)
);
go

--Created from <ent>
create table Fluggesellschaft(
    orgCode   varchar(132)  not null primary key
,   name      varchar(132)  not null
,   hauptsitz varchar(132)  not null
);
go

--Created from <ent>
create table Flughafen(
    flughafennr varchar(132)  not null primary key
,   name        varchar(132)  not null
,   stadt       varchar(132)  not null
,   land        varchar(132)  not null
,   kapazitaet  varchar(132)  not null
);
go

--Created from a m:n relation
create table "Sitzplatz"(
    Flugzeugtyp_typidentifikation varchar(132)  not null references Flugzeugtyp(typidentifikation)
,   klasse                        varchar(132)  not null
,   ort                           varchar(132)  not null
,   primary key(Flugzeugtyp_typidentifikation, klasse, ort)
);
go

--Created from a m:n relation
create table Flug(
    Ticket_fnr               varchar(132)  not null
,   Ticket_pnr               varchar(132)  not null
,   Ticket_tnr               varchar(132)  not null
,   Fluggesellschaft_orgCode varchar(132)  not null references Fluggesellschaft(orgCode)
,   Flughafen_flughafennr    varchar(132)  not null references Flughafen(flughafennr)
,   primary key(Ticket_fnr, Ticket_pnr, Ticket_tnr, Fluggesellschaft_orgCode, Flughafen_flughafennr)
,   constraint fk_Ticket2
      foreign key(Ticket_fnr, Ticket_pnr, Ticket_tnr)
      references Ticket(fnr, pnr, tnr)
);
go

