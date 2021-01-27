import pygeoip
import os
import pandas as pd
import argparse

def get_location(IPaddress, database_name='GeoLiteCity.dat'):

    assert type(IPaddress) == str, f'Expected string type. Got {type(IPaddress)}'
    
    path = os.path.join(os.getcwd(),database_name) 
    geobase = pygeoip.GeoIP(path)
    recordes = geobase.record_by_name(IPaddress) 
    longitude = recordes['longitude']
    latitude = recordes['latitude']
    coordinate = {'longitude':longitude, 'latitude':latitude}

    return coordinate

def main():
    # setup argument parsing
    parser = argparse.ArgumentParser(description='Passing argument via command line')

    # reading and storing the value for IPaddress
    parser.add_argument('--IPaddress', action = "store", dest = "IPaddress",
    required=True)

    get_args = parser.parse_args()
    IPaddress = get_args.IPaddress

    #check if IPaddress is none
    coordinate = None

    if IPaddress == None:
        print(parser.usage)
        exit(0)
    else:
    	try:
            coordinate = get_location(IPaddress)
    	except TypeError:
    		print('Error Available')
    return coordinate
    
    

if __name__ == '__main__':
    coordinate = main()
    # save the coordinate
    cor = pd.DataFrame(coordinate, index=[0])
    cor.to_csv(os.getcwd() + '/coordinate.csv')

