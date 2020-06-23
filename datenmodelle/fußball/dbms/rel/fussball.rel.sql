//Database Fussball

//Created from <ent>
var mannschaft real relation
{
    name char
,   gruendungsjahr char
,   adresse char
} key{name};

//Created from <ent>
var person real relation
{
    svnr char
,   name char
,   wohnadresse char
,   geburtsdatum char
} key{svnr};

//Created from <ent>
var spieler real relation
{
    spielposition char
,   svnr char
} key{svnr};

constraint fk_spieler_person_on_svnr spieler{svnr} <= person {svnr};

//Created from <ent>
var spiel real relation
{
    spielort char
,   datum char
,   mannschaft_heim char
,   mannschaft_ausw char
,   schiedsrichter char
,   ergebnis char
}key{spielort,datum};

//Created from <ent>
var turnier real relation
{
    nummer char
,   name char
,   begindatum char
,   enddatum char
,   mannschaften char
}key{nummer,name};

//Created from <ent>
var schiedsrichter real relation
{
    datum_pruefung char
,   berechtigungsklasse char
,   svnr char
} key{svnr};

constraint fk_schiedsrichter_person_on_svnr schiedsrichter{svnr} <= person {svnr};

//Created from <ent>
var tore real relation
{
    anzahl_tore char
}key{};

//Created from a m:n relation
var spielt_mit_bei real relation
{
    mannschaft_name char
,   spiel_spielort char
,   spiel_datum char
}key{mannschaft_name,spiel_spielort,spiel_datum};

constraint fk_spielt_mit_bei_mannschaft_on_mannschaft_name (spielt_mit_bei rename {mannschaft_name as name}) {name} <= mannschaft {name};

constraint fk_spielt_mit_bei_spiel_on_spiel_spielort (spielt_mit_bei rename {spiel_spielort as spielort}) {spielort} <= spiel {spielort};

constraint fk_spielt_mit_bei_spiel_on_spiel_datum (spielt_mit_bei rename {spiel_datum as datum}) {datum} <= spiel {datum};

//Created from a m:n relation
var hat_geschossen real relation
{
    spieler_svnr char
} key{spieler_svnr};

//Created from a m:n relation
var wurden_geschossen real relation
{
    spiel_spielort char
,   spiel_datum char
}key{spiel_spielort,spiel_datum};

constraint fk_wurden_geschossen_spiel_on_spiel_spielort (wurden_geschossen rename {spiel_spielort as spielort}) {spielort} <= spiel {spielort};

constraint fk_wurden_geschossen_spiel_on_spiel_datum (wurden_geschossen rename {spiel_datum as datum}) {datum} <= spiel {datum};

