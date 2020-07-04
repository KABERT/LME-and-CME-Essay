import pandas as pd
from tools import read_all_target_country, strip_every_element, get_first_titile, get_key_index, get_max_yr, dict_to_write_helper, append_df_to_excel



def write_df_to_excel(df, sheet_name, is_first=False):
    if is_first:
        df.to_excel("data/Washed_DD_T2_Five_Spheres_All_in_One.xlsx", sheet_name=sheet_name, index=False)
    else:
        append_df_to_excel(df, sheet_name)


def select_rows_by_country_name(df, target_countries, df_name, is_first=False):
    r_frame = pd.DataFrame()
    frame_title = get_first_titile(df)
    country_in_sheet = df[frame_title].tolist()

    for country in target_countries:
        if country in country_in_sheet:
            index = country_in_sheet.index(country)
            row = df.loc[index]
            temp = pd.DataFrame(row).T
            r_frame = r_frame.append([temp])
        else:
            print(df_name, "is Missing: ", country)
    write_df_to_excel(r_frame, df_name, is_first)


def reformat_data_by_country_name(df, target_countries, target_code, df_name, key):
    country_copy = target_countries
    all_countries = strip_every_element(df[get_first_titile(df)].tolist())

    # Check if it is country code or conutry name
    if len(all_countries[0]) == 3:
        target_countries = target_code

    # get the index of the key.
    subject_index, yr_index, value_index = get_key_index(df)
    max_yr = get_max_yr(df)
    # Years, subject
    data_collection = {}

    for i in range(len(all_countries)):
        if all_countries[i] in target_countries:
            if df.loc[i][subject_index] == key:
                # Check if the time is in the range.
                if 2000 <= df.loc[i][yr_index] <= max_yr:
                    if all_countries[i] not in data_collection:
                        data_collection[all_countries[i]] = [[df.loc[i][yr_index]], [df.loc[i][value_index]]]
                    else:
                        data_collection[all_countries[i]][0].append(df.loc[i][yr_index])
                        data_collection[all_countries[i]][1].append(df.loc[i][value_index])
    dict_to_write_helper(data_collection, target_countries, country_copy, df_name)


if __name__ == "__main__":
    df = pd.ExcelFile(r"data/DD_T2_Five_Spheres_All_in_One.xlsx")
    df_countries = pd.read_excel(df, "Countries Selected")
    all_country_name, all_county_code, _ = read_all_target_country()

    select_rows_sheets = ['Collective Bargaining Coverage', 'Employment Length < 1yr', 'Employment Protection',
                          'Mergers and Acquisitions', 'Long term Employment', "Size of Stock Market", 'VC investment', 'Avg Tenure']

    for i in range(len(select_rows_sheets)):
        sheet_name = select_rows_sheets[i]
        df_current = pd.read_excel(df, sheet_name)
        if i == 0:
            select_rows_by_country_name(df_current, all_country_name, sheet_name, is_first=True)
        else:
            select_rows_by_country_name(df_current, all_country_name, sheet_name)

    other_sheets = ["Unemployment Protection", 'UpperSecondary Non-Ter Emp Rate', 'Tertiary',
                    'Coordination of Wage Setting', 'Work Council Rights']
    for i in range(len(other_sheets)):
        sheet_name = other_sheets[i]
        df_current = pd.read_excel(df, sheet_name)

        if sheet_name == "UpperSecondary Non-Ter Emp Rate":
            key = "UPPSRY_NTRY"
        if sheet_name == 'Tertiary':
            key = "25_34"
        if sheet_name == "Unemployment Protection":
            key = "TOT"
        if sheet_name == 'Coordination of Wage Setting':
            key = "COORD"
        if sheet_name == 'Work Council Rights':
            key = "WC_rights"

        reformat_data_by_country_name(df_current, all_country_name, all_county_code, sheet_name, key)
