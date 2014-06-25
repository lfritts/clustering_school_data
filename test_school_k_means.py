import pandas as pd
import school_k as k
from school_k import NoSchoolWithIDError
# import numpy as np
import pytest
slow = pytest.mark.slow

"""
Testing on the school_k module is limited as K-means itself was not the
best way to do what we needed to do for our school clustering app.  We
did, however, use the _prep_k_data function function that is part of
the k_means module, so that is tested here.
"""


@pytest.fixture(scope="module")
def data_tuples():
    scData = pd.DataFrame.from_csv('test_data/k_nrml_demographics_data.txt')
    ids = scData[:]['School_ID'].values
    enroll = scData[:]['NRML_Enroll'].values
    lowSES = scData[:]['Low_SES'].values
    tuples = [(ids[i], enroll[i], lowSES[i]) for i in range(len(ids))]
    return tuples


def test_prep_k_data_Error(data_tuples):
    # 1111 is not in the data
    search_ID = 1111
    with pytest.raises(NoSchoolWithIDError):
        k._prep_k_data(search_ID, data_tuples)


def test_prep_k_data(data_tuples):
    # Edmonds Challenge Elementary ID is 1520 in the data row 8
    search_ID = 1520
    tuple = k._prep_k_data(search_ID, data_tuples)
    assert tuple[0] == 8
    assert tuple[1][8] == search_ID
    # below is third in tuple, 8th row, first column enrollment
    assert tuple[2][8][0] == 13.03571429
    # Challenge Elementary % low SEs is 6.21
    assert tuple[2][8][1] == 6.21
    # Wa He Lut Indian Elementary ID is 8407
    assert tuple[1][2304] == 8407
    # Wa He Lut % low SES is 7.27
    assert tuple[2][2304][1] == 7.27

"""
# for some reason this slow test runs all the time???
@slow
def test_find_schools_in_cluster(data_tuples):
    # hardcode a real id for Concrete Twin Cedars High
    search_id = 1605
    # print k.find_schools_in_cluster(search_id, data_tuples)
    k.find_schools_in_cluster(
        search_id, data_tuples, K=10, tol=0)
"""
