from get_latlong import get_latlong


def test_get_latlong_for_school():
    address = 'Almira Elementary School 99103'
    actual = get_latlong(address)
    expected_lat = 47.7078193
    expected_long = -118.9408949
    assert actual[0] == expected_lat
    assert actual[1] == expected_long


def test_get_latlong_notfound():
    # create bad address to generate NotFound message
    address = 'akdjhfakdjsf'
    actual = get_latlong(address)
    expected = 'NotFound'
    assert actual == expected
