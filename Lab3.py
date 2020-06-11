from RandomGenerator import get_random_sequence
import math

# F(x) = sqrt(x)/2
# f(x) = 1/(4sqrt(x))


def get_distribution_intervals(values, num_of_intervals):
    sorted_values = sorted(values)

    sequence_range = 4
    interval_length = sequence_range/num_of_intervals

    intervals = {}
    for i in range(num_of_intervals):
        intervals[interval_length*(i+1)] = sum(interval_length *
                                               i < value <= interval_length*(i+1) for value in sorted_values)

    return intervals, interval_length


def F(x):
    return math.sqrt(x)/2


def pearson(values, intervals, interval_step):
    p_star = []
    for interval, count in intervals.items():
        p_star.append(count/len(values))

    xi_squared = 0
    interval_ranges = list(intervals.keys())

    for i in range(len(intervals.values())):
        if i == 0:
            p = F(interval_ranges[i]) - F(0)
        else:
            p = F(interval_ranges[i]) - F(interval_ranges[i-1])

        xi_squared += (p_star[i]-p)**2/p

    xi_squared *= len(values)
    xi_squared_limit = 42.6  # For 0.05 error

    print("Corresponds to the distribution (by Pearson):",
          xi_squared < xi_squared_limit)


def kolmogorov(values):
    sorted_values = sorted(values)
    max_gap = 0

    for i in range(len(values)-1):
        f_star = i/len(values)

        f = F(sorted_values[i])
        next_f = F(sorted_values[i+1])

        gap = abs(f_star - f)
        next_gap = abs(f_star-next_f)

        max_gap = max(gap, next_gap, max_gap)

    criteria = math.sqrt(len(values)) * max_gap
    criteria_limit = 1.36  # For 0.05 error

    print("Corresponds to the distribution (by Kolmogorov):",
          criteria < criteria_limit)


def mises(values):
    sorted_values = sorted(values)
    mises_sum = 1/(12 * len(values))

    for i in range(len(values)-1):
        mises_sum += (F(sorted_values[i]) - (i+0.5)/len(values))**2

    mises_limit = 0.461  # For 0.05 error

    print("Corresponds to the distribution (by Mises):",
          mises_sum < mises_limit)


if __name__ == "__main__":
    values = get_random_sequence(200)
    intervals, step = get_distribution_intervals(values, 30)

    pearson(values, intervals, step)

    values = get_random_sequence(30)
    kolmogorov(values)

    values = get_random_sequence(50)
    mises(values)
