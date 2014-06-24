import pytest
import pandas as pd
import school_k as k
# import numpy as np


@pytest.fixture(scope="module")
def data_tuples():
    scData = pd.DataFrame.from_csv('test_data/k_nrml_demographics_data.txt')
    ids = scData[:]['School_ID'].values
    enroll = scData[:]['NRML_Enroll'].values
    lowSES = scData[:]['Low_SES'].values
    tuples = [(ids[i], enroll[i], lowSES[i]) for i in range(len(ids))]
    return tuples


def test_find_schools_in_cluster(data_tuples):
    # hardcode a real id for Concrete Twin Cedars High
    search_id = 1605
    # print k.find_schools_in_cluster(search_id, data_tuples)
    k.find_schools_in_cluster(
        search_id, data_tuples, K=10, tol=0)
