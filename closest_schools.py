import k_means as km
import school_k as sk
# import numpy as np


def pick_n(n, school_distance_array):
    """
    take the closest n schools (ignore first! it's your search school)
    IF there are schools with equal distances and this pushes you over n
    schools, then only allow one tie to push you over. E.g. if n = 10, and we
    have a 10 schools with the same, 4th ranked closest distance, we'll get
    all 10 of those tied schools and the first 3, but no more.
    returns
    """
    top_n = []
    i = 0
    while i < n:
        top_n.append(school_distance_array[i])
        i += 1
        while school_distance_array[i-1] == school_distance_array[i]:
            top_n.append(school_distance_array[i])
            i += 1
    return top_n


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
        km.squared_distance(X[search_ID_idx, :], school) for school in X]
    # join the id_list and the dist_list
    # sort the list by distance from search_ID school
    # the pure python way
    dist_list = zip(id_list, dist_list)
    dist_list = sorted(dist_list, key=lambda school: school[1])
    # the numpy way (which we won't use because it converts int ids to float
    # dist_list = np.vstack((id_list, dist_list)).T
    # dist_list = dist_list[dist_list[:, 1].argsort()]
    print "\ndist_list after sorting"
    print dist_list

    # take all but the first item in the dist_list (that is the distance to the
    # school you're searching on, 0)
    return pick_n(n, dist_list[1:][:])
