//Database Mondial_Datenbank

//Created from <ent>
var Land real relation
{
    Land char
,   Code char
,   Hauptstadt char
,   Gebietsgroesse char
,   Bevoelkerung char
,   Bevoelkerungungswachstum char
,   Kindersterblichkeitsrate char
,   BIP char
,   Landwirtschaft char
,   Dienstleistungen char
,   Industrie char
,   Inflation char
,   Arbeitslosigkeit char
,   Unabhaengigkeit char
,   WarAbhaengig char
,   Abhaengig char
,   Regierung char
} key{Code};

constraint fk_Land_Land_on_Code Land{Code} <= Land {Code};

//Created from <ent>
var Provinz real relation
{
    Code char
,   Provinz char
,   Bevoelkerung char
,   Gebietsgroesse char
,   lokaler_Name char
}key{Code,Provinz};

constraint fk_Provinz_Land_on_Code Provinz{Code} <= Land {Code};

//Created from <ent>
var Stadt real relation
{
    Code char
,   Provinz char
,   Stadt char
,   lokaler_name char
,   Bevoelkerung char
,   Breitengrad char
,   Laengengrad char
,   Hoehe char
}key{Code,Provinz,Stadt};

constraint fk_Stadt_Provinz_on_Code Stadt{Code} <= Provinz {Code};

constraint fk_Stadt_Provinz_on_Provinz Stadt{Provinz} <= Provinz {Provinz};

//Created from <ent>
var Organisation real relation
{
    Abkuerzung char
,   Organisation char
,   Etabliert char
} key{Abkuerzung};

//Created from <ent>
var Flughafen real relation
{
    IATACode char
,   Flughafen char
,   Insel char
,   Breitengrad char
,   Laengengrad char
,   Hoehe char
} key{IATACode};

//Created from <ent>
var Sprache real relation
{
    Sprache char
} key{Sprache};

//Created from <ent>
var Ethnische_Gruppe real relation
{
    Ethnische_Gruppe char
} key{Ethnische_Gruppe};

//Created from <ent>
var Religion real relation
{
    Religion char
} key{Religion};

//Created from <ent>
var Kontinent real relation
{
    Kontinent char
,   Gebietsgroesse char
} key{Kontinent};

//Created from <ent>
var Berg real relation
{
    Berg char
,   Berge char
,   Hoehe char
,   Typ char
,   Laengengrad char
,   Breitengrad char
} key{Berg};

//Created from <ent>
var Wueste real relation
{
    Wueste char
,   Gebietsgroesse char
,   Laengengrad char
,   Breitengrad char
} key{Wueste};

//Created from <ent>
var Insel real relation
{
    Insel char
,   Inseln char
,   Gebietsgroesse char
,   Hoehe char
,   Typ char
,   Laengengrad char
,   Breitengrad char
} key{Insel};

//Created from <ent>
var See real relation
{
    See char
,   Gebietsgroesse char
,   Hoehe char
,   Tiefe char
,   Typ char
,   Koordinaten char
} key{See};

//Created from <ent>
var Meer real relation
{
    Meer char
,   Gebietsgroesse char
,   Tiefe char
} key{Meer};

//Created from <ent>
var Fluss real relation
{
    Fluss char
,   Laenge char
,   Gebietsgroesse char
} key{Fluss};

//Created from <ent>
var Quelle real relation
{
    Fluss char
,   Berg char
,   Hoehe char
,   Laengengrad char
,   Breitengrad char
} key{Fluss};

constraint fk_Quelle_Fluss_on_Fluss Quelle{Fluss} <= Fluss {Fluss};

//Created from <ent>
var Muendung real relation
{
    Fluss char
,   Hoehe char
,   Laengengrad char
,   Breitengrad char
} key{Fluss};

constraint fk_Muendung_Fluss_on_Fluss Muendung{Fluss} <= Fluss {Fluss};

//Created from a m:n relation
var sprechen real relation
{
    Land_Code char
,   Sprache_Sprache char
,   Prozentsatz char
}key{Land_Code,Sprache_Sprache};

constraint fk_sprechen_Land_on_Land_Code (sprechen rename {Land_Code as Code}) {Code} <= Land {Code};

constraint fk_sprechen_Sprache_on_Sprache_Sprache (sprechen rename {Sprache_Sprache as Sprache}) {Sprache} <= Sprache {Sprache};

//Created from a m:n relation
var gehoert real relation
{
    Land_Code char
,   Ethnische_Gruppe_Ethnische_Gruppe char
,   Prozentsatz char
}key{Land_Code,Ethnische_Gruppe_Ethnische_Gruppe};

