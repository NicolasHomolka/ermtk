//Database Fluggesellschaften

//Created from <ent>
var BoardKarte real relation
{
    fnr char
,   datum char
,   abflughafen char
,   ankunftsflughafen char
,   name char
,   sitz char
} key{fnr};

//Created from <ent>
var Passagier real relation
{
    fnr char
,   pnr char
,   name char
,   anrede char
,   titel char
}key{fnr,pnr};

constraint fk_Passagier_BoardKarte_on_fnr Passagier{fnr} <= BoardKarte {fnr};

//Created from <ent>
var Ticket real relation
{
    fnr char
,   pnr char
,   tnr char
,   ausgabedatum char
,   preis char
,   waehrung char
,   vertriebsbuero char
}key{fnr,pnr,tnr};

constraint fk_Ticket_Passagier_on_fnr Ticket{fnr} <= Passagier {fnr};

constraint fk_Ticket_Passagier_on_pnr Ticket{pnr} <= Passagier {pnr};

//Created from <ent>
var Flugzeugtyp real relation
{
    typidentifikation char
,   hersteller char
,   reichweite char
} key{typidentifikation};

//Created from <ent>
var Flugzeug real relation
{
    flugzeugnummer char
,   interregnummer char
,   name char
,   startDatum char
}key{flugzeugnummer,interregnummer};

//Created from <ent>
var Fluggesellschaft real relation
{
    orgCode char
,   name char
,   hauptsitz char
} key{orgCode};

//Created from <ent>
var Flughafen real relation
{
    flughafennr char
,   name char
,   stadt char
,   land char
,   kapazitaet char
} key{flughafennr};

//Created from a m:n relation
var Sitzplatz real relation
{
    BoardKarte_fnr char
,   Flugzeugtyp_typidentifikation char
,   klasse char
,   ort char
}key{BoardKarte_fnr,Flugzeugtyp_typidentifikation,klasse,ort};

constraint fk_Sitzplatz_BoardKarte_on_BoardKarte_fnr (Sitzplatz rename {BoardKarte_fnr as fnr}) {fnr} <= BoardKarte {fnr};

constraint fk_Sitzplatz_Flugzeugtyp_on_Flugzeugtyp_typidentifikation (Sitzplatz rename {Flugzeugtyp_typidentifikation as typidentifikation}) {typidentifikation} <= Flugzeugtyp {typidentifikation};

//Created from a m:n relation
var Flug real relation
{
    Ticket_fnr char
,   Ticket_pnr char
,   Ticket_tnr char
,   Fluggesellschaft_orgCode char
,   Flughafen_flughafennr char
}key{Ticket_fnr,Ticket_pnr,Ticket_tnr,Fluggesellschaft_orgCode,Flughafen_flughafennr};

constraint fk_Flug_Ticket_on_Ticket_fnr (Flug rename {Ticket_fnr as fnr}) {fnr} <= Ticket {fnr};

constraint fk_Flug_Ticket_on_Ticket_pnr (Flug rename {Ticket_pnr as pnr}) {pnr} <= Ticket {pnr};

constraint fk_Flug_Ticket_on_Ticket_tnr (Flug rename {Ticket_tnr as tnr}) {tnr} <= Ticket {tnr};

constraint fk_Flug_Fluggesellschaft_on_Fluggesellschaft_orgCode (Flug rename {Fluggesellschaft_orgCode as orgCode}) {orgCode} <= Fluggesellschaft {orgCode};

constraint fk_Flug_Flughafen_on_Flughafen_flughafennr (Flug rename {Flughafen_flughafennr as flughafennr}) {flughafennr} <= Flughafen {flughafennr};

