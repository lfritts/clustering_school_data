import k_means as km
# import school_k as sk
from school_k import NoSchoolWithIDError
import numpy as np


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


def _prep_data(search_ID, data):
    """
    used for prepping the data for closest_schools.  Input is:
    * search_ID
    * data (a list of tuples). The first element of the tuple is always the
    building id for the school represented in the data in the rest of the
    tuple.
    * returns (search_ID_data, id_list, data_array) The search_ID_data,
    A list of the school ids, and a numpy array of the data passed in through
    the tuple. The search_ID will not be in the returned id_list or data_array
    * RAISES a NoSchoolWithIDError Exception if search_ID not in data

    """
    # annoying, but to use np.vstack the array has to be initialized with
    # the same dimensions of data, so let's initialize with the first
    # school and then move on.

    # search_ID_idx is used to check if search_ID was in data, and also to
    # help speed up lookup later
    search_ID_data = None
    iter_data = iter(data)
    first_school = next(iter_data)
    # skip adding the search school, and store it's data to return later
    if search_ID == first_school[0]:
        search_ID_data = first_school[1:]
        first_school = next(iter_data)
    id_list = [first_school[0]]
    data_array = np.array(first_school[1:])
    # build the id list and the data array
    for school in iter_data:
        # print "school is {}".format(school)
        # skip adding the search school
        if search_ID == school[0]:
            search_ID_data = school[1:]
            continue
        # grab the first item in the tuple, the id
        id_list.append(school[0])
        # grab the rest of the tuple, the data
        data_array = np.vstack([data_array, school[1:]])

    # raise an error if search_ID not in data
    if search_ID_data is None:
        raise NoSchoolWithIDError()

    return (search_ID_data, id_list, data_array)


def find_n_closest_schools(search_ID, data, n):
    """
    Given a search_ID, data (a list of tuples), and n, return a list of
    school IDs of schools that are the closest to the school represented
    by the search_ID. 'Close' is measured by the distance between
    school data points.
    * RAISES NoSchoolWithIDError if the the school we are searching on is
    not in data.
    * If user calls calls function with n greater than the number of schools,
    * the function will truncate n to the number of schools.
    * If a user calls the function with n < 1, it will raise a ValueError
    """
    data_len = len(data)
    # check the input
    if n < 1:
        raise ValueError("find_n_closest_schools called with n<1")
    # reduce n if necessary
    elif n > data_len:
        # needs to be data_len - 1 because we will remove the search school
        # from the data before passing it to _pick_n()
        n = data_len - 1

    # prep the data sk._prep_data raises Error if search_ID not in data
    search_ID_data, id_list, X = _prep_data(search_ID, data)

    # find the distance from the search_ID to all other schools in
    # dataset X
    dist_list = [
        km.squared_distance(search_ID_data, school) for school in X]

    # join the id_list and the dist_list
    # sort the list by distance from search_ID school
    # the pure python way
    dist_list = zip(id_list, dist_list)
    dist_list = sorted(dist_list, key=lambda school: school[1])
    # the numpy way (which we won't use because it converts int ids to float
    # dist_list = np.vstack((id_list, dist_list)).T
    # dist_list = dist_list[dist_list[:, 1].argsort()]

    # pick the first n items from the sorted data
    return _pick_n(n, dist_list)
