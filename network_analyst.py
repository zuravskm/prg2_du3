import sys
import fiona
import geopandas

def load_info():
    input_path = "A:/skola_uk/8_SEMESTR/prg_II/ukol3/data/silnice_data50.shp"  #sys.argv[1] ve finalnim skriptu zde budou argumenty z prikazovy radky -- sys.argv 
    output_path = "cesta k vystupnimu souboru" #sys.argv[2]
    start_lat = 10 #sys.argv[3] definice bodů, zemepisna sirka a delka...
    start_lon = 10 #sys.argv[4]
    end_lat = 10 #sys.argv[5]
    end_lon = 10 #sys.argv[6]

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
given_info = load_info() # zde je entice s overenymi vstupnimi udaji
print(given_info)

