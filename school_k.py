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


def find_school_clusters(data, K=5, tol=0, max_iters=60, num_runs=5):
    """
    find_schools_in_cluster will take a
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

    - returns a list of lists. The outer list contains K inner lists, one
      for each cluster.  Each inner list contains the school ids of
      schools in a given cluster.
    """
    id_list, X = _prep_k_data(data)
    # do K-Means num_runs times, updating best run when necessary
    # best_centroids = None
    best_idx = None
    lowest_cost = float('inf')
    for i in range(num_runs + 1):
        # print "In run {}\n".format(i)
        init_centroids = km.init_centroids(X, K)
        centroids, idx = km.run_k_means(X, init_centroids, max_iters, tol)
        cost = km.cost(centroids, X, idx)
        print "Cost for run {0} is {1}\n".format(i, cost)
        if cost < lowest_cost:
            # best_centroids = centroids
            best_idx = idx
            lowest_cost = cost
        # print "K-Means Run {} finished. Best centroids so far are:".format(i)
        # print best_centroids
        # print "With cost: {}".format(lowest_cost)
        # raw_input("Press enter to continue...")

    # for each centroid, find the schools in that cluster and build the
    # return list
    return_list = [[] for cluster in xrange(K)]  # initialize the list of lists
    for school, cluster in enumerate(best_idx):
        return_list[cluster].append(id_list[school])
    return return_list
    # for i, cluster in enumerate(return_list):
    #     print "Schools in cluster {}:".format(i)
    #     print cluster
