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


def write_df_to_excel(df, sheet_name, is_first=False):
    if is_first:
        df.to_excel("data/Washed_DD_T2_Five_Spheres_All_in_One.xlsx", sheet_name=sheet_name, index=False)
    else:
        append_df_to_excel(df, sheet_name)


def append_df_to_excel(df, sheet_name):
    path = "data/Washed_DD_T2_Five_Spheres_All_in_One.xlsx"
    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine='openpyxl')
    writer.book = book

    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
    writer.close()


def select_rows_by_country_name(df, target_countries, df_name, is_first=False):
    r_frame = pd.DataFrame()
    frame_title = df.columns.ravel().tolist()[0]
    for i in range(len(df)):
        row = df.loc[i]
        if row[frame_title] in target_countries:
            temp = pd.DataFrame(row).T
            r_frame = r_frame.append([temp])
    write_df_to_excel(r_frame, df_name, is_first)


if __name__ == "__main__":
    df = pd.ExcelFile(r"data/DD_T2_Five_Spheres_All_in_One.xlsx")
    df_countries = pd.read_excel(df, "Countries Selected")
    all_countries = get_all_countries_name(df_countries)

    all_sheets = df.sheet_names
    select_rows_sheets = ['Collective Bargaining Coverage', 'Employment Length < 1yr', 'Employment Protection', 'Tertiary EMP Rate', 'UpperSecondary Non-Ter Emp Rate', 'Tertiary', 'VC investment', 'Mergers and Acquisitions', 'Coordination of Wage Setting', 'Work Council Rights', 'Long term Employment', 'Countries Selected']
