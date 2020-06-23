--Created from <ent>
create table if not exists kino(
    adresse text  not null primary key
,   name    text  not null
);

--Created from <ent>
create table if not exists saal(
    adresse text  not null references kino (adresse)
,   saal_nr text  not null
,   primary key(adresse, saal_nr)
);

--Created from <ent>
create table if not exists sitzplan(
    reihe    text  not null
,   sitz_nr  text  not null
,   begin    text  not null
,   vergeben text  not null
,   primary key(reihe, sitz_nr, begin)
);

--Created from <ent>
create table if not exists ticket(
    beginn text  not null
,   reihe  text  not null
);

--Created from <ent>
create table if not exists zeitplan(
    begin text  not null primary key
);

--Created from <ent>
create table if not exists film(
    titel            text  not null primary key
,   genre            text  not null
,   herstellungsjahr text  not null
,   land             text  not null
,   sprache          text  not null
,   dauer            text  not null
,   verleih          text  not null
,   altersfreigabe   text  not null
);

--Created from <ent>
create table if not exists person(
    svnr          text  not null primary key
,   nachname      text  not null
,   vorname       text  not null
,   nationalitaet text  not null
,   geburtsdatum  text  not null
,   todesdatum    text  not null
,   bemerkung     text  not null
);

--Created from a m:n relation
create table if not exists spielt_mit(
    person_svnr text  not null references person (svnr)
,   film_titel  text  not null references film (titel)
,   primary key(person_svnr, film_titel)
);

--Created from a m:n relation
create table if not exists wird_gezeigt_in(
    film_titel   text  not null references film (titel)
,   kino_adresse text  not null references kino (adresse)
,   von          text  not null
,   bis          text  not null
,   primary key(film_titel, kino_adresse)
);

--Created from a m:n relation
create table if not exists ist_Sitzplan_fuer(
    saal_adresse     text  not null
,   saal_saal_nr     text  not null
,   sitzplan_reihe   text  not null
,   sitzplan_sitz_nr text  not null
,   sitzplan_begin   text  not null
,   primary key(saal_adresse, saal_saal_nr, sitzplan_reihe, sitzplan_sitz_nr, sitzplan_begin)
,   constraint fk_saal1
      foreign key(saal_adresse, saal_saal_nr)
      references saal(adresse, saal_nr)
,   constraint fk_sitzplan2
      foreign key(sitzplan_reihe, sitzplan_sitz_nr, sitzplan_begin)
      references sitzplan(reihe, sitz_nr, begin)
);

