import numpy as np
import k_means as km


def _prep_k_data(data):
    """
    used for prepping the data for find_schools_in_cluster.
    Input
    * data (a list of tuples). The first element of the tuple is always the
    building id for the school represented in the data in the rest of the
    tuple.
    * returns id_list, data_array
        -a list of the school ids, and
        - a numpy array of the data
    """
    # init numpy array data_array to all zeros - probably faster than vstack
    num_schools = len(data)
    num_features = len(data[0]) - 1
    id_list = []
    data_array = np.zeros((num_schools, num_features))
    # build the id list and the data array
    for i, school in enumerate(data):
        id_list.append(school[0])
        data_array[i] = school[1:]
    return id_list, data_array


def parallel_find_best_school_clusters(
        data, K=5, tol=0, max_iters=60, num_runs=5, debug=False):
    pass


def find_best_school_clusters(
        data, K=5, tol=0, max_iters=60, num_runs=5, debug=False):
    """
    find_best_school_clusters takes
    * data (a list of tuples). The first element of the tuple is always the
    building id for the school represented in the data in the rest of the
    tuple.
    * K, the number of clusters the data will be grouped into, by default 5.
    * tol is the tolerance for a convergence test that stops iterations.
    * max_iters is the number of iterations K-means algorithm uses to update
    centroids. Defaults to 5.
    * num_runs is the number of times this method runs K-means and chooses
    the lowest cost run of them.
    Returns a list of lists. The outer list contains K inner lists, one
      for each cluster.  Each inner list contains the school ids of
      schools in a given cluster.
    """
    id_list, X = _prep_k_data(data)
    # do K-Means num_runs times, updating best run when necessary
    best_cluster_idx = None
    best_centroids = None
    lowest_cost = float('inf')
    for run in range(num_runs):
        cost, cluster_idx, centroids = get_k_run_results(X, K, max_iters, tol)
        if cost < lowest_cost:
            best_cluster_idx = cluster_idx
            lowest_cost = cost
            best_centroids = centroids
            if debug:
                print_debug_info_and_pause(
                    run, cost, centroids, lowest_cost, best_centroids)
    # find the schools in each cluster and build the return list
    return build_clusters(id_list, best_cluster_idx, K)


def get_k_run_results(X, K, max_iters, tol):
    init_centroids = km.init_centroids(X, K)
    centroids, cluster_idx = km.run_k_means(X, init_centroids, max_iters, tol)
    cost = km.cost(centroids, X, cluster_idx)
    return cost, cluster_idx, centroids


def build_clusters(ids, cluster_idx, K):
    """builds a list of lists, where each inner list is a cluster
    containing the ids of schools in that cluster"""
    return_list = [[] for k in xrange(K)]  # initialize the list of lists
    for school_idx, cluster in enumerate(cluster_idx):
        return_list[cluster].append(ids[school_idx])
    return return_list


def print_debug_info_and_pause(
        run, cost, centroids, lowest_cost, best_centroids):
        print "K-Means Run {} done."
        print "Cost for run {0} is {1} with centroids:".format(run, cost)
        print centroids
        print "Best centroids so far are:".format(run)
        print best_centroids
        print "With cost: {}".format(lowest_cost)
        raw_input("Press enter to continue...")
