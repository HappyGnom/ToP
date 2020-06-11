from RandomGenerator import get_random_sequence
import matplotlib.pyplot as plt
from scipy.special import erfinv
from scipy.special import erf
from scipy.stats import t, norm
import math

# F(x) = sqrt(x)/2
# f(x) = 1/(4sqrt(x))


def laplace_func(x):
    return erf(x/2**0.5)/2


def inverse_laplace_func(y):
    return 2**0.5*erfinv(2*y)


def estimate_math_expectation(values):
    return sum(values)/len(values)


def estimate_dispersion(values, expectation):
    dispersion = 0

    for value in values:
        dispersion += (value-expectation)**2

    return dispersion/len(values)


def estimate_trust_interval_no_dispersion(values, expectation):
    trust_levels = [0.75, 0.8, 0.85, 0.9, 0.95]
    trust_intervals = {}

    for trust_level in trust_levels:
        standard_deviation = math.sqrt(dispersion)

        student_coefficient = t.isf((1-trust_level)/2, len(values)-1)
        half_interval = student_coefficient * \
            standard_deviation/math.sqrt(len(values))

        first_border = expectation - half_interval
        second_border = expectation + half_interval
        trust_intervals[trust_level] = (
            min(first_border, second_border), max(first_border, second_border))

    return trust_intervals


def estimate_trust_interval(values, expectation, dispersion):
    trust_levels = [0.75, 0.8, 0.85, 0.9, 0.95]
    trust_intervals = {}

    for trust_level in trust_levels:
        standard_deviation = math.sqrt(dispersion)

        laplace_arg = norm.isf((1-trust_level)/2)
        half_interval = laplace_arg * standard_deviation/math.sqrt(len(values))

        first_border = expectation - half_interval
        second_border = expectation + half_interval
        trust_intervals[trust_level] = (
            min(first_border, second_border), max(first_border, second_border))

    return trust_intervals


def output_trust_intervals(trust_intervals, with_dispersion):
    if not with_dispersion:
        print("Estimation trust intervals (unknown dispersion):")
    else:
        print("Estimation trust intervals (known dispersion):")

    for level, interval in trust_intervals.items():
        print(" Trust level:", "{:.2f};".format(level),
              "Interval:", interval,
              "- Range:", abs(interval[0]-interval[1]))


def plot_trust_intervals(trust_intervals, with_dispersion):
    interval_lengths = []
    for level, interval in trust_intervals.items():
        interval_lengths.append(abs(interval[0]-interval[1]))

    plt.plot(list(trust_intervals.keys()),
             interval_lengths, '-ok', color="#ff1e56")
    plt.gca().set_facecolor("#000839")

    if not with_dispersion:
        plt.title('Trust intervals (unknown dispersion)')
    else:
        plt.title('Trust intervals (known dispersion)')

    plt.xlabel('Trust level')
    plt.ylabel('Interval length')

    plt.show()


def plot_trust_intervals_by_sizes(intervals_by_sizes):
    colors = {20: "#FF99B3", 30: "#FF7094", 50: "#FF4775",
              70: "#FF1E56", 100: "#F5003D", 150: "#CC0033"}

    for size, intervals in intervals_by_sizes.items():
        interval_lengths = []
        for level, interval in intervals.items():
            interval_lengths.append(abs(interval[0]-interval[1]))

        plt.plot(list(intervals.keys()),
                 interval_lengths, '-ok', color=colors[size],
                 label="Size: " + str(size))

    plt.gca().set_facecolor("#000839")
    plt.legend(loc='upper right')

    plt.title('Trust intervals by sample sizes')
    plt.xlabel('Trust level')
    plt.ylabel('Interval length')

    plt.show()


if __name__ == "__main__":
    sample_sizes = [20, 30, 50, 70, 100, 150]
    intervals_by_sizes = {}

    for sample_size in sample_sizes:
        print("Sample size:", sample_size, end="\n\n")
        values = get_random_sequence(sample_size)

        expectation = estimate_math_expectation(values)
        print("Estimate of mathematical expectation M[x]:", expectation)

        dispersion = estimate_dispersion(values, expectation)
        print("Estimate of dispersion D[x]:", dispersion)

        trust_intervals_no_dispersion = estimate_trust_interval_no_dispersion(
            values, expectation)

        output_trust_intervals(trust_intervals_no_dispersion, False)
        plot_trust_intervals(trust_intervals_no_dispersion, False)

        actual_dispersion = 64/45
        trust_intervals = estimate_trust_interval(
            values, expectation, actual_dispersion)
        intervals_by_sizes[sample_size] = trust_intervals

        output_trust_intervals(trust_intervals, True)
        plot_trust_intervals(trust_intervals, True)

        print("\n\n")

    plot_trust_intervals_by_sizes(intervals_by_sizes)
