import numpy as np
from numpy.random import random_sample as rand


def squared_distance(x1, x2):
    """
    Where x1 and x2 are two Numpy arrays, returns
    the squared distance ||x2-y(i)||^2 between the
    two vectors x1 and x2.
    """
    return np.sum(np.square(np.subtract(x1, x2)))


def find_closest_centroids(X, centroids):
    """
    Each row in dataset X is a single example.
    Returns a vector idx of centroid assignments for each example.
    I.e. idx = m x 1 and each entry in idx in range [1..K]
    """
    X = X.astype(float)
    K = centroids.shape[0]
    m = X.shape[0]
    idx = np.zeros(m)
    # loop over m training examples
    for i in range(m):

        # initialize lowest_distance to
        # squared_distance(X[i][:], centroids[0][:])
        distance = squared_distance(X[i][:], centroids[0][:])
        lowest_distance = distance
        idx[i] = 0

        for k in range(1, K):
            """
            calculate distance to each centroid, if distance is lower than
            current min, stored in idx[k] then update idx[k] to new min.
            """
            distance = squared_distance(X[i][:], centroids[k][:])

            """
            if distance is ==, pick a random centroid of the two,
            otherwise if distance < lowest_distance, update
            lowest_distance <- distance and idx[i] <- k
            """
            if ((distance == lowest_distance) and (np.round(rand()) == 1)) or (
                    distance < lowest_distance):
                lowest_distance = distance
                idx[i] = k
    return idx


def init_centroids(X, K):
    """
    Initializes K centroids that are to be used in K-Means on dataset X.
    """
    X = X.astype(float)
    # create a random permutation of the indices of each vector in X
    rand_idx = np.random.permutation(X.shape[0])
    # take the first K of the random indexed samples
    return X[rand_idx[0:K]]


def compute_centroids(X, idx, K):
    """
    returns the new centroids by computing the means of the data points
    assigned to each centroid.  Given data set X where each ro is a single
    data point, a vector idx of centroid assignents (each entry in range [1..K]
    for each example, and K the number of centroids.  Return a matrix of
    centroids, where each row of centroids is the mean of data points
    assigned to it.
    """
    X = X.astype(float)
    (m, n) = X.shape

    centroids = np.zeros((K, n))
    # idxLogical is K x m logical matrix, where each value
    # is True or False depending if example m is part of cluster k.
    idxLogical = np.zeros((K, m))

    # loop over centroids and set row to T/F depending on
    # membership in cluster k.
    for k in range(K):
        idxLogical[k] = (idx == k)

    # compute the new centroids, which are the averages of the points in
    # each cluster
    # Note:  [:,np.newaxis] turns idxLogical into column vector
    centroids = np.dot(idxLogical, X) / np.sum(idxLogical, 1)[:, np.newaxis]

    return centroids


def cost(centroids, X, idx):
    """returns the cost of a given clustering"""
    # calculate distance between example in X and it's assigned cluster
    # cost = 0.
    # m, n = X.shape
    # for i, row in enumerate(X[:]):
    #     centroid = centroids[idx[i]]
    #     cost += squared_distance(row, centroid)
    # return cost / m

    # Is it really this simple?
    m, _ = X.shape
    return squared_distance(X[:], centroids[idx]) / float(m)


def run_k_means(X, initial_centroids, max_iters, tol=0):

    print "Running K-Means Clustering\n"
    # print "Our Dataset X"
    # print X

    # grab K from initial_centroids dimensions
    K, dimensions = initial_centroids.shape

    # print "{0} clusters, K, and {1} Iterations.".format(K, max_iters)

    # start with the initial centroids
    centroids = initial_centroids
    for i in range(max_iters):
        last_centroids = centroids
        idx = find_closest_centroids(X, centroids)
        centroids = compute_centroids(X, idx, K)
        if squared_distance(centroids, last_centroids) <= tol:
            print "covergence at {0} iterations, instead of max of {1}".format(
                i, max_iters)
            break

        # print centroids
        # raw_input("Press enter to continue...")

    print "K-Means is done. \n\n"

    # the return will change to:
    # return centroids, idx, cost

    return (centroids, idx)
