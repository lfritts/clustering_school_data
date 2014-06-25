import pytest
import numpy as np
import numpy.testing as np_testing
import k_means as km


@pytest.fixture(scope="module")
def X_data():
    X = np.loadtxt('test_data/k_test_dataset2.csv', delimiter=',')
    return X


@pytest.fixture("module")
def correct_idx():
    idx = np.loadtxt('test_data/k_test_index_values.csv')
    # print idx
    return idx


@pytest.fixture("module")
def dummy_centroids():
    centroids = np.array([[3., 3.], [6., 2.], [8., 5.]])
    return centroids


@pytest.fixture("module")
def correct_centroids():
    centrds = np.array([[1.9540, 5.0256], [3.0437, 1.0154], [6.0337, 3.0005]])
    return centrds


def test_run_k_means(
        X_data, dummy_centroids, correct_centroids, correct_idx):
    """
    this test checks the centroids found against a known working algorithm and
    the results it produces.  Do not alter the number of iterations as it may
    not find the same answer.
    """
    ans_cent, ans_idx = km.run_k_means(X_data, dummy_centroids, 10)
    np_testing.assert_allclose(
        ans_cent, correct_centroids, 1e-4, 0, "Arrays not close enough")
    np_testing.assert_array_equal(ans_idx, correct_idx, "Arrays not equal")
