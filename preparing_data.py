import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import math
from sklearn.svm import SVC
import cvxpy as cp


# -------------------------get all data prepared-----------------------------------
def get_all_countries():
    # Get all countries
    country_excel = pd.read_excel(r"data/countries.xlsx")
    # print(country_excel['Witt and Jackson 2016'].tolist())
    countries = ['Austria', 'Australia', 'Belgium', 'Canada', 'Denmark', 'Finland', 'Germany', 'Ireland', 'Japan', 'Netherlands', 'Norway', 'New Zealand', 'Sweden', 'Switzerland', 'UK', 'USA', 'France', 'Greece', 'Italy', 'Portugal', 'South Korea', 'Spain', 'The Czech Republic', 'Hungary', 'Poland', 'Turkey']

    # LME = 1; CME = 0
    country_type = country_excel["16 TYPE"].tolist()
    temp = []
    for i in range(len(country_type)):
        if country_type[i] == "CME":
            temp.append(1)
        if country_type[i] == "LME":
            temp.append(0)
    country_type[:] = temp

    return countries, country_type


# -------------------------A helper function to get the country code-----------------
def get_country_code():
    countries, code = get_all_countries()
    market = pd.ExcelFile(r"data/capitalization as a percentage of GDP.xls")
    df1 = pd.read_excel(market, "Data")

    all_countries = df1["Country Name"].tolist()
    all_country_code = df1[df1.columns.ravel()[1]].tolist()

    wanted_country_code = []
    wanted_country_type = []
    for i in range(len(all_country_code)):
        if all_countries[i].strip() in countries:
            wanted_country_code.append(all_country_code[i])
            # wanted_country_type.append(code[countries.index(all_countries[i])])
    return wanted_country_code, wanted_country_type


# -------------------A helper function to scatter plot the graph--------------------
def scatter_helper(all_data, all_type):
    plt.scatter(all_data[:, 0], all_data[:, 1], color=["r" if y_point == 1 else "b" for y_point in all_type],
                label="data")
    plt.show()


# -------------------A helper function to do the SVM--------------------------------
def SVM_helper(all_data, all_type, c=1, dis=0.01):
    clf = SVC(kernel="rbf", gamma="auto", C=c)
    clf.fit(all_data, all_type)
    X = all_data
    x1s = np.linspace(min(X[:, 0]), max(X[:, 0]), 600)
    x2s = np.linspace(min(X[:, 1]), max(X[:, 1]), 600)
    points = np.array([[x1, x2] for x1 in x1s for x2 in x2s])
    dist_bias = clf.decision_function(points)
    bounds_bias = np.array([pt for pt, dist in zip(points, dist_bias) if abs(dist) < dis])
    plt.scatter(bounds_bias[:, 0], bounds_bias[:, 1], color="g", s=0.5, label="decision boundary")
    scatter_helper(all_data, all_type)
    plt.show()


# -------------------A helper function to do the Linear SVM-----------------------------
def liner_SVM_helper(X, y, C=0.25):
    D = X.shape[1]
    N = X.shape[0]
    W = cp.Variable(D)
    b = cp.Variable()

    # We use C = 1/4 here.
    C = C
    loss = (0.5 * cp.sum_squares(W) + C * cp.sum(cp.pos(1 - cp.multiply(y, X * W + b))))
    # Note that we change the loss function and remove the constraints here.
    prob = cp.Problem(cp.Minimize(loss))
    prob.solve()

    # Get the value of w and b.
    w = W.value
    b = b.value
    print(w, b)

    # Plot the decision boundary.
    x = np.linspace(min(X[:, 0]), max(X[:, 0]), 1200)
    plt.plot(x, (-b - ((w[0]) * x)) / w[1], 'r', label="decision boundary for Soft Margain SVM")
    scatter_helper(X, y)
    plt.legend()
    plt.show()


def clean_nan(all_data, all_type):
    temp_data = []
    temp_type = []
    # Now loop over the all data again, and clean the point with nan.
    for i in range(len(all_data)):
        smth = all_data[i]
        if not math.isnan(smth[1]):
            temp_data.append(all_data[i])
            temp_type.append(all_type[i])
    temp_data = np.asarray(temp_data)
    return temp_data, temp_type


