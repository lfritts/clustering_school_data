import os
import csv
import requests


def read_address_file(filename):
    """
    Read tab delimited text file containing school addresses and call
    get_latlong function to add latitude/longitude to each.
    """

    rec_list = []
    with open(filename) as address_file:
        reader = csv.DictReader(address_file, delimiter='\t')
        for row in reader:
            row['LatLong'] = get_latlong(row['School name'] + ' ' +
                                         row['ZipCode'])
            rec_list.append(row)
    return rec_list


def get_latlong(address):
    """
    Use google maps api to get latitude/longitude from school name +
    zipcode lookup.
    """
    api_url = 'http://maps.googleapis.com/maps/api/geocode/json'
    parameters = {'sensor': 'false',
                  'address': address}
    resp = requests.get(api_url, params=parameters)
    data = resp.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return (location['lat'], location['lng'])
    else:
        return 'NotFound'


def write_address_file(filename, rec_list):
    """
    Write updated address info to tab delimited text file.
    """
    header = rec_list[0].keys()
    with open(filename, 'w') as out_file:
        out_file.write('{}\n'.format('\t'.join(header)))
        for record in rec_list:
            out_file.write('{}\n'.format('\t'.join(record.values())))


if __name__ == '__main__':
    base_dir = os.getcwd() + '/raw_data/'
    print "\nReads tab delimited text file containing address information"
    print 'and queries Google Maps api for latitude/longitude information.'
    print 'Text file should be placed in raw_data folder'
    inputfile = raw_input('\n\nPlease enter the filename: ')
    write_address_file(base_dir + 'addresses.txt',
                       read_address_file(base_dir + inputfile))
    print '\nOutput has been written to raw_data/addresses.txt'
