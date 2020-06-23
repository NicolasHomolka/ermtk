//Database Schulinformationssystem

//Created from <ent>
var Person real relation
{
    svnr char
,   nName char
,   vName char
,   gebDat char
} key{svnr};

//Created from <ent>
var Lehrer real relation
{
    lnr char
,   svnr char
} key{svnr};

constraint fk_Lehrer_Person_on_svnr Lehrer{svnr} <= Person {svnr};

//Created from <ent>
var Schueler real relation
{
    MatrNr char
,   svnr char
} key{svnr};

constraint fk_Schueler_Person_on_svnr Schueler{svnr} <= Person {svnr};

//Created from <ent>
var Abteilung real relation
{
    abkuerzung char
,   name char
} key{abkuerzung};

//Created from <ent>
var Gegenstand real relation
{
    abkuerzung char
,   bezeichnung char
} key{abkuerzung};

//Created from <ent>
var Lehrplan real relation
{
    jahrgang char
,   pStunden char
,   tStunden char
} key{jahrgang};

//Created from <ent>
var Klasse real relation
{
    bezeichnung char
,   jahrgang char
,   klassensprecher char
,   kassierer char
} key{bezeichnung};

//Created from <ent>
var LVG real relation
{
    lvgNr char
,   faktor char
} key{lvgNr};

//Created from a m:n relation
var ist_Geschwister_von real relation
{
    Schueler_svnr char
,   Schueler_svnr2 char
}key{Schueler_svnr,Schueler_svnr2};

constraint fk_ist_Geschwister_von_Schueler_on_Schueler_svnr (ist_Geschwister_von rename {Schueler_svnr as svnr}) {svnr} <= Schueler {svnr};

constraint fk_ist_Geschwister_von_Schueler_on_Schueler_svnr2 (ist_Geschwister_von rename {Schueler_svnr2 as svnr}) {svnr} <= Schueler {svnr};

//Created from a m:n relation
var besitzt_Noten_fuer real relation
{
    Schueler_svnr char
,   Gegenstand_abkuerzung char
,   semesternote char
,   jahresnote char
}key{Schueler_svnr,Gegenstand_abkuerzung};

constraint fk_besitzt_Noten_fuer_Schueler_on_Schueler_svnr (besitzt_Noten_fuer rename {Schueler_svnr as svnr}) {svnr} <= Schueler {svnr};

constraint fk_besitzt_Noten_fuer_Gegenstand_on_Gegenstand_abkuerzung (besitzt_Noten_fuer rename {Gegenstand_abkuerzung as abkuerzung}) {abkuerzung} <= Gegenstand {abkuerzung};

//Created from a m:n relation
var vermerkt real relation
{
    Gegenstand_abkuerzung char
} key{Gegenstand_abkuerzung};

constraint fk_vermerkt_Gegenstand_on_Gegenstand_abkuerzung (vermerkt rename {Gegenstand_abkuerzung as abkuerzung}) {abkuerzung} <= Gegenstand {abkuerzung};

