import numpy as np

matrixE = np.eye(10)
matrixA = np.array([0, 0, 0.00497, 0, 4.1, 0, 0, 0, 0, 0],
                   [0, 0, 1.946, 1.557, 0.0001, 8.846, 2.211, 1.327, 0.0001, 0],
                   [0, 0.018, 0, 9.08, 0.059, 0.009, 0.0003, 0.0004, 0, 0],
                   [0, 0, 1.605, 0, 0.0002, 4.012, 4.012, 0.008, 0, 0],
                   [0, 0, 2.67, 0, 0, 0, 1.256, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0.0001, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0.0002, 5.26, 0, 0],
                   [0, 0, 0, 0, 0, 0.0007, 0, 0, 0.001, 0],
                   [0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0])

matrixYnew = np.array([226000000],
                      [201000000],
                      [1620000000],
                      [430000000],
                      [96000000000],
                      [98000000],
                      [7250000],
                      [1900000],
                      [1000000],
                      []65200)

print((matrixE - matrixA)**-1 * matrixYnew)