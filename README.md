# Vyhledávač cest
Rosťa: Ahoj, 
vzdhledem k tomu, že zítra se s vámí nemůžu spojit, tak jsem lehce začal, abych vám na zítra aspoň něco předpřipravil :D Je to jen maličkost. Je tam jedna funkce, která ověřuje, jestli je vstup od uživatele validní. Ve funkci se nejprve načte vstup od uživatele (teď tam jsou napevno nastavený hodnoty, ve finále tam bude sys.argv[neco]), a pak ověří jestli je zem. sirka a delka ve spravnem intervalu -90 az 90 a -180 az 180, zaroven overi, jestli jsou to cisla. Zaroven otevre vstupni data (sit komunikaci) a open overuje, jestli je validni cesta k nim, aby skript nespadl, ale inteligentne se kdyztak ukoncil. to je vse zatim :D 
funkce vraci entici, ve ktery je otevrana vstupni sit komunikaci jako geopandas objekt, pres ktery vam uz pujde iterovat, pak tam je cesta k vystupnimu souboru a nakonec overeny souradnice. s udajema, ktery jsou v ty entici bych dal pracoval. 
Cestu k vystupnimu souboru bych overoval az pri ukladani. 
Good luck, ja se k vam pridam a budu se snazit byti uzitecnym. :D klidne mi toho nechte hodne a neco tezkyho :D 

Markéta: Update - přidaly jsme tvorbu grafu, výpočet nejkratší cesty; funguje vykreslení grafu, logické uspořádání grafu (asi jen pro naši kontrolu, když děláme konzolovou variantu aplikace). 


Dále k řešení 
- nalezení nejbližších bodů na síti zadaným bodům (skoro hotovo, ale ve funkci se mi nedaří setřídit slovník, nevim proč, nefunguje mi fce sort -- kdyby někoho napadlo, proč tomu tak je, budu ráda :) nebo kdyby někoho napadlo elegantnější řešení... Anička našla např. [zde](https://stackoverflow.com/questions/61304137/finding-the-closest-coordinates-to-a-point?noredirect=1&lq=1), mně se ale nějak nepovedlo udělat něco podobného v našem skriptu)
- export vysledné cesty do GeoJSON -- našla jsem k tomu např. [odkaz](https://networkx.org/documentation/stable/reference/readwrite/json_graph.html)
- bonusy :)


Testová data jsou v souboru testdata.geojson (jsou to data Holešovic ze cvičení :) ).


Poznámka z hodiny - říkal, že pokud budeme chtít řešit jako bonus i orientovaný graf (jednosměrky), bude to za 2 b, pak už to ale asi zapomněl připsat do zadání. :)


([odkaz na zadání](https://github.com/xtompok/prg2_20/tree/main/du03))

([odkaz na záznamy cvičení](https://owncloud.cesnet.cz/index.php/s/8VzyWaUv9LI4LYG))

