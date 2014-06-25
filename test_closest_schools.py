import pytest
import pandas as pd
import closest_schools as cs


@pytest.fixture(scope="module")
def full_data_tuples():
    scData = pd.DataFrame.from_csv('test_data/k_nrml_demographics_data.csv')
    ids = scData[:]['School_ID'].values
    enroll = scData[:]['NRML_Enroll'].values
    lowSES = scData[:]['Low_SES'].values
    tuples = [(ids[i], enroll[i], lowSES[i]) for i in range(len(ids))]
    return tuples


@pytest.fixture(scope="module")
def small_data_tuples():
    scData = pd.DataFrame.from_csv(
        'test_data/k_nrml_small_demographics_data.csv')
    ids = scData[:]['School_ID'].values
    enroll = scData[:]['NRML_Enroll'].values
    lowSES = scData[:]['Low_SES'].values
    tuples = [(ids[i], enroll[i], lowSES[i]) for i in range(len(ids))]
    return tuples


@pytest.fixture(scope="module")
def mini_big_and_small_data_tuples():
    scData = pd.DataFrame.from_csv(
        'test_data/k_mini_big_and_small_nrml_demographics_data.csv')
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


def test_find_n_closest_schools_small(small_data_tuples):
    # search on the one very small school
    search_id = 5113
    results = cs.find_n_closest_schools(search_id, small_data_tuples, 9)
    assert 3588 in results
    assert 3533 in results
    assert 5071 in results
    assert 5049 in results
    assert 4470 in results
    assert 3496 in results
    assert 1903 in results
    assert 1763 in results
    assert 1950 in results
    assert 5113 not in results


def test_closest_schools(full_data_tuples):
    search_id = 1605
    print cs.find_n_closest_schools(search_id, full_data_tuples, 10)
