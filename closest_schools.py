from k_means import k_means as km
import school_k as sk
from school_k import NoSchoolWithIDError
import numpy as np


def find_n_closest_schools(search_ID, data, n):
    """
    Given a search_ID, data (a list of tuples), and n, return a list of
    school IDs of schools that are the closest to the school represented
    by the search_ID. 'Close' is measured by the Euclidean distance between
    school data points.
    * RAISES NoSchoolWithIDError if the the school we are searching on is
    not in data
    """

    # prep the data
    search_ID_idx, id_list, X = sk._prep_k_data(search_ID, data)
    # find the distance from the search_ID to all other schools in
    # dataset X
    dist_list = [
        km.squared_distance(X[:, search_ID_idx], school) for school in X]
    print dist_list

    # return l_closest_schools
