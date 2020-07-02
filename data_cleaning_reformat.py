import pandas as pd
from openpyxl import load_workbook
from tools import read_all_target_country, strip_every_element
import csv


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
    country_in_sheet = strip_every_element(df[frame_title].tolist())

    for country in target_countries:
        if country in country_in_sheet:
            index = country_in_sheet.index(country)
            row = df.loc[index]
            temp = pd.DataFrame(row).T
            r_frame = r_frame.append([temp])
        else:
            print(df_name, "is Missing: ", country)
    write_df_to_excel(r_frame, df_name, is_first)



if __name__ == "__main__":
    df = pd.ExcelFile(r"data/DD_T2_Five_Spheres_All_in_One.xlsx")
    df_countries = pd.read_excel(df, "Countries Selected")
    all_country_name, all_county_code, _ = read_all_target_country()

    all_sheets = ['Collective Bargaining Coverage', 'Employment Length < 1yr', 'Employment Protection', 'Tertiary EMP Rate', 'UpperSecondary Non-Ter Emp Rate', 'Tertiary', 'VC investment', 'Mergers and Acquisitions', 'Coordination of Wage Setting', 'Work Council Rights', 'Long term Employment', 'Countries Selected']

    select_rows_sheets = ['Collective Bargaining Coverage', 'Employment Length < 1yr', 'Employment Protection', 'Mergers and Acquisitions', 'Long term Employment', 'VC investment']

    for i in range(len(select_rows_sheets)):
        sheet_name = select_rows_sheets[i]
        df_current = pd.read_excel(df, sheet_name)
        if i == 0:
            select_rows_by_country_name(df_current, all_country_name, sheet_name, is_first=True)
        else:
            select_rows_by_country_name(df_current, all_country_name, sheet_name)
