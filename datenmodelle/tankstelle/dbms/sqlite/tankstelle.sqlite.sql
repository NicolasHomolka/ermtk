--Created from <ent>
create table if not exists tankstelle(
    plz     text  not null primary key
,   flaeche text  not null
,   adresse text  not null
);

--Created from <ent>
create table if not exists ort(
    ortsname  text  not null primary key
,   einwohner text  not null
,   bezirk    text  not null
);

--Created from <ent>
create table if not exists mitarbeiter(
    pnr  text  not null primary key
,   name text  not null
);

--Created from <ent>
create table if not exists tank(
    nr      text  not null primary key
,   fassung text  not null
,   fuel    text  not null
);

--Created from <ent>
create table if not exists kraftstoff(
    bezeichn text  not null primary key
,   oktanz   text  not null
,   kosten   text  not null
);

--Created from <ent>
create table if not exists zapfsaeule(
    nr text  not null primary key
);

--Created from <ent>
create table if not exists grosshaendler(
    fname     text  not null
,   anschrift text  not null
,   primary key(fname, anschrift)
);

--Created from a m:n relation
create table if not exists hat_mitarbeiter(
    tankstelle_plz  text  not null references tankstelle (plz)
,   mitarbeiter_pnr text  not null references mitarbeiter (pnr)
,   primary key(tankstelle_plz, mitarbeiter_pnr)
);

--Created from a m:n relation
create table if not exists tankkraft(
    tank_nr             text  not null references tank (nr)
,   kraftstoff_bezeichn text  not null references kraftstoff (bezeichn)
,   primary key(tank_nr, kraftstoff_bezeichn)
);

--Created from a m:n relation
create table if not exists vertrag_vereinbaren(
    tankstelle_plz         text  not null references tankstelle (plz)
,   grosshaendler_fname    text  not null
,   grosshaendler_anschrift text  not null
,   primary key(tankstelle_plz, grosshaendler_fname, grosshaendler_anschrift)
,   constraint fk_grosshaendler1
      foreign key(grosshaendler_fname, grosshaendler_anschrift)
      references grosshaendler(fname, anschrift)
);

--Created from a m:n relation
create table if not exists tankvorgang(
    tankstelle_plz      text  not null references tankstelle (plz)
,   zapfsaeule_nr       text  not null references zapfsaeule (nr)
,   kraftstoff_bezeichn text  not null references kraftstoff (bezeichn)
,   menge               text  not null
,   preis               text  not null
,   datum               text  not null
,   uhrzeit             text  not null
,   autoname            text  not null
,   autofarbe           text  not null
,   kennzeichen         text  not null
,   primary key(tankstelle_plz, zapfsaeule_nr, kraftstoff_bezeichn)
);

