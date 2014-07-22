import os
import csv
from IPython import parallel


def read_address_file(filename):
    """
    Read tab delimited text file containing school addresses and call
    get_latlong function to add latitude/longitude to each.
    """

    rec_list = []
    with open(filename) as address_file:
        reader = csv.DictReader(address_file, delimiter='\t')
        for row in reader:
            rec_list.append(row)
    return rec_list


def get_latlong(record):
    """
    Use google maps api to get latitude/longitude from school name +
    zipcode lookup.
    """
    import requests
    api_url = 'http://maps.googleapis.com/maps/api/geocode/json'
    # Used school name and zip as first pass
    # parameters = {'sensor': 'false',
    #               'address': (record['School name'] + ' ' + record['ZipCode'])}
    # Better choice is address1 and zip. School name/zip will still be needed
    # for schools with only PO Box.
    parameters = {'sensor': 'false',
                  'address': (record['AddressLine1'] + ' ' + record['ZipCode'])}
    resp = requests.get(api_url, params=parameters)
    data = resp.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        record['Lat'] = str(location['lat'])
        record['Long'] = str(location['lng'])
    else:
        record['Lat'] = 'NotFound'
        record['Long'] = 'NotFound'
    return record


def multiprocess_latlong(rec_list):
    """
    Use IPython parallel processing to farm out api requests. Requires
    starting clusters in a separate terminal
    (use ipcluster start -n <num_clusters> from cli).
    """
    # Watch for hitting download/second limits. Dial back number of
    # clusters as needed. Also may hit gross limit for API calls (2500/24hr)
    clients = parallel.Client()
    lview = clients.load_balanced_view()
    lview.block = True
    result = lview.map(get_latlong, rec_list)
    return result


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
    record_list = multiprocess_latlong(read_address_file(base_dir + inputfile))
    write_address_file(base_dir + 'addresses.txt',
                       record_list)
    print '\nOutput has been written to raw_data/addresses.txt'