constraint fk_gehoert_Land_on_Land_Code (gehoert rename {Land_Code as Code}) {Code} <= Land {Code};

constraint fk_gehoert_Ethnische_Gruppe_on_Ethnische_Gruppe_Ethnische_Gruppe (gehoert rename {Ethnische_Gruppe_Ethnische_Gruppe as Ethnische_Gruppe}) {Ethnische_Gruppe} <= Ethnische_Gruppe {Ethnische_Gruppe};

//Created from a m:n relation
var glauben real relation
{
    Land_Code char
,   Religion_Religion char
,   Prozentsatz char
}key{Land_Code,Religion_Religion};

constraint fk_glauben_Land_on_Land_Code (glauben rename {Land_Code as Code}) {Code} <= Land {Code};

constraint fk_glauben_Religion_on_Religion_Religion (glauben rename {Religion_Religion as Religion}) {Religion} <= Religion {Religion};

//Created from a m:n relation
var umfasst real relation
{
    Land_Code char
,   Kontinent_Kontinent char
,   Prozentsatz char
}key{Land_Code,Kontinent_Kontinent};

constraint fk_umfasst_Land_on_Land_Code (umfasst rename {Land_Code as Code}) {Code} <= Land {Code};

constraint fk_umfasst_Kontinent_on_Kontinent_Kontinent (umfasst rename {Kontinent_Kontinent as Kontinent}) {Kontinent} <= Kontinent {Kontinent};

//Created from a m:n relation
var istMitglied real relation
{
    Land_Code char
,   Organisation_Abkuerzung char
,   Typ char
}key{Land_Code,Organisation_Abkuerzung};

constraint fk_istMitglied_Land_on_Land_Code (istMitglied rename {Land_Code as Code}) {Code} <= Land {Code};

constraint fk_istMitglied_Organisation_on_Organisation_Abkuerzung (istMitglied rename {Organisation_Abkuerzung as Abkuerzung}) {Abkuerzung} <= Organisation {Abkuerzung};

//Created from a m:n relation
var Grenze real relation
{
    Land_Code char
,   Land_Code2 char
,   Laenge char
}key{Land_Code,Land_Code2};

constraint fk_Grenze_Land_on_Land_Code (Grenze rename {Land_Code as Code}) {Code} <= Land {Code};

constraint fk_Grenze_Land_on_Land_Code2 (Grenze rename {Land_Code2 as Code}) {Code} <= Land {Code};

//Created from a m:n relation
var nahe real relation
{
    Stadt_Code char
,   Stadt_Provinz char
,   Stadt_Stadt char
,   Flughafen_IATACode char
}key{Stadt_Code,Stadt_Provinz,Stadt_Stadt,Flughafen_IATACode};

constraint fk_nahe_Stadt_on_Stadt_Code (nahe rename {Stadt_Code as Code}) {Code} <= Stadt {Code};

constraint fk_nahe_Stadt_on_Stadt_Provinz (nahe rename {Stadt_Provinz as Provinz}) {Provinz} <= Stadt {Provinz};

constraint fk_nahe_Stadt_on_Stadt_Stadt (nahe rename {Stadt_Stadt as Stadt}) {Stadt} <= Stadt {Stadt};

constraint fk_nahe_Flughafen_on_Flughafen_IATACode (nahe rename {Flughafen_IATACode as IATACode}) {IATACode} <= Flughafen {IATACode};

//Created from a m:n relation
var Wueste_in_Provinz real relation
{
    Provinz_Code char
,   Provinz_Provinz char
,   Wueste_Wueste char
}key{Provinz_Code,Provinz_Provinz,Wueste_Wueste};

constraint fk_Wueste_in_Provinz_Provinz_on_Provinz_Code (Wueste_in_Provinz rename {Provinz_Code as Code}) {Code} <= Provinz {Code};

constraint fk_Wueste_in_Provinz_Provinz_on_Provinz_Provinz (Wueste_in_Provinz rename {Provinz_Provinz as Provinz}) {Provinz} <= Provinz {Provinz};

constraint fk_Wueste_in_Provinz_Wueste_on_Wueste_Wueste (Wueste_in_Provinz rename {Wueste_Wueste as Wueste}) {Wueste} <= Wueste {Wueste};

//Created from a m:n relation
var Berg_in_Provinz real relation
{
    Provinz_Code char
,   Provinz_Provinz char
,   Berg_Berg char
}key{Provinz_Code,Provinz_Provinz,Berg_Berg};

