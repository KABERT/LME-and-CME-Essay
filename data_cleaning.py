import pandas as pd
from openpyxl import load_workbook
from preparing_data import get_country_code
import csv


def get_all_countries_name(df_countries):
    country_list = df_countries["Selected Countries"].tolist()
    # strip all the country
    for i in range(len(country_list)):
        country_list[i] = country_list[i].strip()
    return country_list


def write_df_to_excel(df, sheet_name):
    df.to_excel("data/Washed_DD_T2_Five_Spheres_All_in_One.xlsx", sheet_name=sheet_name, index=False)


def append_df_to_excel(df, sheet_name):
    path = "data/Washed_DD_T2_Five_Spheres_All_in_One.xlsx"
    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine='openpyxl')
    writer.book = book

    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
    writer.close()


def clean_collective_bargain(df_col_bar, country_lst):
    r_frame = pd.DataFrame()
    for i in range(len(df_col_bar)):
        row = df_col_bar.loc[i]
        if row["Year"] in country_lst:
            temp = pd.DataFrame(row).T
            r_frame = r_frame.append([temp])
    write_df_to_excel(r_frame, "Collective Bargain Coverage")


def clean_short_employment(df_col_bar, country_lst):
    r_frame = pd.DataFrame()
    for i in range(len(df_col_bar)):
        row = df_col_bar.loc[i]
        if row["Time"] in country_lst:
            temp = pd.DataFrame(row).T
            r_frame = r_frame.append([temp])
    append_df_to_excel(r_frame, "Employment Length < 1yr")


def clean_emp_protection(df_col_bar, country_lst):
    r_frame = pd.DataFrame()
    for i in range(len(df_col_bar)):
        row = df_col_bar.loc[i]
        if row["Time"] in country_lst:
            temp = pd.DataFrame(row).T
            r_frame = r_frame.append([temp])
    append_df_to_excel(r_frame, "Employment Protection")


def clean_MA(df_col_bar, country_lst):
    r_frame = pd.DataFrame()
    for i in range(len(df_col_bar)):
        row = df_col_bar.loc[i]
        if row["Country Name"] in country_lst:
            temp = pd.DataFrame(row).T
            r_frame = r_frame.append([temp])
    append_df_to_excel(r_frame, "Mergers and Acquisitions")


def clean_long_term(df_col_bar, country_lst):
    r_frame = pd.DataFrame()
    for i in range(len(df_col_bar)):
        row = df_col_bar.loc[i]
        if row["Time"] in country_lst:
            temp = pd.DataFrame(row).T
            r_frame = r_frame.append([temp])
    append_df_to_excel(r_frame, "Long term Employment")



def clean_tertiary_EDU():
    country_code, country_type = get_country_code()
    all_data, all_year = [], []
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
                    all_data.append(df1.iloc[i][6])
                    all_year.append(int(df1.iloc[i][5]))

    lst_yr, temp_yr, lst_data, temp_data = [], [], [], []
    for i in range(len(all_data)):
        if 2000 <= all_year[i] < 2018:
            temp_data.append(all_data[i])
            temp_yr.append(all_year[i])
        else:
            temp_data.append(all_data[i])
            temp_yr.append(all_year[i])
            lst_yr.append(temp_yr)
            lst_data.append(temp_data)
            temp_data = []
            temp_yr = []

    data_collection = []
    for i in range(len(lst_yr)):
        dict_subject = {"Country Name": country_code[i]}
        for j in range(len(lst_yr[i])):
            dict_subject[lst_yr[i][j]] = lst_data[i][j]
        data_collection.append(dict_subject)

    f = open("data/Cleaned tertiary.csv", "w")
    writer = csv.DictWriter(f, fieldnames=["Country Name", 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,
                                           2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
                            )
    writer.writeheader()
    for data in data_collection:
        writer.writerow(data)
    f.close()



if __name__ == "__main__":
    df = pd.ExcelFile(r"data/DD_T2_Five_Spheres_All_in_One.xlsx")
    df_countries = pd.read_excel(df, "Countries Selected")
    all_countries = get_all_countries_name(df_countries)
    print(all_countries)
    #
    # df_col_bar = pd.read_excel(df, "Collective Bargaining Coverage")
    # clean_collective_bargain(df_col_bar, all_countries)
    #
    # df_short_emp = pd.read_excel(df, "Employment Length < 1yr")
    # clean_short_employment(df_short_emp, all_countries)
    #
    # df_emp_protection = pd.read_excel(df, "Employment Protection")
    # clean_emp_protection(df_emp_protection, all_countries)
    #
    # df_MA = pd.read_excel(df, "Mergers and Acquisitions")
    # clean_MA(df_MA, all_countries)
    #
    # df_long_term = pd.read_excel(df, "Long term Employment")
    # clean_long_term(df_long_term, all_countries)


    clean_tertiary_EDU()

