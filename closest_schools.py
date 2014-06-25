import k_means as km
import school_k as sk
# import numpy as np


def _pick_n(n, sd_array):
    """
    * n is the number of school ids to return.
    * sd_array is a sorted list of 2-tuples, the first element is
    the school id, the second element is the squared_distance from the search
    school.  Sorted by distance from the search school.
    take the closest n schools (ignore first! it's your search school)
    IF there are schools with equal distances and this pushes you over n
    schools, then only allow one tie to push you over. E.g. if n = 10, and we
    have a 10 schools with the same, 4th ranked closest distance, we'll get
    all 10 of those tied schools and the first 3, but no more.
    returns the school_id of closest 'n' schools.
    """
    top_n = []
    array_len = len(sd_array)
    i = 0
    while i < n:
        top_n.append(sd_array[i][0])
        i += 1
        while i < array_len and (sd_array[i-1][1] == sd_array[i][1]):
            top_n.append(sd_array[i][0])
            i += 1
    return top_n


def find_n_closest_schools(search_ID, data, n):
    """
    Given a search_ID, data (a list of tuples), and n, return a list of
    school IDs of schools that are the closest to the school represented
    by the search_ID. 'Close' is measured by the Euclidean distance between
    school data points.
    * RAISES NoSchoolWithIDError if the the school we are searching on is
    not in data.
    * If user calls calls function with n greater than the number of schools,
    * the function will truncate n to the number of schools.
    * If a user calls the function with n < 1, it will raise a ValueError
    """
    # check the input
    if n < 1:
        raise ValueError("find_n_closest_schools called with n<1")
    # reduce n if necessary
    elif n > len(data):
        n = len(data)

    # prep the data sk._prep_k_data raises Error if search_ID not in data
    search_ID_idx, id_list, X = sk._prep_k_data(search_ID, data)

    # find the distance from the search_ID to all other schools in
    # dataset X
    dist_list = [
        km.squared_distance(X[search_ID_idx, :], school) for school in X]

    # join the id_list and the dist_list
    # sort the list by distance from search_ID school
    # the pure python way
    dist_list = zip(id_list, dist_list)
    dist_list = sorted(dist_list, key=lambda school: school[1])
    # the numpy way (which we won't use because it converts int ids to float
    # dist_list = np.vstack((id_list, dist_list)).T
    # dist_list = dist_list[dist_list[:, 1].argsort()]

    # take all but the first item in the dist_list (that is the distance to the
    # school you're searching on, 0)
    return _pick_n(n, dist_list[1:][:])
