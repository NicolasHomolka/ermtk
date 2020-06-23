drop tablespace Tankstelle including contents;
create tablespace Tankstelle
  datafile 'tbs_Tankstelle'
    size 20M reuse;
--Created from <ent>
create table tankstelle
(
    plz varchar(400) primary key
,   flaeche varchar(400)
,   adresse varchar(400)
)
tablespace Tankstelle;

--Created from <ent>
create table ort
(
    ortsname varchar(400) primary key
,   einwohner varchar(400)
,   bezirk varchar(400)
)
tablespace Tankstelle;

--Created from <ent>
create table mitarbeiter
(
    pnr varchar(400) primary key
,   name varchar(400)
)
tablespace Tankstelle;

--Created from <ent>
create table tank
(
    nr varchar(400) primary key
,   fassung varchar(400)
,   fuel varchar(400)
)
tablespace Tankstelle;

--Created from <ent>
create table kraftstoff
(
    bezeichn varchar(400) primary key
,   oktanz varchar(400)
,   kosten varchar(400)
)
tablespace Tankstelle;

--Created from <ent>
create table zapfsaeule
(
    nr varchar(400) primary key
)
tablespace Tankstelle;

--Created from <ent>
create table grosshaendler
(
    fname varchar(400)
,   anschrift varchar(400)
,   primary key(fname,anschrift)
)
tablespace Tankstelle;

--Created from a m:n relation
create table hat_mitarbeiter
(
    tankstelle_plz varchar(400) references tankstelle (plz)
,   mitarbeiter_pnr varchar(400) references mitarbeiter (pnr)
,   primary key(tankstelle_plz,mitarbeiter_pnr)
)
tablespace Tankstelle;

--Created from a m:n relation
create table tankkraft
(
    tank_nr varchar(400) references tank (nr)
,   kraftstoff_bezeichn varchar(400) references kraftstoff (bezeichn)
,   primary key(tank_nr,kraftstoff_bezeichn)
)
tablespace Tankstelle;

--Created from a m:n relation
create table vertrag_vereinbaren
(
    tankstelle_plz varchar(400) references tankstelle (plz)
,   grosshaendler_fname varchar(400)
,   grosshaendler_anschrift varchar(400)
,   primary key(tankstelle_plz,grosshaendler_fname,grosshaendler_anschrift)
,   constraint fk_grosshaendler1
      foreign key(grosshaendler_fname,grosshaendler_anschrift)
      references grosshaendler(fname,anschrift)
)
tablespace Tankstelle;

--Created from a m:n relation
create table tankvorgang
(
    tankstelle_plz varchar(400) references tankstelle (plz)
,   zapfsaeule_nr varchar(400) references zapfsaeule (nr)
,   kraftstoff_bezeichn varchar(400) references kraftstoff (bezeichn)
,   menge varchar(321)
,   preis varchar(321)
,   datum varchar(321)
,   uhrzeit varchar(321)
,   autoname varchar(321)
,   autofarbe varchar(321)
,   kennzeichen varchar(321)
,   primary key(tankstelle_plz,zapfsaeule_nr,kraftstoff_bezeichn)
)
tablespace Tankstelle;

drop table tankvorgang;
drop table vertrag_vereinbaren;
drop table tankkraft;
drop table hat_mitarbeiter;
drop table grosshaendler;
drop table zapfsaeule;
drop table kraftstoff;
drop table tank;
drop table mitarbeiter;
drop table ort;
drop table tankstelle;