constraint fk_Berg_in_Provinz_Provinz_on_Provinz_Code (Berg_in_Provinz rename {Provinz_Code as Code}) {Code} <= Provinz {Code};

constraint fk_Berg_in_Provinz_Provinz_on_Provinz_Provinz (Berg_in_Provinz rename {Provinz_Provinz as Provinz}) {Provinz} <= Provinz {Provinz};

constraint fk_Berg_in_Provinz_Berg_on_Berg_Berg (Berg_in_Provinz rename {Berg_Berg as Berg}) {Berg} <= Berg {Berg};

//Created from a m:n relation
var Insel_in_Provinz real relation
{
    Provinz_Code char
,   Provinz_Provinz char
,   Insel_Insel char
}key{Provinz_Code,Provinz_Provinz,Insel_Insel};

constraint fk_Insel_in_Provinz_Provinz_on_Provinz_Code (Insel_in_Provinz rename {Provinz_Code as Code}) {Code} <= Provinz {Code};

constraint fk_Insel_in_Provinz_Provinz_on_Provinz_Provinz (Insel_in_Provinz rename {Provinz_Provinz as Provinz}) {Provinz} <= Provinz {Provinz};

constraint fk_Insel_in_Provinz_Insel_on_Insel_Insel (Insel_in_Provinz rename {Insel_Insel as Insel}) {Insel} <= Insel {Insel};

//Created from a m:n relation
var Meer_in_Provinz real relation
{
    Provinz_Code char
,   Provinz_Provinz char
,   Meer_Meer char
}key{Provinz_Code,Provinz_Provinz,Meer_Meer};

constraint fk_Meer_in_Provinz_Provinz_on_Provinz_Code (Meer_in_Provinz rename {Provinz_Code as Code}) {Code} <= Provinz {Code};

constraint fk_Meer_in_Provinz_Provinz_on_Provinz_Provinz (Meer_in_Provinz rename {Provinz_Provinz as Provinz}) {Provinz} <= Provinz {Provinz};

constraint fk_Meer_in_Provinz_Meer_on_Meer_Meer (Meer_in_Provinz rename {Meer_Meer as Meer}) {Meer} <= Meer {Meer};

//Created from a m:n relation
var Fluss_in_Provinz real relation
{
    Provinz_Code char
,   Provinz_Provinz char
,   Fluss_Fluss char
}key{Provinz_Code,Provinz_Provinz,Fluss_Fluss};

constraint fk_Fluss_in_Provinz_Provinz_on_Provinz_Code (Fluss_in_Provinz rename {Provinz_Code as Code}) {Code} <= Provinz {Code};

constraint fk_Fluss_in_Provinz_Provinz_on_Provinz_Provinz (Fluss_in_Provinz rename {Provinz_Provinz as Provinz}) {Provinz} <= Provinz {Provinz};

constraint fk_Fluss_in_Provinz_Fluss_on_Fluss_Fluss (Fluss_in_Provinz rename {Fluss_Fluss as Fluss}) {Fluss} <= Fluss {Fluss};

//Created from a m:n relation
var See_in_Provinz real relation
{
    Provinz_Code char
,   Provinz_Provinz char
,   See_See char
}key{Provinz_Code,Provinz_Provinz,See_See};

constraint fk_See_in_Provinz_Provinz_on_Provinz_Code (See_in_Provinz rename {Provinz_Code as Code}) {Code} <= Provinz {Code};

constraint fk_See_in_Provinz_Provinz_on_Provinz_Provinz (See_in_Provinz rename {Provinz_Provinz as Provinz}) {Provinz} <= Provinz {Provinz};

constraint fk_See_in_Provinz_See_on_See_See (See_in_Provinz rename {See_See as See}) {See} <= See {See};

//Created from a m:n relation
var Berg_auf_Insel real relation
{
    Insel_Insel char
,   Berg_Berg char
}key{Insel_Insel,Berg_Berg};

constraint fk_Berg_auf_Insel_Insel_on_Insel_Insel (Berg_auf_Insel rename {Insel_Insel as Insel}) {Insel} <= Insel {Insel};

constraint fk_Berg_auf_Insel_Berg_on_Berg_Berg (Berg_auf_Insel rename {Berg_Berg as Berg}) {Berg} <= Berg {Berg};

//Created from a m:n relation
var Insel_in_Meer real relation
{
    Insel_Insel char
,   Meer_Meer char
}key{Insel_Insel,Meer_Meer};

constraint fk_Insel_in_Meer_Insel_on_Insel_Insel (Insel_in_Meer rename {Insel_Insel as Insel}) {Insel} <= Insel {Insel};

