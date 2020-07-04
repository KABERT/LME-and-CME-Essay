from tools import construct_dict_by_country_name, repharse_data_and_type, read_all_target_country, \
    joint_dictionary_together, invert_dict_to_lst, reformate_dict_to_output, dict_to_write_helper
import pandas as pd
from plot_all_data import plot_helper
import numpy as np
import matplotlib.pylab as plt


def plot_all_sphere(SME=False):
    df = pd.ExcelFile(r"data/Washed_DD_T2_Five_Spheres_All_in_One.xlsx")
    spheres = ['Collective Bargaining Coverage', 'Coordination of Wage Setting', 'Employment Length < 1yr',
               'Employment Protection', 'Unemployment Protection'], [
                                                                     'UpperSecondary Non-Ter Emp Rate', 'Tertiary'],\
              ['Size of Stock Market', 'VC investment'], ['Mergers and Acquisitions'], ['Work Council Rights',
                                                                                        'Long term Employment', 'Avg Tenure']
    for i in range(len(spheres)):
        i = 4
        sphere = spheres[i]
        sphere_info = {}
        for j in range(len(sphere)):
            sheet = sphere[j]
            print(sheet)
            X, _ = repharse_data_and_type(df, sheet)
            ratio = get_ratio(X)
            dict = construct_dict_by_country_name(df, sheet)
            if sheet not in ["Employment Length < 1yr", "Tertiary", "Size of Stock Market", "VC investment", "Mergers and Acquisitions"]:
                CME = False
            else:
                CME = True



            temp = update_indicator(dict, ratio, CME)
            print(temp)
            temp = interpolation(temp)

            sphere_info = joint_dictionary_together(sphere_info, temp)
        sphere_info = reformate_dict_to_output(sphere_info)
        country,_,_ = read_all_target_country()
        dict_to_write_helper(sphere_info, country, country, "Sphere ")
        # X, y = invert_dict_to_lst(sphere_info, SME)
        #
        # plt.clf()
        # plot_helper(np.asarray(X), y, "Sphere " + str(i), SME=SME)
        break


def interpolation(dict):
    for keys in dict:
        data = dict[keys]
        yr = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
        data_yr = []
        for i in range(len(data)):
            data_yr.append(data[i][0])
        for year in yr:
            if year not in data_yr:
                dict[keys].append([year, 5])
    return dict


def get_ratio(X):
    temp = []
    for i in range(len(X)):
        if (type(X[i][1]) != int and type(X[i][1]) != float) or str(X[i][1]) == "nan":
            X[i][1] = -1
        temp.append(float(X[i][1]))
    max_val = max(temp)
    if max_val > 4500:
        lst = []
        for i in range(len(temp)):
            if temp[i] <= 4500:
                lst.append(temp[i])
        max_val = max(lst)
    ratio = max_val / 10
    return ratio


def update_indicator(dict, ratio, CME):
    for key in dict:
        for i in range(len(dict[key])):
            if (type(dict[key][i][1]) != int and type(dict[key][i][1]) != float) or str(dict[key][i][1]) == "nan":
                dict[key][i][1] = 5
            else:
                indicator = dict[key][i][1] / ratio
                if indicator > 10:
                    print(key)
                    if CME:
                        dict[key][i][1] = 10
                    else:
                        dict[key][i][1] = 0
                else:
                    if CME:
                        dict[key][i][1] = dict[key][i][1] / ratio
                    else:
                        dict[key][i][1] = 10 - (dict[key][i][1] / ratio)
    return dict


if __name__ == "__main__":
    plot_all_sphere()
    # plot_all_sphere(SME=True)
