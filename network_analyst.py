import sys
import fiona
import geopandas
import networkx as nx
import math
import matplotlib.pyplot as plt

def load_info():
    input_path = "A:/skola_uk/8_SEMESTR/prg_II/ukol3/data/silnice_data50.shp"  #sys.argv[1] ve finalnim skriptu zde budou argumenty z prikazovy radky -- sys.argv 
    output_path = "cesta k vystupnimu souboru" #sys.argv[2]
    start_lat = 10 #sys.argv[3] definice bodů, zemepisna sirka a delka...
    start_lon = 10 #sys.argv[4]
    end_lat = 10 #sys.argv[5]
    end_lon = 10 #sys.argv[6]
    
    # souradnice bodu primo na ceste
    # start_lat = 50.1035841276 #sys.argv[3] definice bodů, zemepisna sirka a delka...
    # start_lon = 14.4434777766 #sys.argv[4]
    # end_lat = 50.1009957377 #sys.argv[5]
    # end_lon = 14.4527108553 #sys.argv[6]

    # souradnice bodu mimo cestu
    # start_lat = 50.103600774 #sys.argv[3] definice bodů, zemepisna sirka a delka...
    # start_lon = 14.4436590254 #sys.argv[4]
    # end_lat = 50.1009953013 #sys.argv[5]
    # end_lon = 14.4529370504 #sys.argv[6]

    # input paths to files
    try:
        input = geopandas.read_file(input_path)
    except fiona.errors.DriverError:
        print("Inappropriate path to input file.")
        quit()

    # test coordinates
    try:
        if (float(start_lat) > 90) or (float(start_lat) < -90) or (float(end_lat) > 90) or (float(end_lat) < -90):
            print("Inappropriate latitude input. Program is over.")
            quit()

        if (float(start_lon) > 180) or (float(start_lon) < -180) or (float(end_lon) > 180) or (float(end_lon) < -180):
            print("Inappropriate longitude input. Program is over.")
            quit()
    except ValueError:
        print("Inappropriate number input. Use integer of float for latitude and longitude.")
        quit()

    return (input, output_path, start_lat, start_lon, end_lat, end_lon)

###########################################################################

### nacteni a kontrola dat
given_info = load_info() # zde je entice s overenymi vstupnimi udaji
# print(given_info)

gdf_object = given_info[0]
# print(gdf_object)
output = given_info[1]
coords_start = given_info[2:4]
# print("start", coords_start)
coords_end = given_info[4:6]
# print("end", coords_end)


### vytvoreni grafu
G = nx.Graph()

# iterace
for idx,r in gdf_object.iterrows():
    coords = r.geometry.coords
    # Remember last point for creating edges
    mempoint = r.geometry.coords[0]
    # Add edges (starting from second point, first we have in mempoint)
    for point in r.geometry.coords[1:]:
        # Point is a tuple containing coordinates -> it can be used as node name
        G.add_edge(mempoint,point)

        length = math.hypot((mempoint[0]-point[0]),(mempoint[1]-point[1]))

        # Add the index of the feature as edge attribute
        G.edges[mempoint,point]['index'] = idx

        G.edges[mempoint,point]['length'] = length

        # Update the last point
        mempoint = point

        
### nalezeni nejblizsiho uzlu zadanym bodum
# point = list(G.nodes)[0] 
# print(point)


### hledani nejkratsi cesty
start_point = list(G.nodes)[0] # zde bude nejblizsi bod z predchoziho vypoctu
end_point = list(G.nodes)[20] # zde bude nejblizsi bod z predchoziho vypoctu

# vypocet nejkratsi cesty
path = nx.shortest_path(G, start_point, end_point, weight='length')


### pro kontrolu vykresleni cesty do grafu
memnode = path[0]
for v in path[1:]:
    G.edges[(memnode, v)]['path'] = True
    memnode = v

edgecolors = []
for e in G.edges:
    if 'path' in G.edges[e]:
        edgecolors.append('r')
    else:
        edgecolors.append('k')

# logicke usporadani/vykresleni grafu
pos = {n:n for n in G.nodes}

# vykresleni grafu
nx.draw(G, pos=pos, edge_color=edgecolors)
plt.show()
