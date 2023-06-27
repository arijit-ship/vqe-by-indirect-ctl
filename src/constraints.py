import numpy as np
from scipy.optimize import LinearConstraint


def create_time_constraints(time_params_length, all_params_length) -> LinearConstraint:
    """Create constraints for time params. As parameter list includes params of
    theta, we have to create constraints of the same length.

    The rule of constraints are like following.
    t_{i} - t_{i-1} >= 0, t_{i-1} - t_{i-2} >= 0, ... t_{2} - t_{1} >= 0, t_{1} >= 0
    Therefore, when time_params_length is 4 and all_params_length is 8, the matrix is
        [[ 1. -1.  0.  0.  0.  0.  0.  0.]
        [ 0.  1. -1.  0.  0.  0.  0.  0.]
        [ 0.  0.  1. -1.  0.  0.  0.  0.]
        [ 0.  0.  0.  1.  0.  0.  0.  0.]]
    time_params_length equals `depth + 1`
    because we need to set before and after times for each time evolution.
    """
    matrix = np.array([])
    for i in range(time_params_length):
        for j in range(time_params_length):
            if i == j:
                matrix = np.append(matrix, 1)
            elif j == i + 1:
                matrix = np.append(matrix, -1)
            else:
                matrix = np.append(matrix, 0)

    matrix = np.hstack(
        (
            matrix.reshape(time_params_length, time_params_length),
            np.zeros((time_params_length, all_params_length - time_params_length)),
        )
    )
    return LinearConstraint(matrix, 0, np.inf)
