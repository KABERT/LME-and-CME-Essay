from tools import construct_dict_by_country_name, repharse_data_and_type, read_all_target_country
import pandas as pd
from plot_all_data import plot_helper
import numpy as np


def plot_all_sphere(SME=False):
    df = pd.ExcelFile(r"data/Washed_DD_T2_Five_Spheres_All_in_One.xlsx")
    all_sheets_lst = df.sheet_names

    spheres = ['Collective Bargaining Coverage', 'Coordination of Wage Setting', 'Employment Length < 1yr',
               'Employment Protection', 'Unemployment Protection'], ['Tertiary EMP Rate',
                                                                     'UpperSecondary Non-Ter Emp Rate', 'Tertiary'],\
              ['Size of Stock Market', 'VC investment'], ['Mergers and Acquisitions'], ['Work Council Rights',
                                                                                        'Long term Employment']
    for sphere in spheres:
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
        print(y)
        plot_helper(np.asarray(X), y, "sphere1", SME=SME)

        break


def invert_dict_to_lst(dict, SME):
    X, y = [], []
    all_target_country, _, code = read_all_target_country()
    for country in all_target_country:
        data = dict[country]
        country_type = code[all_target_country.index(country)]
        if not SME:
            if country_type != 0:
                X += data
                y += [country_type] * len(data)
        else:
            X += data
            y += [country_type] * len(data)
    return X, y



def joint_dictionary_together(first, second):
    if first == {}:
        first = second
    else:
        for k, v in second.items():
            # Check if the first dictionary has this country
            if k not in first:
                first[k] = second[k]
            for items in v:
                yr = items[0]
                flag = False
                for first_item in first[k]:
                    if first_item[0] == yr:
                        first_item[1] += items[1]
                        flag = True
                if not flag:
                    first[k].append(items)
    return first


def combine_list_info(target_lst, new_lst):
    if len(target_lst) == 0:
        target_lst = new_lst
    else:
        for i in range(len(target_lst)):
            target_lst[i][1] += new_lst[i][1]
    return target_lst


def get_ratio(X):
    temp = []
    for i in range(len(X)):
        if type(X[i][1]) != int and type(X[i][1]) != float or str(X[i][1]) == "nan":
            X[i][1] = -1
        temp.append(X[i][1])
    max_val = max(temp)
    print(max_val)
    ratio = max_val / 10
    return ratio


def update_indicator(dict, ratio):
    for key in dict:
        for i in range(len(dict[key])):
            if type(dict[key][i][1]) != int and type(dict[key][i][1]) != float or str(dict[key][i][1]) == "nan":
                dict[key][i][1] = 5
            else:
                dict[key][i][1] = dict[key][i][1] / ratio
    return dict

if __name__ == "__main__":
    plot_all_sphere()
