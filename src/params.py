import numpy as np
from scipy.optimize import Bounds


def _generate_random_time_params(min_time, max_time, num) -> np.ndarray:
    return np.random.uniform(min_time, max_time, num)


def _generate_random_bn_params(
    min_bn: float = -1.0, max_bn: float = 1.0, num: int = 1
) -> np.ndarray:
    return np.random.uniform(min_bn, max_bn, num)


def _generate_random_theta_params(num: int) -> np.ndarray:
    return np.random.random(num) * 1e-1


def create_init_params(config):
    """Create params for a parametric ciruit.

    Parameters are time, cn, r(gamma), bn
    time: 0 - max_time
    cn: 0 - 1
    r(gamma): 0 - 1
    bn: 0 - 1
    theta: 0 - 1
    Return [
        t1, t2, ... td, cn1, cn2, ... cnd,
        r1, r2, ..., rd, bn1, bn2, ..., bnd,
        theta1, ..., theatd * gate_set
    ]
    """
    n_qubits = config["n_qubits"]
    if config["gate"]["type"] == "direct":
        list_count = 2 * n_qubits * (config["depth"] + 1)
        return _generate_random_theta_params(list_count), None

    # init time
    init_params = np.array([])
    if config["gate"]["time"]["type"] == "random":
        init_params = _generate_random_time_params(
            config["gate"]["time"]["init"]["min_val"],
            config["gate"]["time"]["init"]["max_val"],
            config["depth"] + 1,
        )

    # append bn params if bn type is random
    if config["gate"]["bn"]["type"] == "random":
        init_params = np.append(
            init_params,
            _generate_random_bn_params(-1.0, 1.0, config["depth"] * n_qubits),
        )

    # append theta params
    init_theta_params = _generate_random_theta_params(
        config["gate"]["parametric_rotation_gate_set"] * config["depth"]
    )
    init_params = np.append(init_params, init_theta_params)

    # set bounds
    if config["gate"]["bounds"]:
        return init_params, create_bounds(n_qubits, config)

    return init_params, None


def create_bounds(n_qubits, config):
    t_min = np.array([config["gate"]["time"]["min_val"]] * (config["depth"] + 1))
    t_max = np.array([config["gate"]["time"]["max_val"]] * (config["depth"] + 1))
    bn_min = np.array([0.0] * config["depth"] * n_qubits)
    bn_max = np.array([1.0] * config["depth"] * n_qubits)
    theta_min = np.array(
        [-np.Inf] * (config["gate"]["parametric_rotation_gate_set"] * config["depth"])
    )
    theta_max = np.array(
        [np.Inf] * (config["gate"]["parametric_rotation_gate_set"] * config["depth"])
    )

    if config["gate"]["bn"]["type"] == "random":
        min_bounds = np.append(np.append(np.append(np.array([]), t_min), bn_min), theta_min)
        max_bounds = np.append(np.append(np.append(np.array([]), t_max), bn_max), theta_max)
    else:
        min_bounds = np.append(np.append(np.array([]), t_min), theta_min)
        max_bounds = np.append(np.append(np.array([]), t_max), theta_max)

    return Bounds(min_bounds, max_bounds)
