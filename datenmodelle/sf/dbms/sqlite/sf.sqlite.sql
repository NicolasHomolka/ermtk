--Created from <ent>
create table if not exists kurs(
    knr      text  not null primary key
,   bezeichn text  not null
,   tage     text  not null
,   preis    text  not null
);

--Created from <ent>
create table if not exists kveranst(
    knr     text  not null references kurs (knr)
,   knrlfnd text  not null
,   von     text  not null
,   bis     text  not null
,   ort     text  not null
,   plaetze text  not null
,   primary key(knr, knrlfnd)
);

--Created from <ent>
create table if not exists person(
    pnr   text  not null primary key
,   fname text  not null
,   vname text  not null
,   ort   text  not null
,   land  text  not null
);

--Created from <ent>
create table if not exists referent(
    gebdat text  not null
,   seit   text  not null
,   titel  text  not null
,   pnr    text  not null primary key references person (pnr)
);

--Created from a m:n relation
create table if not exists setzt_voraus(
    kurs_knr  text  not null references kurs (knr)
,   kurs_knr2 text  not null references kurs (knr)
,   primary key(kurs_knr, kurs_knr2)
);

--Created from a m:n relation
create table if not exists besucht(
    kveranst_knr     text  not null
,   kveranst_knrlfnd text  not null
,   person_pnr       text  not null references person (pnr)
,   bezahlt          text  not null
,   primary key(kveranst_knr, kveranst_knrlfnd, person_pnr)
,   constraint fk_kveranst1
      foreign key(kveranst_knr, kveranst_knrlfnd)
      references kveranst(knr, knrlfnd)
);

--Created from a m:n relation
create table if not exists geeignet(
    kurs_knr     text  not null references kurs (knr)
,   referent_pnr text  not null references referent (pnr)
,   primary key(kurs_knr, referent_pnr)
);

