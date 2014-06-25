import pytest
import pandas as pd
import closest_schools as cs


@pytest.fixture(scope="module")
def data_tuples():
    scData = pd.DataFrame.from_csv('test_data/k_nrml_demographics_data.txt')
    ids = scData[:]['School_ID'].values
    enroll = scData[:]['NRML_Enroll'].values
    lowSES = scData[:]['Low_SES'].values
    tuples = [(ids[i], enroll[i], lowSES[i]) for i in range(len(ids))]
    return tuples


def test_pick_n_easy_data():
    ids = [425, 9381, 1533, 1231, 2, 45]
    dist = [0.023, 1.23, 3.44, 8.45, 9.2, 10]
    fake_data = zip(ids, dist)
    top_n = cs._pick_n(4, fake_data)
    assert top_n == [425, 9381, 1533, 1231]


def test_pick_n_repetitive_data_at_end():
    ids = [6, 5, 2, 1, 8]
    dist = [1, 2, 2, 2, 2]
    fake_data = zip(ids, dist)
    top_n = cs._pick_n(3, fake_data)
    assert top_n == [6, 5, 2, 1, 8]


def test_pick_n_all_repetitive_data():
    ids = [6, 5, 2, 1, 8]
    dist = [2, 2, 2, 2, 2]
    fake_data = zip(ids, dist)
    top_n = cs._pick_n(3, fake_data)
    assert top_n == [6, 5, 2, 1, 8]


def test_pick_n_repetitive_data_middle():
    ids = [6, 5, 2, 1, 8]
    dist = [1, 3, 3, 3, 5]
    fake_data = zip(ids, dist)
    top_n = cs._pick_n(3, fake_data)
    assert top_n == [6, 5, 2, 1]


def test_closest_schools(data_tuples):
    search_id = 1605
    print cs.find_n_closest_schools(search_id, data_tuples, 10)
