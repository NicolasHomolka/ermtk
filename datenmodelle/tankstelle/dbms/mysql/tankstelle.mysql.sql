drop table if exists tankvorgang;
drop table if exists vertrag_vereinbaren;
drop table if exists tankkraft;
drop table if exists hat_mitarbeiter;
drop table if exists grosshaendler;
drop table if exists zapfsaeule;
drop table if exists kraftstoff;
drop table if exists tank;
drop table if exists mitarbeiter;
drop table if exists ort;
drop table if exists tankstelle;

#Created from <ent>
create table tankstelle(
    plz     varchar(132)  not null primary key
,   flaeche varchar(132)  not null
,   adresse varchar(132)  not null
);

#Created from <ent>
create table ort(
    ortsname  varchar(132)  not null primary key
,   einwohner varchar(132)  not null
,   bezirk    varchar(132)  not null
);

#Created from <ent>
create table mitarbeiter(
    pnr  varchar(132)  not null primary key
,   name varchar(132)  not null
);

#Created from <ent>
create table tank(
    nr      varchar(132)  not null primary key
,   fassung varchar(132)  not null
,   fuel    varchar(132)  not null
);

#Created from <ent>
create table kraftstoff(
    bezeichn varchar(132)  not null primary key
,   oktanz   varchar(132)  not null
,   kosten   varchar(132)  not null
);

#Created from <ent>
create table zapfsaeule(
    nr varchar(132)  not null primary key
);

#Created from <ent>
create table grosshaendler(
    fname     varchar(132)  not null
,   anschrift varchar(132)  not null
,   primary key(fname, anschrift)
);

#Created from a m:n relation
create table hat_mitarbeiter(
    tankstelle_plz  varchar(132)  not null references tankstelle (plz)
,   mitarbeiter_pnr varchar(132)  not null references mitarbeiter (pnr)
,   primary key(tankstelle_plz, mitarbeiter_pnr)
);

#Created from a m:n relation
create table tankkraft(
    tank_nr             varchar(132)  not null references tank (nr)
,   kraftstoff_bezeichn varchar(132)  not null references kraftstoff (bezeichn)
,   primary key(tank_nr, kraftstoff_bezeichn)
);

#Created from a m:n relation
create table vertrag_vereinbaren(
    tankstelle_plz         varchar(132)  not null references tankstelle (plz)
,   grosshaendler_fname    varchar(132)  not null
,   grosshaendler_anschrift varchar(132)  not null
,   primary key(tankstelle_plz, grosshaendler_fname, grosshaendler_anschrift)
,   constraint fk_grosshaendler1
      foreign key(grosshaendler_fname, grosshaendler_anschrift)
      references grosshaendler(fname, anschrift)
);

#Created from a m:n relation
create table tankvorgang(
    tankstelle_plz      varchar(132)  not null references tankstelle (plz)
,   zapfsaeule_nr       varchar(132)  not null references zapfsaeule (nr)
,   kraftstoff_bezeichn varchar(132)  not null references kraftstoff (bezeichn)
,   menge               varchar(132)  not null
,   preis               varchar(132)  not null
,   datum               varchar(132)  not null
,   uhrzeit             varchar(132)  not null
,   autoname            varchar(132)  not null
,   autofarbe           varchar(132)  not null
,   kennzeichen         varchar(132)  not null
,   primary key(tankstelle_plz, zapfsaeule_nr, kraftstoff_bezeichn)
);

