#!/usr/bin/env python

def RNGenerator(r, rnseed, num_samples= 1000,steps=100):
    #print('Start simulation')
    import numpy as np
    from scipy.linalg import eigh, cholesky
    from scipy.stats import norm

    from pylab import plot, show, axis, subplot, xlabel, ylabel, grid

    np.random.seed(int(rnseed))
    [m, n] = r.shape
    # Choice of cholesky or eigenvector method.
    method = 'cholesky'
    # method = 'eigenvectors'


    # The desired covariance matrix.
    #r = np.array([
    #    [3.40, -2.75, -2.00],
    #    [-2.75, 5.50, 1.50],
    #    [-2.00, 1.50, 1.25]
    #])



    # We need a matrix `c` for which `c*c^T = r`.  We can use, for example,
    # the Cholesky decomposition, or the we can construct `c` from the
    # eigenvectors and eigenvalues.

    if method == 'cholesky':
        # Compute the Cholesky decomposition.
        c = cholesky(r, lower=True)
    else:
        # Compute the eigenvalues and eigenvectors.
        evals, evecs = eigh(r)
        # Construct c, so c*c^T = r.
        c = np.dot(evecs, np.diag(np.sqrt(evals)))
    y = []
    for i in range(0,steps):
        # Generate samples from three independent normally distributed random
        # variables (with mean 0 and std. dev. 1).
        x = norm.rvs(size=(n, num_samples))

        # Convert the data to correlated random variables.
        y.append(np.dot(c, x))

    #
    # Plot various projections of the samples.
    #
    '''
    subplot(2, 2, 1)
    plot(y[0], y[1], 'b.')
    ylabel('y[1]')
    axis('equal')
    grid(True)

    subplot(2, 2, 3)
    plot(y[0], y[2], 'b.')
    xlabel('y[0]')
    ylabel('y[2]')
    axis('equal')
    grid(True)

    subplot(2, 2, 4)
    plot(y[1], y[2], 'b.')
    xlabel('y[1]')
    axis('equal')
    grid(True)

    show()
    '''
    print('RNG done!')
    return y