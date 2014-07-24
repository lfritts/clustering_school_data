import pandas as pd
import school_k as k
# import numpy as np
import pytest
import itertools
slow = pytest.mark.slow

"""
Testing on the school_k module is limited as K-means itself was not the
best way to do what we needed to do for our school clustering app.  We
did, however, use the _prep_k_data function function that is part of
the k_means module, so that is tested here.
"""


@pytest.fixture(scope="module")
def data_tuples():
    scData = pd.DataFrame.from_csv('test_data/k_nrml_demographics_data.csv')
    ids = scData[:]['School_ID'].values
    enroll = scData[:]['NRML_Enroll'].values
    lowSES = scData[:]['Low_SES'].values
    tuples = [(ids[i], enroll[i], lowSES[i]) for i in range(len(ids))]
    return tuples


def test_prep_k_data(data_tuples):
    id_list, data_array = k._prep_k_data(data_tuples)
    assert len(id_list) == 2305
    assert len(data_array) == 2305
    # Edmonds Challenge Elementary ID is 1520 in the data row 8
    assert id_list[8] == 1520
    # Challenge Elementary NRML_Enroll = 13.03571429
    assert data_array[8][0] == 13.03571429
    # Challenge Elementary % Low_SES = 6.21
    assert data_array[8][1] == 6.21
    # # Wa He Lut Indian Elementary ID is 8407
    assert id_list[2304] == 8407
    # Wa He Lut NRML_Enroll = 5.758928571
    assert data_array[2304][0] == 5.758928571
    # Wa He Lut % low SES is 7.27
    assert data_array[2304][1] == 7.27


def test_build_clusters():
    K = 4
    ids = [1, 2, 3, 4, 5, 6, 7, 8]
    cluster_idx = [0, 1, 1, 0, 1, 2, 1, 1]
    expected = [[1, 4], [2, 3, 5, 7, 8], [6], []]
    result = k.build_clusters(ids, cluster_idx, K)
    assert expected == result


def test_school_k_means(data_tuples):
    K = 5
    centroids, result_clusters = k.find_best_school_clusters(data_tuples, K=K)
    # check that we get correct number of school ids back
    num_schools = 0
    for cluster in result_clusters:
        num_schools += len(cluster)
    # check that we get correct number of clusters back
    assert len(result_clusters) == K
    assert num_schools == len(data_tuples)
    # check that each school id is only in one cluster
    for i in xrange(len(result_clusters)):
        this_cluster = result_clusters[i]
        other_clusters = result_clusters[:i] + result_clusters[i+1:]
        for school_id in this_cluster:
            for other_id in itertools.chain(*other_clusters):
                assert school_id != other_id
