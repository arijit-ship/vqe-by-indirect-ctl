from constraints import create_time_constraints

def test_create_time_constraints() -> None:
    res = create_time_constraints(3, 6)
    # assert(res, [])