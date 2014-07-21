import numpy as np
import k_means as km


def _prep_k_data(data):
    """
    used for prepping the data for find_schools_in_cluster.
    Input
    * data (a list of tuples). The first element of the tuple is always the
    building id for the school represented in the data in the rest of the
    tuple.
    * returns (id_list, data_array)
        -a list of the school ids, and
        - a numpy array of the data
    """
    # initialize numpy array data_array to all zeros - probably faster than
    # vstack
    num_schools = len(data)
    num_features = len(data[0]) - 1
    id_list = []
    data_array = np.zeros((num_schools, num_features))
    # build the id list and the data array
    for i, school in enumerate(data):
        id_list.append(school[0])
        data_array[i] = school[1:]
    return id_list, data_array


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

    # find_closest_centroids one more time on the average centroid locations
    # idx = km.find_closest_centroids(X, avg_cents)
