from preparing_data import get_country_code, scatter_helper, SVM_helper
import pandas as pd
import numpy as np


def get_EDUTRY():
    country_code, country_type = get_country_code()
    all_data, all_type = [], []
    # -----------------------------Read CSV HERE-------------------------------
    df1 = pd.read_csv("data/EDUTRY.csv")
    country_header = df1.columns.ravel()[0]

    edutry_country_list = df1[country_header].tolist()

    for i in range(len(edutry_country_list)):
        # Check if the country is wanted
        if edutry_country_list[i] in country_code:
            # Check if the age range is wanted
            if df1.iloc[i][2] == "25_34":
                # Check if the years is wanted:
                if int(df1.iloc[i][5]) >= 2000:
                    all_data.append([int(df1.iloc[i][5]), df1.iloc[i][6]])
                    all_type.append(country_type[country_code.index(edutry_country_list[i])])
    all_data = np.asarray(all_data)

    # scatter_helper(all_data, all_type)
    SVM_helper(all_data, all_type, C=1)


if __name__ == "__main__":
    get_EDUTRY()
