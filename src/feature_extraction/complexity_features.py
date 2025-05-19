def estimate_complexity(loop_count, recursion, num_variables):
    time_complexity = 1 + loop_count + recursion * 2
    space_complexity = num_variables + loop_count
    return time_complexity, space_complexity