constraint fk_Insel_in_Meer_Meer_on_Meer_Meer (Insel_in_Meer rename {Meer_Meer as Meer}) {Meer} <= Meer {Meer};

//Created from a m:n relation
var Insel_in_Fluss real relation
{
    Insel_Insel char
,   Fluss_Fluss char
}key{Insel_Insel,Fluss_Fluss};

constraint fk_Insel_in_Fluss_Insel_on_Insel_Insel (Insel_in_Fluss rename {Insel_Insel as Insel}) {Insel} <= Insel {Insel};

constraint fk_Insel_in_Fluss_Fluss_on_Fluss_Fluss (Insel_in_Fluss rename {Fluss_Fluss as Fluss}) {Fluss} <= Fluss {Fluss};

//Created from a m:n relation
var Insel_in_See real relation
{
    Insel_Insel char
,   See_See char
}key{Insel_Insel,See_See};

constraint fk_Insel_in_See_Insel_on_Insel_Insel (Insel_in_See rename {Insel_Insel as Insel}) {Insel} <= Insel {Insel};

constraint fk_Insel_in_See_See_on_See_See (Insel_in_See rename {See_See as See}) {See} <= See {See};

//Created from a m:n relation
var Flughafen_auf_Insel real relation
{
    Insel_Insel char
,   Flughafen_IATACode char
}key{Insel_Insel,Flughafen_IATACode};

constraint fk_Flughafen_auf_Insel_Insel_on_Insel_Insel (Flughafen_auf_Insel rename {Insel_Insel as Insel}) {Insel} <= Insel {Insel};

constraint fk_Flughafen_auf_Insel_Flughafen_on_Flughafen_IATACode (Flughafen_auf_Insel rename {Flughafen_IATACode as IATACode}) {IATACode} <= Flughafen {IATACode};

//Created from a m:n relation
var Stadt_bei_Meer real relation
{
    Stadt_Code char
,   Stadt_Provinz char
,   Stadt_Stadt char
,   Meer_Meer char
}key{Stadt_Code,Stadt_Provinz,Stadt_Stadt,Meer_Meer};

constraint fk_Stadt_bei_Meer_Stadt_on_Stadt_Code (Stadt_bei_Meer rename {Stadt_Code as Code}) {Code} <= Stadt {Code};

constraint fk_Stadt_bei_Meer_Stadt_on_Stadt_Provinz (Stadt_bei_Meer rename {Stadt_Provinz as Provinz}) {Provinz} <= Stadt {Provinz};

constraint fk_Stadt_bei_Meer_Stadt_on_Stadt_Stadt (Stadt_bei_Meer rename {Stadt_Stadt as Stadt}) {Stadt} <= Stadt {Stadt};

constraint fk_Stadt_bei_Meer_Meer_on_Meer_Meer (Stadt_bei_Meer rename {Meer_Meer as Meer}) {Meer} <= Meer {Meer};

//Created from a m:n relation
var Stadt_bei_Fluss real relation
{
    Stadt_Code char
,   Stadt_Provinz char
,   Stadt_Stadt char
,   Fluss_Fluss char
}key{Stadt_Code,Stadt_Provinz,Stadt_Stadt,Fluss_Fluss};

constraint fk_Stadt_bei_Fluss_Stadt_on_Stadt_Code (Stadt_bei_Fluss rename {Stadt_Code as Code}) {Code} <= Stadt {Code};

constraint fk_Stadt_bei_Fluss_Stadt_on_Stadt_Provinz (Stadt_bei_Fluss rename {Stadt_Provinz as Provinz}) {Provinz} <= Stadt {Provinz};

constraint fk_Stadt_bei_Fluss_Stadt_on_Stadt_Stadt (Stadt_bei_Fluss rename {Stadt_Stadt as Stadt}) {Stadt} <= Stadt {Stadt};

constraint fk_Stadt_bei_Fluss_Fluss_on_Fluss_Fluss (Stadt_bei_Fluss rename {Fluss_Fluss as Fluss}) {Fluss} <= Fluss {Fluss};

//Created from a m:n relation
var Stadt_bei_See real relation
{
    Stadt_Code char
,   Stadt_Provinz char
,   Stadt_Stadt char
,   See_See char
}key{Stadt_Code,Stadt_Provinz,Stadt_Stadt,See_See};

constraint fk_Stadt_bei_See_Stadt_on_Stadt_Code (Stadt_bei_See rename {Stadt_Code as Code}) {Code} <= Stadt {Code};

constraint fk_Stadt_bei_See_Stadt_on_Stadt_Provinz (Stadt_bei_See rename {Stadt_Provinz as Provinz}) {Provinz} <= Stadt {Provinz};

