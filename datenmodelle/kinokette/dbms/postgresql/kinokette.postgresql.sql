--Created from <ent>
create table kino
(
    adresse varchar(300) primary key
,   name varchar(300)
);

--Created from <ent>
create table saal
(
    adresse varchar(300) references kino (adresse)
,   saal_nr varchar(300)
,   primary key(adresse,saal_nr)
);

--Created from <ent>
create table sitzplan
(
    reihe varchar(300)
,   sitz_nr varchar(300)
,   begin varchar(300)
,   vergeben varchar(300)
,   primary key(reihe,sitz_nr,begin)
);

--Created from <ent>
create table ticket
(
    begin varchar(300)
,   reihe varchar(300)
);

--Created from <ent>
create table zeitplan
(
    begin varchar(300) primary key
);

--Created from <ent>
create table film
(
    titel varchar(300) primary key
,   genre varchar(300)
,   herstellungsjahr varchar(300)
,   land varchar(300)
,   sprache varchar(300)
,   dauer varchar(300)
,   verleih varchar(300)
,   altersfreigabe varchar(300)
);

--Created from <ent>
create table person
(
    svnr varchar(300) primary key
,   nachname varchar(300)
,   vorname varchar(300)
,   nationalitaet varchar(300)
,   geburtsdatum varchar(300)
,   todesdatum varchar(300)
,   bemerkung varchar(300)
);

--Created from a m:n relation
create table spielt_mit
(
    person_svnr varchar(300) references person (svnr)
,   film_titel varchar(300) references film (titel)
,   primary key(person_svnr,film_titel)
);

--Created from a m:n relation
create table wird_gezeigt_in
(
    film_titel varchar(300) references film (titel)
,   kino_adresse varchar(300) references kino (adresse)
,   von varchar(300)
,   bis varchar(300)
,   primary key(film_titel,kino_adresse)
);

--Created from a m:n relation
create table ist_Sitzplan_fuer
(
    saal_adresse varchar(300)
,   saal_saal_nr varchar(300)
,   sitzplan_reihe varchar(300)
,   sitzplan_sitz_nr varchar(300)
,   sitzplan_begin varchar(300)
,   primary key(saal_adresse,saal_saal_nr,sitzplan_reihe,sitzplan_sitz_nr,sitzplan_begin)
,   foreign key(saal_adresse, saal_saal_nr) references saal(adresse,saal_nr)
,   foreign key(sitzplan_reihe, sitzplan_sitz_nr, sitzplan_begin) references sitzplan(reihe,sitz_nr,begin)
);

drop table if exists ist_Sitzplan_fuer;
drop table if exists wird_gezeigt_in;
drop table if exists spielt_mit;
drop table if exists person;
drop table if exists film;
drop table if exists zeitplan;
drop table if exists ticket;
drop table if exists sitzplan;
drop table if exists saal;
drop table if exists kino;
