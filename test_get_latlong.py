from get_latlong import get_latlong


def test_get_latlong_for_school():
    record = {'City': 'Aberdeen',
              'District name': 'Aberdeen School District',
              'ZipCode': '98520-5510',
              'Lowest Grade': 'PK',
              'School Code': '2834',
              'phone': '360.538.2131',
              'State': 'Washington',
              'AddressLine2': '',
              'AddressLine1': '1801 Bay Ave.',
              'District-County Code': '14005',
              'Principal Name': "William O'Donnell",
              'ESD Name': 'Educational Service District 113',
              'School Type': 'Public School',
              'Highest Grade': '6',
              'School name': 'A J West Elementary',
              'ESD Code': '34801'}
    actual = get_latlong(record)
    expected_lat = '46.971922'
    expected_long = '-123.838252'
    assert actual['Lat'] == expected_lat
    assert actual['Long'] == expected_long


def test_get_latlong_notfound():
    # create bad address, zip to generate NotFound message
    record = {'City': 'Aberdeen',
              'District name': 'Aberdeen School District',
              'ZipCode': 'asdfkjaf',
              'Lowest Grade': 'PK',
              'School Code': '2834',
              'phone': '360.538.2131',
              'State': 'Washington',
              'AddressLine2': '',
              'AddressLine1': 'adjfhlkajdshf',
              'District-County Code': '14005',
              'Principal Name': "William O'Donnell",
              'ESD Name': 'Educational Service District 113',
              'School Type': 'Public School',
              'Highest Grade': '6',
              'School name': 'A J West Elementary',
              'ESD Code': '34801'}
    actual = get_latlong(record)
    expected = 'NotFound'
    assert actual['Lat'] == expected
    assert actual['Long'] == expected
