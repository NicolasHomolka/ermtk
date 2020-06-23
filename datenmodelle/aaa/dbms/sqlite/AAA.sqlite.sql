--Created from <ent>
create table if not exists BoardKarte(
    fnr               text  not null primary key
,   datum             text  not null
,   abflughafen       text  not null
,   ankunftsflughafen text  not null
,   name              text  not null
,   sitz              text  not null
);

--Created from <ent>
create table if not exists Passagier(
    fnr    text  not null references BoardKarte (fnr)
,   pnr    text  not null
,   name   text  not null
,   anrede text  not null
,   titel  text  not null
,   primary key(fnr, pnr)
);

--Created from <ent>
create table if not exists Ticket(
    fnr            text  not null
,   pnr            text  not null
,   tnr            text  not null
,   ausgabedatum   text  not null
,   preis          text  not null
,   waehrung       text  not null
,   vertriebsbuero text  not null
,   primary key(fnr, pnr, tnr)
,   constraint fk_Passagier1
      foreign key(fnr, pnr)
      references Passagier(fnr, pnr)
);

--Created from <ent>
create table if not exists Flugzeugtyp(
    typidentifikation text  not null primary key
,   hersteller        text  not null
,   "reichweite"      text  not null
);

--Created from <ent>
create table if not exists Flugzeug(
    flugzeugnummer text  not null
,   interregnummer text  not null
,   name           text  not null
,   startDatum     text  not null
,   primary key(flugzeugnummer, interregnummer)
);

--Created from <ent>
create table if not exists Fluggesellschaft(
    orgCode   text  not null primary key
,   name      text  not null
,   hauptsitz text  not null
);

--Created from <ent>
create table if not exists Flughafen(
    flughafennr text  not null primary key
,   name        text  not null
,   stadt       text  not null
,   land        text  not null
,   kapazitaet  text  not null
);

--Created from a m:n relation
create table if not exists "Sitzplatz"(
    Flugzeugtyp_typidentifikation text  not null references Flugzeugtyp (typidentifikation)
,   klasse                        text  not null
,   ort                           text  not null
,   primary key(Flugzeugtyp_typidentifikation, klasse, ort)
);

--Created from a m:n relation
create table if not exists Flug(
    Ticket_fnr               text  not null
,   Ticket_pnr               text  not null
,   Ticket_tnr               text  not null
,   Fluggesellschaft_orgCode text  not null references Fluggesellschaft (orgCode)
,   Flughafen_flughafennr    text  not null references Flughafen (flughafennr)
,   primary key(Ticket_fnr, Ticket_pnr, Ticket_tnr, Fluggesellschaft_orgCode, Flughafen_flughafennr)
,   constraint fk_Ticket2
      foreign key(Ticket_fnr, Ticket_pnr, Ticket_tnr)
      references Ticket(fnr, pnr, tnr)
);

