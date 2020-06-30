import numpy as np
import pandas as pd
import matplotlib.pylab as plt

from sklearn.svm import SVC

# Part 1
# Doing the SVM model for the capitalization as percent of GDP.
excel = pd.ExcelFile(r"capitalization as a percentage of GDP.xls")

df1 = pd.read_excel(excel, "Data")

headers = df1.columns.ravel()

