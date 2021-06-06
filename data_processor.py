import pandas as pd

import config


def read_data(file_path):
    file_path = file_path[0].replace("_", "", 1)  # TODO: Bug fix
    file_path = config.WAVE_SDK_ROOT_PATH + '/data' + file_path

    with open(file_path, 'r') as csv_file:
        dict_from_csv = pd.read_csv(csv_file).to_dict()

    return dict_from_csv


def generate_plot_data(data, x_axis, y_axis_array):
    x_dictionary = data[x_axis]
    plot_data = []
    for i, x in x_dictionary.items():
        for group in y_axis_array:
            y_dictionary = data[group]
            point = (group, x, y_dictionary[i])
            plot_data.append(point)
    return plot_data
