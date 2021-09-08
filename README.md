# Vyhledávač cest
## Uživatelská dokumentace
Program umí vyhledat cestu mezi 2 body v zadaných datech. Výslednou nejkratší cestu uloží jako *.GeoJSON. Pro spuštění programu stačí zavolat:
  `network_analyst.py --net "vstupni_soubor" --out "vystupni_soubor" --from lat lon --to lat lon`, kde `"input_path"` je cesta ke vstupnímu souboru, `"output_path"` cesta k výstupnímu souboru a `star_lat` `star_lon` `end_lat` `end_lon` jsou počáteční a koncový bod zadaný s pomocí zeměpisných souřadnic ve WGS-84. Při výpočtu nejbližší trasy je uvažována vzdálenost mezi lomovými body silnic. 

#### Poznámka 1: 
Při zadání vstupních dat silnic ve WGS-84 v zeměpisných souřadnicích jsou tato data automaticky převeda do WGS-84 Web Mercator (EPSG 3857). V tomto CRS je i výstupní GeoJSON. 
#### Poznámka 2: 
Program nepodporuje multipart geometrii. Pokud Vaše data obsahují multipart linie, převeďte je např. v QGISu všechny na singlepart.
#### Poznámka 3: 
Výsledný geojson soubor nemá explicitně vepsán souřadnicový systém. Souřadnicový systém ve výstupním geojsonu je stejný jako ve vstupních liniových datech, při vizualizaci např. v QGISu je nutné nejdřív určit použitý CRS --> Layer CRS --> Set layer CRS.
#### Poznámka 4:
Na konci skriptu je zakomentována část kódu pro vykreslování grafu s nalezenou cestou s pomocí knihovny matplotlib. Vykreslování je nevhodné pro velké datové sady, pro menší je  možno kód odkomentovat a graf s cestou vykreslit. 

## Vývojářská dokumentace
Dokumentace ke konzolové aplikaci pro vyhledání nejkratší cesty mezi dvěma body. Aplikace využívá knihovny pro práci s geodaty: NetworkX, GeoPandas, Proj a další.

#### Vstupy
Funkční rozhranní konzolové aplikace je: `network_analyst.py --net "vstupni_soubor" --out "vystupni_soubor" --from lat lon --to lat lon`. Program má tedy celkem 6 vstupů, jejichž načtení a kontrolu provádí funkce `parse_data()`, `load_info()`. V případě, že jsou zadány vstupy chybně (neplatná cesta k souboru, chybně zadané souřadnice), program vypíše chybovou hlášku a skončí. Toto chování zajišťuje několik bloků s výjimkami. Vstupy můžou být v libovolném pořadí.

#### Další funkce
`wgs2cartesian(gdf_o, start, end)`
Funkce převede počáteční a koncový bod ve WGS84 do stejného souřadnicového systému, v jakém jsou vektorová data silnic. 

`save_output(line, targed_file)`
Zde je jednak vytvořena struktura výstupního geojson souboru a následně je tento soubor s výstupní linií uložen. 

#### Funkcionalita skriptu
Skript nejprve načte vstupy od uživatele s pomocí funkcí `parse_data()`, `load_info()`. Následně převede počáteční a koncový bod z WGS84 do stejného souř. systému v jakém je vrstva silnic. Pokud je vstupní vrstva silnic ve WGS-84, pak jsou data automaticky převedena do WGS-84 Web Mercator. Poté je vytvořen graf a ve 2 vnořených `for` cyklech je iterováno přes jednotlivé linie a jejich body. Při tom jsou z bodů vytvářeny hrany, které jsou přidávány do grafu. Zároveň jsou hledány nejbližší body v grafu `(start_nearest, end_nearest)` k transformovanému počátečnímu a koncovému bodu, které zadá uživatel `(start_reprojected, end_reprojected)`. Pomocí funkce `shortest_path()` z knihovny NetworkX je nalezena nejkratší cesta mezi zadanými body. Pokud taková cesta neexistuje (může nastat v případě, že nejbližší body na síti k zadaným bodům nejsou propojeny zadanou silniční sítí), program vypíše informaci o chybě a ukončí se. Výstupem je nalezená nejkratší cesta, která je uložena jako GeoJSON. Ukládání provádí funkce `save_output()`.

#### Data
Potřebným formátem vstupních dat je *.shp nebo *.GeoJSON. Souřadnice počátečního a koncového bodu cesty se zadávají v zeměpisných souřadnicích (pro ukázku testových bodů jsou jejich souřadnice uvedeny ve skriptu jako komentáře na řádcích 19-41).

Jako testová data byly použity dvě různě velké datové sady: 
- větší datová sada - síť silnic (soubor silnice_data50_singl.shp) - výřez silnic z Dat 50 (poskytuje ČUZK),
- menší datová sada - síť ulic (testdata_utm.geojson) - výřez silnic z dat OpenStreetMap (získaná s pomocí Overpass turbo),
- menší datová sada - síť ulic (testdata_wgs84.geojson) - výřez silnic z dat OpenStreetMap (získaná s pomocí Overpass turbo).
