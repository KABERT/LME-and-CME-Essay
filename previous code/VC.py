from preparing_data import get_country_code, scatter_helper, SVM_helper, liner_SVM_helper
import pandas as pd
import numpy as np

def get_VC():
    country_code, country_type = get_country_code()
    all_data, all_type = [], []
    # -----------------------------Read CSV HERE-------------------------------
    df1 = pd.read_csv("data/VC.csv")
    country_header = df1.columns.ravel()[0]
    VC_country_list = df1[country_header].tolist()

    for i in range(len(VC_country_list)):
        # Check if the country is wanted
        if VC_country_list[i] in country_code:
            # Check if the data is Total VC
            if df1.iloc[i][5] == "Total" and df1.iloc[i][-3] < 2000:
                if not(df1.iloc[i][-3] > 750 and country_type[country_code.index(VC_country_list[i])] == 1) and \
                        not(df1.iloc[i][-3] < 500 and country_type[country_code.index(VC_country_list[i])] != 1):
                    all_data.append([int(df1.iloc[i][8]), df1.iloc[i][-3]])
                    all_type.append(country_type[country_code.index(VC_country_list[i])])
    all_data = np.asarray(all_data)

    SVM_helper(all_data, all_type)

if __name__ == "__main__":
    get_VC()
