import csv
from collections import defaultdict

import config


def read_data(file_path):
    file_path = file_path[0].replace("_", "")  # TODO: Bug fix
    file_path = config.WAVE_SDK_ROOT_PATH + '/data' + file_path

    dict_from_csv = defaultdict(list)

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            for key, value in line.items():
                dict_from_csv[key].append(value)

    return dict_from_csv


def generate_plot_data(data, x_axis, y_axis_array):
    plot_data = []
    for i, x in enumerate(data[x_axis]):
        for group in y_axis_array:
            plot_data.append([group, x, data[group][i]])
    return plot_data
