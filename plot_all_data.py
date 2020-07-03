import matplotlib.pylab as plt
import pandas as pd
from tools import repharse_data_and_type
import numpy as np


def plot_all_data(SME=False):
    df = pd.ExcelFile(r"data/Washed_DD_T2_Five_Spheres_All_in_One.xlsx")
    all_sheets_lst = df.sheet_names

    for i in range(len(all_sheets_lst)):
        plt.close()
        X, y = repharse_data_and_type(df, all_sheets_lst[i], SME=SME)
        plot_helper(X, y, all_sheets_lst[i], SME)


def plot_helper(X, y, sheet_name, SME):
    X = np.asarray(X)
    if SME:
        suffix = " With SME and NA"
        color = ["r" if y_point == -1 else "b" if y_point == 1 else "g" for y_point in y]
    else:
        suffix = " Without SME and NA"
        color = ["r" if y_point == -1 else "b" for y_point in y]
    plt.title(sheet_name + suffix)
    plt.scatter(X[:, 0], X[:, 1], color=color, s=20, alpha=0.7)
    plt.savefig("img/"+sheet_name + suffix)


if __name__ == "__main__":
    plot_all_data(SME=False)
    plot_all_data(SME=True)
