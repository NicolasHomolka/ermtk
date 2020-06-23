//Database Schulungsfirma

//Created from <ent>
var kurs real relation
{
    knr char
,   bezeichn char
,   tage char
,   preis char
} key{knr};

//Created from <ent>
var kveranst real relation
{
    knr char
,   knrlfnd char
,   von char
,   bis char
,   ort char
,   plaetze char
}key{knr,knrlfnd};

constraint fk_kveranst_kurs_on_knr kveranst{knr} <= kurs {knr};

//Created from <ent>
var person real relation
{
    pnr char
,   fname char
,   vname char
,   ort char
,   land char
} key{pnr};

//Created from <ent>
var referent real relation
{
    gebdat char
,   seit char
,   titel char
,   pnr char
} key{pnr};

constraint fk_referent_person_on_pnr referent{pnr} <= person {pnr};

//Created from a m:n relation
var setzt_voraus real relation
{
    kurs_knr char
,   kurs_knr2 char
}key{kurs_knr,kurs_knr2};

constraint fk_setzt_voraus_kurs_on_kurs_knr (setzt_voraus rename {kurs_knr as knr}) {knr} <= kurs {knr};

constraint fk_setzt_voraus_kurs_on_kurs_knr2 (setzt_voraus rename {kurs_knr2 as knr}) {knr} <= kurs {knr};

//Created from a m:n relation
var besucht real relation
{
    kveranst_knr char
,   kveranst_knrlfnd char
,   person_pnr char
,   kurs_knr char
,   bezahlt char
}key{kveranst_knr,kveranst_knrlfnd,person_pnr,kurs_knr};

constraint fk_besucht_kveranst_on_kveranst_knr (besucht rename {kveranst_knr as knr}) {knr} <= kveranst {knr};

constraint fk_besucht_kveranst_on_kveranst_knrlfnd (besucht rename {kveranst_knrlfnd as knrlfnd}) {knrlfnd} <= kveranst {knrlfnd};

constraint fk_besucht_person_on_person_pnr (besucht rename {person_pnr as pnr}) {pnr} <= person {pnr};

constraint fk_besucht_kurs_on_kurs_knr (besucht rename {kurs_knr as knr}) {knr} <= kurs {knr};

//Created from a m:n relation
var geeignet real relation
{
    kurs_knr char
,   referent_pnr char
}key{kurs_knr,referent_pnr};

constraint fk_geeignet_kurs_on_kurs_knr (geeignet rename {kurs_knr as knr}) {knr} <= kurs {knr};

constraint fk_geeignet_referent_on_referent_pnr (geeignet rename {referent_pnr as pnr}) {pnr} <= referent {pnr};