def get_2001_and_GDP_data():
    countries, country_type = get_all_countries()
    # ————————————————————————preparing data 1------------------------------------------
    market = pd.ExcelFile(r"capitalization as a percentage of GDP.xls")
    df1 = pd.read_excel(market, "Data")

    all_countries = df1["Country Name"].tolist()

    years = df1.columns.ravel().tolist()[-19:-1]
    # change all years into int type
    for i in range(len(years)):
        years[i] = int(years[i])

    GDP_data = []
    for i in range(len(all_countries)):
        if all_countries[i].strip() in countries:
            data = df1.iloc[i][-19:-1].tolist()
            for j in range(len(years)):
                data[j] = [years[j], 10 * data[j]]
            GDP_data.append(data)

    data_2001 = []
    for i in range(len(countries)):
        data_2001.append(GDP_data[i][0])

    all_data = []
    all_type = []
    for j in range(len(GDP_data[0])):
        for i in range(len(countries)):
            all_data.append(GDP_data[i][j])
        all_type += country_type

    all_data, all_type = clean_nan(all_data, all_type)

    # Now do SVM and draw the decision boundary on the plot.

    # ------------------------------------------------------------------------
    clf = SVC(kernel="rbf", gamma="auto", C=10)
    clf.fit(all_data, all_type)
    X = all_data
    x1s = np.linspace(min(X[:, 0]), max(X[:, 0]), 1200)
    x2s = np.linspace(min(X[:, 1]), max(X[:, 1]), 1200)
    points = np.array([[x1, x2] for x1 in x1s for x2 in x2s])
    dist_bias = clf.decision_function(points)
    bounds_bias = np.array([pt for pt, dist in zip(points, dist_bias) if abs(dist) < 0.08])
    # plt.scatter(bounds_bias[:, 0], bounds_bias[:, 1], color="g", s=0.5, label="decision boundary")

    plt.scatter(all_data[:, 0], all_data[:, 1], color=["r" if y_point == 1 else "b" for y_point in all_type],
                label="data")
    plt.show()


# get_2001_and_GDP_data()


def test_data():
    countries, country_type = get_all_countries()
    # ————————————————————————preparing data 1------------------------------------------
    df1 = pd.read_excel(r"test.xlsx")

    all_countries = df1["Country Name"].tolist()

    years = df1.columns.ravel().tolist()[-15:-1]
    for i in range(len(years)):
        years[i] = int(years[i])

    GDP_data = []
    for i in range(len(all_countries)):
        if all_countries[i].strip() in countries:
            data = df1.iloc[i][-15:-1].tolist()
            for j in range(len(years)):
                data[j] = [years[j], data[j]]
            GDP_data.append(data)

    print(GDP_data)

    all_data = []
    all_type = []
    for j in range(len(GDP_data[0])):
        for i in range(len(GDP_data)):
            all_data.append(GDP_data[i][j])
        all_type += country_type

    all_data, all_type = clean_nan(all_data, all_type)

    plt.scatter(all_data[:, 0], all_data[:, 1], color=["r" if y_point == 1 else "b" for y_point in all_type],
                label="data")

    # ----------------------------------------------------------------------------------
    clf = SVC(kernel="rbf", gamma="auto", C=1e2)
    clf.fit(all_data, all_type)
    X = all_data
    x1s = np.linspace(min(X[:, 0]), max(X[:, 0]), 1200)
    x2s = np.linspace(min(X[:, 1]), max(X[:, 1]), 1200)
    points = np.array([[x1, x2] for x1 in x1s for x2 in x2s])
    dist_bias = clf.decision_function(points)
    bounds_bias = np.array([pt for pt, dist in zip(points, dist_bias) if abs(dist) < 0.01])
    plt.scatter(bounds_bias[:, 0], bounds_bias[:, 1], color="g", s=0.5, label="decision boundary")

    plt.scatter(all_data[:, 0], all_data[:, 1], color=["r" if y_point == 1 else "b" for y_point in all_type],
                label="data")
    plt.show()
