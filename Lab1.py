from RandomGenerator import get_random_sequence
from prettytable import PrettyTable
import matplotlib.pyplot as plt
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

if __name__ == "__main__":
    values = get_random_sequence(40)
    intervals, step = get_distribution_intervals(values, 10)

    variation_table = PrettyTable(["Interval end", "Count of values"])
    variation_table.title = "Variation series"
    interval_ends, counts = zip(*intervals.items())
    for interval_end, count in intervals.items():
        variation_table.add_row(["{:.2f}".format(interval_end), count])

    print(variation_table)

    empirical_function_table = PrettyTable(["x", "F(x)"])
    empirical_function_table.title = "Empirical function"
    empirical_function = []
    for index, value in enumerate(sorted(values), start=1):
        empirical_function.append(index/len(values))
        empirical_function_table.add_row([value, index/len(values)])

    print(empirical_function_table)
    
    real_function_table = PrettyTable(["x", "F(x)"])
    real_function_table.title = "Real function"
    real_function = []
    for value in sorted(values):
        real_function.append(F(value))
        real_function_table.add_row([value, F(value)])

    print(real_function_table)
    

    plt.gca().set_facecolor("#000839")

    plt.plot(interval_ends, counts, '-o',
             color="#FF4775", label="Variation series")
    plt.plot(sorted(values), empirical_function, '-o',
             color="#FF7094", label="Empirical function")
    plt.plot(sorted(values), real_function, '--',
             color="#CC0033", label="Real function")
    
    plt.legend(loc='upper right')

    plt.show()
