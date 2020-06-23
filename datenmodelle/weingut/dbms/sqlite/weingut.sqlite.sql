--Created from <ent>
create table if not exists wein(
    name     text  not null primary key
,   farbe    text  not null
,   jahrgang text  not null
,   restsuesse text  not null
,   erzeuger text  not null
);

--Created from <ent>
create table if not exists erzeuger(
    name         text  not null primary key
,   adresse      text  not null
,   lizenznummer text  not null
,   mengewein    text  not null
,   anbaugebiet  text  not null
);

--Created from <ent>
create table if not exists anbaugebiet(
    name   text  not null
,   region text  not null
,   land   text  not null
);

--Created from <ent>
create table if not exists rebsorte(
    name   text  not null
,   farbe  text  not null
,   anteil text  not null
);

--Created from <ent>
create table if not exists lizenz(
    lizenznummer text  not null
,   menge        text  not null
);

--Created from a m:n relation
create table if not exists erzeugt(
    erzeuger_name text  not null references erzeuger (name)
,   wein_name     text  not null references wein (name)
,   primary key(erzeuger_name, wein_name)
);

--Created from a m:n relation
create table if not exists "beinhaltet"(
    wein_name text  not null primary key references wein (name)
,   anteil    text  not null
);

