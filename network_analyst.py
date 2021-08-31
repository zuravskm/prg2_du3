import sys
import fiona
import geopandas
import networkx as nx
import math
from pyproj import Transformer
import matplotlib.pyplot as plt
import json

def load_info():

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    start_lat = sys.argv[3]
    start_lon = sys.argv[4]
    end_lat = sys.argv[5]
    end_lon = sys.argv[6]

    # path Praha - Aš:
    """input_path = "data/silnice_data50_singl.shp"  #sys.argv[1]
    output_path = "data/output.geojson" #sys.argv[2]
    start_lat = 50.0864 #sys.argv[3] Praha
    start_lon = 14.4821 #sys.argv[4]
    end_lat = 50.2244 #sys.argv[5] Aš
    end_lon = 12.1839 #sys.argv[6]"""

    # holesovice
    """input_path = "data/testdata_utm.geojson"
    output_path = "data/output.geojson" #sys.argv[2]
    start_lat = 50.103246 #sys.argv[3] 
    start_lon = 14.455911 #sys.argv[4]
    end_lat = 50.102948 #sys.argv[5]
    end_lon = 14.442816 #sys.argv[6]"""

    # holesovice 2
    """input_path = "data/testdata_utm.geojson"
    output_path = "data/output.geojson" #sys.argv[2]
    start_lat = 50.103600774 #sys.argv[3]
    start_lon = 14.4436590254 #sys.argv[4]
    end_lat = 50.1009953013 #sys.argv[5]
    end_lon = 14.4529370504 #sys.argv[6]"""

    # input path to file
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

def wgs2cartestian(gdf_o, start, end):
    used_crs = gdf_o.crs
    used_crs != "epsg:4326"
    transformer = Transformer.from_crs("epsg:4326", used_crs, always_xy=True)
    #print(used_crs)
    start = list(transformer.transform(start[1], start[0]))
    end = list(transformer.transform(end[1], end[0]))
    return start, end

def save_output(line, targed_file):
    line_string = {
      "type": "Feature",
      "properties": {"type": "shortest_path"},
      "geometry": {
        "type": "LineString",
        "coordinates": line
      }     
    }
    gj_structure = {"type":"FeatureCollection"}
    gj_structure["features"] = [line_string]

    # save output geojson file:
    try:
        with open(targed_file, "w", encoding = "utf-8") as f:
            json.dump(gj_structure,f, indent = 2)
    except FileNotFoundError:
        print("Inappropriate path to output file.")
        quit()
    except PermissionError:
        print("Inappropriate path to output file. Can't write to given directory, permission denied.")
        quit()

###########################################################################

# load and check data
print("Loading input data...")
given_info = load_info() # zde je entice s overenymi vstupnimi udaji
print("Data loaded.")
gdf_object = given_info[0]
path_output = given_info[1]
coords_start = given_info[2:4]
coords_end = given_info[4:6]

print("Reprojecting GPS coordinates...")
# reproject input points from wgs84 to the same coordinate system as given roads vector data
start_reprojected, end_reprojected = wgs2cartestian(gdf_object, coords_start, coords_end)
print("Coordinates reprojected.")

print("Creating graph...")
first_iter = True
# create graph
G = nx.Graph()
# iterator
for idx,r in gdf_object.iterrows():
    # Remember last point for creating edges
    try:
        mempoint = r.geometry.coords[0]
    except NotImplementedError:
        print("Data contains multipart geometries, which is not supported. Please, export yout data as single part geometry.")
        quit()

    if first_iter:
        start_nearest = mempoint#list(G.nodes)[0]
        end_nearest = mempoint#list(G.nodes)[0]

        start_dist = math.hypot((start_reprojected[0]-start_nearest[0]),(start_reprojected[1]-start_nearest[1]))
        end_dist = math.hypot((end_reprojected[0]-end_nearest[0]),(end_reprojected[1]-end_nearest[1]))

        first_iter = False

    first_inner_iter = True
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

        # find nearest point on graph for start and end point
        if first_inner_iter: # just for first iteration
            start_test = math.hypot((start_reprojected[0]-mempoint[0]),(start_reprojected[1]-mempoint[1]))
            end_test = math.hypot((end_reprojected[0]-mempoint[0]),(end_reprojected[1]-mempoint[1]))
            
            if (start_test < start_dist):
                start_nearest = mempoint
                start_dist = start_test

            if (end_test < end_dist):
                end_nearest = mempoint
                end_dist = end_test
            
            start_test = math.hypot((start_reprojected[0]-r.geometry.coords[0][0]),(start_reprojected[1]-r.geometry.coords[0][1]))
            end_test = math.hypot((end_reprojected[0]-r.geometry.coords[0][0]),(end_reprojected[1]-r.geometry.coords[0][1]))
            
            if (start_test < start_dist):
                start_nearest = r.geometry.coords[0]
                start_dist = start_test

            if (end_test < end_dist):
                end_nearest = r.geometry.coords[0]
                end_dist = end_test

            first_inner_iter = False

        else: # for any other iteration
            start_test = math.hypot((start_reprojected[0]-mempoint[0]),(start_reprojected[1]-mempoint[1]))
            end_test = math.hypot((end_reprojected[0]-mempoint[0]),(end_reprojected[1]-mempoint[1]))
            
            if (start_test<start_dist):
                start_nearest = mempoint
                start_dist = start_test

            if (end_test<end_dist):
                end_nearest = mempoint
                end_dist = end_test
print("Graph created.")

print("Finding shortest path...")
# compute shortest path
try:
    path_line = nx.shortest_path(G, start_nearest, end_nearest, weight='length')
except nx.exception.NetworkXNoPath:
    print("Can't find path between selected points. Road network is not connected between them.")
    quit()
print("Path found...")

print("Saving output...")
# build and save GeoJson:
save_output(path_line, path_output)
print("Output saved.")

"""### pro kontrolu vykresleni cesty do grafu
memnode = path_line[0]
for v in path_line[1:]:
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
plt.show()"""

print("Succesfully executed. :-)")
