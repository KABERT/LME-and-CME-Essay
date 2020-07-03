from tools import construct_dict_by_country_name, repharse_data_and_type, read_all_target_country, \
    joint_dictionary_together, invert_dict_to_lst
import pandas as pd
from plot_all_data import plot_helper
import numpy as np
import matplotlib.pylab as plt


def plot_all_sphere(SME=False):
    df = pd.ExcelFile(r"data/Washed_DD_T2_Five_Spheres_All_in_One.xlsx")
    spheres = ['Collective Bargaining Coverage', 'Coordination of Wage Setting', 'Employment Length < 1yr',
               'Employment Protection', 'Unemployment Protection'], ['Tertiary EMP Rate',
                                                                     'UpperSecondary Non-Ter Emp Rate', 'Tertiary'],\
              ['Size of Stock Market', 'VC investment'], ['Mergers and Acquisitions'], ['Work Council Rights',
                                                                                        'Long term Employment']
    for i in range(len(spheres)):
        sphere = spheres[i]
        sphere_info = {}
        for i in range(len(sphere)):
            sheet = sphere[i]
            print(sheet)
            X, _ = repharse_data_and_type(df, sheet)
            ratio = get_ratio(X)
            dict = construct_dict_by_country_name(df, sheet)
            temp = update_indicator(dict, ratio)
            sphere_info = joint_dictionary_together(sphere_info, temp)
        X, y = invert_dict_to_lst(sphere_info, SME)

        plt.clf()
        plot_helper(np.asarray(X), y, "sphere" + str(i), SME=SME)


def get_ratio(X):
    temp = []
    for i in range(len(X)):
        if type(X[i][1]) != int and type(X[i][1]) != float or str(X[i][1]) == "nan":
            X[i][1] = -1
        temp.append(X[i][1])
    max_val = max(temp)
    lst = []
    if max_val > 4500:
        lst = []
        for i in range(len(temp)):
            if temp[i] <= 4500:
                lst.append(temp[i])
        max_val = max(lst)
    ratio = max_val / 10
    return ratio


def update_indicator(dict, ratio):
    for key in dict:
        for i in range(len(dict[key])):
            if type(dict[key][i][1]) != int and type(dict[key][i][1]) != float or str(dict[key][i][1]) == "nan":
                dict[key][i][1] = 5
            else:
                indicator = dict[key][i][1] / ratio
                if indicator >= 10:
                    dict[key][i][1] = 10
    return dict


if __name__ == "__main__":
    plot_all_sphere()
    plot_all_sphere(SME=True)