constraint fk_Stadt_bei_See_Stadt_on_Stadt_Stadt (Stadt_bei_See rename {Stadt_Stadt as Stadt}) {Stadt} <= Stadt {Stadt};

constraint fk_Stadt_bei_See_See_on_See_See (Stadt_bei_See rename {See_See as See}) {See} <= See {See};

//Created from a m:n relation
var muendet_in_See real relation
{
    Muendung_Fluss char
,   See_See char
}key{Muendung_Fluss,See_See};

constraint fk_muendet_in_See_Muendung_on_Muendung_Fluss (muendet_in_See rename {Muendung_Fluss as Fluss}) {Fluss} <= Muendung {Fluss};

constraint fk_muendet_in_See_See_on_See_See (muendet_in_See rename {See_See as See}) {See} <= See {See};

//Created from a m:n relation
var muendet_in_Fluss real relation
{
    Muendung_Fluss char
,   Fluss_Fluss char
}key{Muendung_Fluss,Fluss_Fluss};

constraint fk_muendet_in_Fluss_Muendung_on_Muendung_Fluss (muendet_in_Fluss rename {Muendung_Fluss as Fluss}) {Fluss} <= Muendung {Fluss};

constraint fk_muendet_in_Fluss_Fluss_on_Fluss_Fluss (muendet_in_Fluss rename {Fluss_Fluss as Fluss}) {Fluss} <= Fluss {Fluss};

//Created from a m:n relation
var muendet_in_Meer real relation
{
    Muendung_Fluss char
,   Meer_Meer char
}key{Muendung_Fluss,Meer_Meer};

constraint fk_muendet_in_Meer_Muendung_on_Muendung_Fluss (muendet_in_Meer rename {Muendung_Fluss as Fluss}) {Fluss} <= Muendung {Fluss};

constraint fk_muendet_in_Meer_Meer_on_Meer_Meer (muendet_in_Meer rename {Meer_Meer as Meer}) {Meer} <= Meer {Meer};

//Created from a m:n relation
var Quelle_in_Provinz real relation
{
    Quelle_Fluss char
,   Provinz_Code char
,   Provinz_Provinz char
}key{Quelle_Fluss,Provinz_Code,Provinz_Provinz};

constraint fk_Quelle_in_Provinz_Quelle_on_Quelle_Fluss (Quelle_in_Provinz rename {Quelle_Fluss as Fluss}) {Fluss} <= Quelle {Fluss};

constraint fk_Quelle_in_Provinz_Provinz_on_Provinz_Code (Quelle_in_Provinz rename {Provinz_Code as Code}) {Code} <= Provinz {Code};

constraint fk_Quelle_in_Provinz_Provinz_on_Provinz_Provinz (Quelle_in_Provinz rename {Provinz_Provinz as Provinz}) {Provinz} <= Provinz {Provinz};

//Created from a m:n relation
var Muendung_in_Provinz real relation
{
    Quelle_Fluss char
,   Muendung_Fluss char
}key{Quelle_Fluss,Muendung_Fluss};

constraint fk_Muendung_in_Provinz_Quelle_on_Quelle_Fluss (Muendung_in_Provinz rename {Quelle_Fluss as Fluss}) {Fluss} <= Quelle {Fluss};

constraint fk_Muendung_in_Provinz_Muendung_on_Muendung_Fluss (Muendung_in_Provinz rename {Muendung_Fluss as Fluss}) {Fluss} <= Muendung {Fluss};

//Created from a m:n relation
var Hauptsitz real relation
{
    Organisation_Abkuerzung char
,   Stadt_Code char
,   Stadt_Provinz char
,   Stadt_Stadt char
}key{Organisation_Abkuerzung,Stadt_Code,Stadt_Provinz,Stadt_Stadt};

constraint fk_Hauptsitz_Organisation_on_Organisation_Abkuerzung (Hauptsitz rename {Organisation_Abkuerzung as Abkuerzung}) {Abkuerzung} <= Organisation {Abkuerzung};

constraint fk_Hauptsitz_Stadt_on_Stadt_Code (Hauptsitz rename {Stadt_Code as Code}) {Code} <= Stadt {Code};

constraint fk_Hauptsitz_Stadt_on_Stadt_Provinz (Hauptsitz rename {Stadt_Provinz as Provinz}) {Provinz} <= Stadt {Provinz};

constraint fk_Hauptsitz_Stadt_on_Stadt_Stadt (Hauptsitz rename {Stadt_Stadt as Stadt}) {Stadt} <= Stadt {Stadt};

