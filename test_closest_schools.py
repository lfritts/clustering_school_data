import pytest
import pandas as pd
import closest_schools as cs
# import numpy as np


@pytest.fixture(scope="module")
def data_tuples():
    scData = pd.DataFrame.from_csv('test_data/k_nrml_demographics_data.txt')
    ids = scData[:]['School_ID'].values
    enroll = scData[:]['NRML_Enroll'].values
    lowSES = scData[:]['Low_SES'].values
    tuples = [(ids[i], enroll[i], lowSES[i]) for i in range(len(ids))]
    return tuples


def test_closest_schools(data_tuples):
    search_id = 1605
    cs.find_n_closest_schools(search_id, data_tuples, 10)
