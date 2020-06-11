from RandomGenerator import get_random_sequence
import matplotlib.pyplot as plt
from scipy.special import erfinv
from scipy.special import erf
from scipy.stats import t
from scipy.stats import chi2
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


def estimate_trust_interval_no_expectation(values, dispersion):
    trust_levels = [0.75, 0.8, 0.85, 0.9, 0.95]
    trust_intervals = {}

    for trust_level in trust_levels:
        S = dispersion*len(values)/(len(values)-1)
        numerator = (len(values)-1) * S

        first_border = numerator / chi2.ppf((1 - trust_level)/2, len(values)-1)
        second_border = numerator / chi2.ppf(trust_level/2, len(values)-1)
        trust_intervals[trust_level] = (
            min(first_border, second_border), max(first_border, second_border))

    return trust_intervals


def estimate_trust_interval(values, expectation):
    trust_levels = [0.75, 0.8, 0.85, 0.9, 0.95]
    trust_intervals = {}

    real_dispersion = 0
    for value in values:
        real_dispersion += (value - expectation)**2

    for trust_level in trust_levels:
        first_border = real_dispersion / chi2.ppf((1-trust_level)/2, len(values))
        second_border = real_dispersion / chi2.ppf(trust_level/2, len(values))

        trust_intervals[trust_level] = (
            min(first_border, second_border), max(first_border, second_border))

    return trust_intervals


def output_trust_intervals(trust_intervals, with_expectation):
    if not with_expectation:
        print("Estimation trust intervals (unknown expectation):")
    else:
        print("Estimation trust intervals (known expectation):")

    for level, interval in trust_intervals.items():
        print(" Trust level:", "{:.2f};".format(level),
              "Interval:", interval,
              "- Range:", abs(interval[0]-interval[1]))


def plot_trust_intervals(trust_intervals, with_expectation):
    interval_lengths = []
    for level, interval in trust_intervals.items():
        interval_lengths.append(abs(interval[0]-interval[1]))

    plt.plot(list(trust_intervals.keys()),
             interval_lengths, '-ok', color="#ff1e56")
    plt.gca().set_facecolor("#000839")

    if not with_expectation:
        plt.title('Trust intervals (unknown expectation)')
    else:
        plt.title('Trust intervals (known expectation)')

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
        dispersion = estimate_dispersion(values, expectation)

        print("Estimate of dispersion D[x]:", dispersion)
        print("Estimate of mathematical expectation M[x]:", expectation)

        trust_intervals_no_expectation = estimate_trust_interval_no_expectation(
            values, dispersion)

        output_trust_intervals(trust_intervals_no_expectation, False)
        plot_trust_intervals(trust_intervals_no_expectation, False)

        actual_expectation = 4/3
        trust_intervals = estimate_trust_interval(
            values, actual_expectation)
        intervals_by_sizes[sample_size] = trust_intervals

        output_trust_intervals(trust_intervals, True)
        plot_trust_intervals(trust_intervals, True)

        print("\n\n")

    plot_trust_intervals_by_sizes(intervals_by_sizes)
