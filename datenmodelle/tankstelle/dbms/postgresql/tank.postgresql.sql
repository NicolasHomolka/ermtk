--Created from <ent>
create table tankstelle
(
    plz varchar(300) primary key
,   flaeche varchar(300)
,   adresse varchar(300)
);

--Created from <ent>
create table ort
(
    ortsname varchar(300) primary key
,   einwohner varchar(300)
,   bezirk varchar(300)
);

--Created from <ent>
create table mitarbeiter
(
    pnr varchar(300) primary key
,   name varchar(300)
);

--Created from <ent>
create table tank
(
    nr varchar(300) primary key
,   fassung varchar(300)
,   fuel varchar(300)
);

--Created from <ent>
create table kraftstoff
(
    bezeichn varchar(300) primary key
,   oktanz varchar(300)
,   kosten varchar(300)
);

--Created from <ent>
create table zapfsaeule
(
    nr varchar(300) primary key
);

--Created from <ent>
create table grosshaendler
(
    fname varchar(300)
,   anschrift varchar(300)
,   primary key(fname,anschrift)
);

--Created from a m:n relation
create table hat_mitarbeiter
(
    tankstelle_plz varchar(300) references tankstelle (plz)
,   mitarbeiter_pnr varchar(300) references mitarbeiter (pnr)
,   primary key(tankstelle_plz,mitarbeiter_pnr)
);

--Created from a m:n relation
create table tankkraft
(
    tank_nr varchar(300) references tank (nr)
,   kraftstoff_bezeichn varchar(300) references kraftstoff (bezeichn)
,   primary key(tank_nr,kraftstoff_bezeichn)
);

--Created from a m:n relation
create table vertrag_vereinbaren
(
    tankstelle_plz varchar(300) references tankstelle (plz)
,   grosshaendler_fname varchar(300)
,   grosshaendler_anschrift varchar(300)
,   primary key(tankstelle_plz,grosshaendler_fname,grosshaendler_anschrift)
,   foreign key(grosshaendler_fname, grosshaendler_anschrift) references grosshaendler(fname,anschrift)
);

--Created from a m:n relation
create table tankvorgang
(
    tankstelle_plz varchar(300) references tankstelle (plz)
,   zapfsaeule_nr varchar(300) references zapfsaeule (nr)
,   kraftstoff_bezeichn varchar(300) references kraftstoff (bezeichn)
,   menge varchar(321)
,   preis varchar(321)
,   datum varchar(321)
,   uhrzeit varchar(321)
,   autoname varchar(321)
,   autofarbe varchar(321)
,   kennzeichen varchar(321)
,   primary key(tankstelle_plz,zapfsaeule_nr,kraftstoff_bezeichn)
);

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
