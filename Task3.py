from RandomGenerator import get_random_sequence
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np


def draw_histogram(values):
    values.sort()
    table = PrettyTable()
    table.field_names = ["Start", "End", "Height"]

    columns = int(np.sqrt(len(values)))
    values_per_column = int(len(values)/columns)

    A = [values[0]]
    B = [(values[values_per_column-1]+values[values_per_column])/2]

    for i in range(1, columns):
        A.append(B[i-1])

        if (i+1)*(values_per_column) >= len(values):
            B.append(values[len(values)-1])
        else:
            B.append((values[(i+1)*(values_per_column-1)] +
                      values[(i+1)*(values_per_column)])/2)

    for i in range(columns):
        width = B[i] - A[i]
        height = values_per_column/(len(values)*width)

        table.add_row([A[i], B[i], height])
        plt.bar(x=A[i], height=height, width=width, align='edge')

    plt.title('Distribution Histogram')
    plt.xlabel('Value')
    plt.ylabel('Possibility')

    plt.ylim(0, 3)
    plt.grid(axis='y', alpha=0.8)

    print(table.get_string(title="Distribution Histogram Table"))
    plt.show()


def draw_polygon(values):
    values.sort()
    # columns = int(np.sqrt(len(values)))
    columns = 8
    column_range = 4/columns

    table = PrettyTable()
    table.field_names = ["From", "To", "Count"]

    points = {}

    for i in range(columns):
        start = i*column_range
        end = (i+1) * column_range
        range_middle = end - column_range/2

        count = sum(start < x <= end for x in values)

        table.add_row([start, end, count])
        points[range_middle] = count

    lists = sorted(points.items())
    x, y = zip(*lists)

    plt.title('Distribution Polygon')
    plt.xlabel('Value-range')
    plt.ylabel('Count')
    plt.grid(axis='y', alpha=0.8)

    plt.plot(x, y, '-o')

    print(table.get_string(title="Distribution Poly Table"))
    plt.show()


def draw_distribution_function(values):
    values.sort()
    F = []

    table = PrettyTable()
    table.field_names = ["x", "F*(x)"]

    for i in range(len(values)):
        function = i/len(values)
        F.append(function)
        table.add_row([i, function])

    plt.title('Distribution Function for '+str(len(values)) + ' values')
    plt.xlabel('Value')
    plt.ylabel('F*(x)')
    plt.grid(axis='y', alpha=0.8)

    plt.plot(values, F)
    print(table.get_string(title="Distr. F* Table"))
    plt.show()


draw_histogram(get_random_sequence(100))
draw_polygon(get_random_sequence(1000))
draw_distribution_function(get_random_sequence(500))
