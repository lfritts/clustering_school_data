import pytest
import pandas as pd
import closest_schools as cs
from school_k import NoSchoolWithIDError


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


@pytest.fixture(scope="module")
def high_school_and_demo_tuples():
    scData = pd.DataFrame.from_csv('test_data/highschools.csv')
    ids = scData[:]['School_ID'].values
    enroll = scData[:]['NRML_Enroll'].values
    lowSES = scData[:]['Low_SES'].values
    per_native = scData[:]['per_native'].values
    per_asian = scData[:]['per_asian'].values
    per_PI = scData[:]['per_PI'].values
    per_API = scData[:]['per_API'].values
    per_black = scData[:]['per_black'].values
    per_hispanic = scData[:]['per_hispanic'].values
    per_migrant = scData[:]['per_migrant'].values
    per_bil = scData[:]['per_bil'].values
    per_sped = scData[:]['per_sped'].values
    tuples = [(
        ids[i], enroll[i], lowSES[i], per_native[i], per_asian[i], per_PI[i],
        per_API[i], per_black[i], per_hispanic[i], per_migrant[i], per_bil[i],
        per_sped[i]) for i in range(len(ids))]
    return tuples


def test_prep_data_Error(full_data_tuples):
    # 1111 is not in the data
    search_ID = 1111
    with pytest.raises(NoSchoolWithIDError):
        cs._prep_data(search_ID, full_data_tuples)


def test_prep_data(full_data_tuples):
    # Edmonds Challenge Elementary ID is 1520
    search_ID = 1520
    tuples = cs._prep_data(search_ID, full_data_tuples)
    assert tuples[0] == (13.03571429, 6.21)
    # Wa He Lut Indian Elementary ID is 8407
#    print tuples[1][2304]
    assert tuples[1][2303] == 8407
    # Wa He Lut % low SES is 7.27
    assert tuples[2][2303][1] == 7.27


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
    assert len(results) == 9
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


def test_find_n_closest_schools_mini_small_big(mini_big_and_small_data_tuples):
    # results are interesting, look at excel file
    # test_data/k_mini_big_and_small_nrml_demographics_data_RESULTS.xlsx
    # reason that we get 11 results back.
    search_id = 5961
    results = cs.find_n_closest_schools(
        search_id, mini_big_and_small_data_tuples, 10)
    assert len(results) == 11
    assert 1767 in results
    assert 4178 in results
    assert 4225 in results
    assert 5113 in results
    assert 5280 in results
    assert 5283 in results
    assert 1880 in results
    assert 4433 in results
    assert 1603 in results
    assert 1960 in results
    assert 5062 in results
    assert 5961 not in results


def test_many_dimension_data(hi_d_high_school_and_demo_tuples):
    search_ID = 5164
    results = cs.find_n_closest_schools(
        search_ID, hi_d_high_school_and_demo_tuples, 20)
    print "results are: \n"
    print results
    assert len(results) == 20
    assert 5164 not in results


def test_find_n_closest_schools_n_too_big(mini_big_and_small_data_tuples):
    # results are interesting, look at excel file
    # test_data/k_mini_big_and_small_nrml_demographics_data_RESULTS.xlsx
    # reason that we get 11 results back.
    search_id = 5961
    results = cs.find_n_closest_schools(
        search_id, mini_big_and_small_data_tuples, 50)
    assert len(results) == 19
    assert 5961 not in results
    assert 1767 in results
    assert 4178 in results
    assert 4225 in results
    assert 5113 in results
    assert 5280 in results
    assert 5283 in results
    assert 1880 in results
    assert 4433 in results
    assert 1603 in results
    assert 1960 in results
    assert 5062 in results
    assert 5111 in results
    assert 2415 in results
    assert 3640 in results
    assert 2272 in results
    assert 4523 in results
    assert 2134 in results
    assert 2797 in results
    assert 5164 in results


def test_closest_schools(full_data_tuples):
    # search on Seattle Pathfinder Elementary
    # actual results calculated in excel spreadsheet
    search_id = 1620
    results = cs.find_n_closest_schools(search_id, full_data_tuples, 5)
    assert len(results) == 5
    assert 2256 in results
    assert 2964 in results
    assert 4537 in results
    assert 3002 in results
    assert 3561 in results
    assert 1620 not in results
