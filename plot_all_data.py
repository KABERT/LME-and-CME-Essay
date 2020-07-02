import matplotlib.pylab as plt
import pandas as pd
from tools import read_all_target_country
import numpy as np
import time


def plot_all_data():
    df = pd.ExcelFile(r"data/Washed_DD_T2_Five_Spheres_All_in_One.xlsx")
    all_sheets_lst = df.sheet_names

    for i in range(len(all_sheets_lst)):
        plt.close()
        plot_helper(df, all_sheets_lst[i])


def plot_helper(df, sheet_name):
    # Data collection: X and y
    X, y = [], []
    # Read the data using tools.
    all_country_lst, code_lst, type_lst = read_all_target_country()
    df_curr_sheet = pd.read_excel(df, sheet_name)
    titles = df_curr_sheet.columns.ravel().tolist()

    country_lst = df_curr_sheet[titles[0]].tolist()
    print(sheet_name)
    for i in range(len(country_lst)):
        # get the corresponding type of the country
        curr_country_type = type_lst[all_country_lst.index(country_lst[i])]
        for j in range(1, len(titles)):
            point = [int(titles[j]), df_curr_sheet.loc[i].tolist()[j]]
            if point[1] == ".." or point[1] == "":
                point[1] = float("nan")
            else:
                point = [int(titles[j]), float(df_curr_sheet.loc[i].tolist()[j])]
            # Check if this point is valid.
            # if curr_country_type != 0:
            X.append(point)
            y.append(curr_country_type)

    X = np.asarray(X)
    plt.title(sheet_name + " Without SME and NA")
    plt.scatter(X[:, 0], X[:, 1], color=["r" if y_point == -1 else "b" if y_point == 1 else "g" for y_point in y], s=20, alpha=0.5)
    plt.savefig("img/"+sheet_name + " Without SME and NA")


if __name__ == "__main__":
    plot_all_data()
