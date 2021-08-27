# Vyhledávač cest
## Uživatelská dokumentace
Program umí vyhledat cestu mezi 2 body v zadaných datech. Výslednou nejkratší cestu uloží jako .geojson. Pro spuštění programu stačí zavolat:
  `network_analyst.py --net <vstupni_soubor> --out <vystupni_soubor> --from <lat> <lon> --to <lat> <lon>`, kde *net* je vstupní soubor (.shp nebo .geojson) s vektorovou sítí silnic, *out* je výstupní geojson soubor s výslednou cestou a *from* a *to* jsou počáteční a koncový bod zadaný s pomocí zeměpisných souřadnic ve WGS84. Při výpočtu nejbližší trasy je uvažována vzdálenost mezi lomovými body silnic. 
#### Poznámka 1: 
Výpočet je vhodné provádět pouze na datech v rovinných X, Y souřadnicích, ne v zeměpisných souřadnicích.
#### Poznámka 2: 
Program nepodporuje multipart geometrii. Pokud Vaše data obsahují multipart linie, převeďte je např. v QGISu všechny na singlepart.
#### Poznámka 3: 
Výsledný geojson soubor nemá explicitně vepsán souřadnicový systém. Souřadnicový systém ve výstupním geojsonu je stejný jako ve vstupních liniových datech, při vizualizaci např. v QGISu je nutné nejdřív určit použitý CRS --> Layer CRS --> Set layer CRS.

## Vývojářská dokumentace
#### Vstupy


#### Data


#### Nalezení nejbližších bodů na síti


#### Hledání nejkratší cesty


#### Uložení výstupu

