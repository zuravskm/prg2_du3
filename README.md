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
Dokumentace ke konzolové aplikaci pro vyhledání nejkratší cesty mezi dvěma body. Aplikace využívá knihovny pro práci s geodaty: NetworkX a GeoPandas.

#### Vstupy
Funkční rozhranní konzolové aplikace je: `network_analyst.py --net <vstupni_soubor> --out <vystupni_soubor> --from <lat> <lon> --to <lat> <lon>`. Program má tedy celkem 6 vstupů, jejichž načtení a kontrolu provádí funkce `load_data`. V případě, že jsou zadány vstupy chybně (neplatná cesta k souboru, chybně zadané souřadnice), program vypíše chybovou hlášku a skončí.  

#### Data
Potřebným formátem vstupních dat je .shp nebo .geojson. Souřadnice počátečního a koncového bodu cesty se zadávají v zeměpisných souřadnicích.

Jako testová data byly použity dvě datové sady: 
- síť silnic (soubor silnice_data50_singl.shp),
- síť ulic (testdata_utm.geojson). 

#### Nalezení nejbližších bodů na síti


#### Hledání nejkratší cesty
Pomocí funkce `shortest_path` z knihovny NetworkX je nalezena nejkratší cesta mezi zadanými body. Pokud taková cesta neexistuje (může nastat v případě, že nejbližší body na síti k zadaným bodům nejsou propojeny zadanou silniční sítí), program vypíše informaci o chybě a ukončí se. 

#### Uložení výstupu
Výstupem je nalezená nejkratší cesta, která je uložena jako GeoJSON. Ukládání provádí funkce `save_output()`...
