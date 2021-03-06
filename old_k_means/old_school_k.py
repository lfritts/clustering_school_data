import numpy as np
import k_means as km


class NoSchoolWithIDError(Exception):

    def __init__(self, message="search_ID supplied is not in data"):
        Exception.__init__(self, message)


def _prep_k_data(search_ID, data):
    """
    used for prepping the data for find_schools_in_cluster.  Input is:
    * search_ID
    * data (a list of tuples). The first element of the tuple is always the
    building id for the school represented in the data in the rest of the
    tuple.
    * returns (search_ID_idx, id_list, data_array) The index of the search_ID
    in the data, a list of the school ids, and a numpy array of the data
    passed in through the tuple
    * RAISES a NoSchoolWithIDError Exception if search_ID not in data

    """
    # annoying, but to use np.vstack the array has to be initialized with
    # the same dimensions of data, so let's initialize with the first
    # school and then move on.

    # search_ID_idx is used to check if search_ID was in data, and also to
    # help speed up lookup later
    search_ID_idx = -1
    iter_data = iter(data)
    first_school = next(iter_data)
    if search_ID == first_school[0]:
        search_ID_idx = 0
    id_list = [first_school[0]]
    data_array = np.array(first_school[1:])
    # build the id list and the data array
    i = 1
    for school in iter_data:
        # print "school is {}".format(school)
        # grab the first item in the tuple, the id
        if search_ID == school[0]:
            search_ID_idx = i
        i += 1
        id_list.append(school[0])
        data_array = np.vstack([data_array, school[1:]])

    # raise an error if search_ID not in data
    if search_ID_idx == -1:
        raise NoSchoolWithIDError()

    return (search_ID_idx, id_list, data_array)


def avg_centroids(cents):
    """
    takes a list of centroids (as numpy arrays) and returns the
    element-wise mean of them, returned as a single numpy array.
    """
    return np.mean(np.array([cent for cent in cents]), axis=0)


def find_schools_in_cluster(
        search_ID, data, K=5, tol=0, max_iters=60, num_runs=5):
    """
    find_schools_in_cluster will take a
    * search_ID
    * data (a list of tuples). The first element of the tuple is always the
    building id for the school represented in the data in the rest of the
    tuple.
    * K, the number of clusters the data will be grouped into, by default 5.
    * tol is the tolerance for a convergence test.  In the update step, if the
    new centroids squared distance from the previous centroids is less than or
    equal to the tol, K-means will stop iterating.
    * max_iters is the number of iterations K-means algorithm uses to update
    centroids. Defaults to 5.
    * num_runs is the number of times this method runs K-means and chooses
    the lowest cost run of them.

    Returns a list of school building ids from same cluster as search_ID

    Raises NoSchoolWithIDError if search_ID is not in data.
    """
    (search_ID_idx, id_list, X) = _prep_k_data(search_ID, data)
    # feed data to k_means multiple times, storing centroid results
    result_centroids_list = []
    for i in range(num_runs):
        # print "In run {}\n".format(i)
        init_centroids = km.init_centroids(X, K)
        centroids, _ = km.run_k_means(X, init_centroids, max_iters, tol)
        # sort the centroids on first column
        centroids = centroids[centroids[:, 0].argsort()]
        result_centroids_list.append(centroids)
        # print "K-Means Run {0} finished.  Centroids are:".format(i)
        # print centroids
        # raw_input("Press enter to continue...")

    # TODO
    # WE NEED TO FIND THE RUN WITH
    # THE LOWEST COST, NOT THE AVERAGE!!!
    # average centroid locations
    avg_cents = avg_centroids(result_centroids_list)
    # print "Average Centroids are:"
    # print avg_cents

    # find_closest_centroids one more time on the average centroid locations
    idx = km.find_closest_centroids(X, avg_cents)

    # find what cluster search_ID school is in
    search_cluster = idx[search_ID_idx]

    # build list of ids of schools in same cluster
    """
    cluster_schools = []
    for i in range(len(idx)):
        if search_cluster == idx[i]
        cluster_schools.append(id_list[i])
    """
    clustered_IDs = [
        id_list[i] for i in range(len(idx)) if idx[i] == search_cluster
        ]
    # print "Clustered IDs:"
    # print clustered_IDs
    # print "Number of schools in cluster is {}".format(len(clustered_IDs))
    return clustered_IDs
