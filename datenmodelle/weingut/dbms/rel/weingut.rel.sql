//Database Weingut

//Created from <ent>
var wein real relation
{
    name char
,   farbe char
,   jahrgang char
,   restsuesse char
,   erzeuger char
} key{name};

//Created from <ent>
var erzeuger real relation
{
    name char
,   adresse char
,   lizenznummer char
,   mengewein char
,   anbaugebiet char
} key{name};

//Created from <ent>
var anbaugebiet real relation
{
    name char
,   region char
,   land char
}key{};

//Created from <ent>
var rebsorte real relation
{
    name char
,   farbe char
,   anteil char
}key{};

//Created from <ent>
var lizenz real relation
{
    lizenznummer char
,   menge char
}key{};

//Created from a m:n relation
var erzeugt real relation
{
    erzeuger_name char
,   wein_name char
}key{erzeuger_name,wein_name};

constraint fk_erzeugt_erzeuger_on_erzeuger_name (erzeugt rename {erzeuger_name as name}) {name} <= erzeuger {name};

constraint fk_erzeugt_wein_on_wein_name (erzeugt rename {wein_name as name}) {name} <= wein {name};

//Created from a m:n relation
var beinhaltet real relation
{
    wein_name char
,   anteil char
} key{wein_name};

constraint fk_beinhaltet_wein_on_wein_name (beinhaltet rename {wein_name as name}) {name} <= wein {name};

