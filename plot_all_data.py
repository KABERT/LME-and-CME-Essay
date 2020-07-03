import matplotlib.pylab as plt
import pandas as pd
from tools import read_all_target_country, repharse_data_to_plot
import numpy as np


def plot_all_data(SME=False):
    df = pd.ExcelFile(r"data/Washed_DD_T2_Five_Spheres_All_in_One.xlsx")
    all_sheets_lst = df.sheet_names

    for i in range(len(all_sheets_lst)):
        plt.close()
        plot_helper(df, all_sheets_lst[i], SME)


def plot_helper(df, sheet_name, SME):
    X, y = repharse_data_to_plot(df, sheet_name, SME=SME)
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
