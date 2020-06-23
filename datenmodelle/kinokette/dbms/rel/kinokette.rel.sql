//Database Kinokette

//Created from <ent>
var kino real relation
{
    adresse char
,   name char
} key{adresse};

//Created from <ent>
var saal real relation
{
    adresse char
,   saal_nr char
}key{adresse,saal_nr};

constraint fk_saal_kino_on_adresse saal{adresse} <= kino {adresse};

//Created from <ent>
var sitzplan real relation
{
    reihe char
,   sitz_nr char
,   begin1 char
,   vergeben char
}key{reihe,sitz_nr,begin1};

//Created from <ent>
var ticket real relation
{
    begin1 char
,   reihe char
}key{};

//Created from <ent>
var zeitplan real relation
{
    begin1 char
} key{begin1};

//Created from <ent>
var film real relation
{
    titel char
,   genre char
,   herstellungsjahr char
,   land char
,   sprache char
,   dauer char
,   verleih char
,   altersfreigabe char
} key{titel};

//Created from <ent>
var person real relation
{
    svnr char
,   nachname char
,   vorname char
,   nationalitaet char
,   geburtsdatum char
,   todesdatum char
,   bemerkung char
} key{svnr};

//Created from a m:n relation
var spielt_mit real relation
{
    person_svnr char
,   film_titel char
}key{person_svnr,film_titel};

constraint fk_spielt_mit_person_on_person_svnr (spielt_mit rename {person_svnr as svnr}) {svnr} <= person {svnr};

constraint fk_spielt_mit_film_on_film_titel (spielt_mit rename {film_titel as titel}) {titel} <= film {titel};

//Created from a m:n relation
var wird_gezeigt_in real relation
{
    film_titel char
,   kino_adresse char
,   von char
,   bis char
}key{film_titel,kino_adresse};

constraint fk_wird_gezeigt_in_film_on_film_titel (wird_gezeigt_in rename {film_titel as titel}) {titel} <= film {titel};

constraint fk_wird_gezeigt_in_kino_on_kino_adresse (wird_gezeigt_in rename {kino_adresse as adresse}) {adresse} <= kino {adresse};

//Created from a m:n relation
var ist_Sitzplan_fuer real relation
{
    saal_adresse char
,   saal_saal_nr char
,   sitzplan_reihe char
,   sitzplan_sitz_nr char
,   sitzplan_begin char
}key{saal_adresse,saal_saal_nr,sitzplan_reihe,sitzplan_sitz_nr,sitzplan_begin};

constraint fk_ist_Sitzplan_fuer_saal_on_saal_adresse (ist_Sitzplan_fuer rename {saal_adresse as adresse}) {adresse} <= saal {adresse};

constraint fk_ist_Sitzplan_fuer_saal_on_saal_saal_nr (ist_Sitzplan_fuer rename {saal_saal_nr as saal_nr}) {saal_nr} <= saal {saal_nr};

constraint fk_ist_Sitzplan_fuer_sitzplan_on_sitzplan_reihe (ist_Sitzplan_fuer rename {sitzplan_reihe as reihe}) {reihe} <= sitzplan {reihe};

constraint fk_ist_Sitzplan_fuer_sitzplan_on_sitzplan_sitz_nr (ist_Sitzplan_fuer rename {sitzplan_sitz_nr as sitz_nr}) {sitz_nr} <= sitzplan {sitz_nr};

constraint fk_ist_Sitzplan_fuer_sitzplan_on_sitzplan_begin (ist_Sitzplan_fuer rename {sitzplan_begin as begin1}) {begin1} <= sitzplan {begin1};

