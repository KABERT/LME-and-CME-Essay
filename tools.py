import pandas as pd


def read_all_target_country():
    df = pd.ExcelFile(r"data/DD_T2_Five_Spheres_All_in_One.xlsx")
    df_countries = pd.read_excel(df, "Countries Selected")

    target_country_list = get_all_countries_name(df_countries)

    df_country_code = pd.read_excel(df, "Size of Stock Market")

    target_country_code = get_all_country_code(df_country_code, target_country_list)

    target_country_type_list = get_target_type(df_countries)

    return target_country_list, target_country_code, target_country_type_list


def get_target_type(df):
    # extract the country type first
    country_type = df[df.columns.ravel().tolist()[1]].tolist()
    country_type = strip_every_element(country_type)
    r_lst = []
    for type in country_type:
        if type == "LME":
            r_lst.append(1)
        elif type == "CME":
            r_lst.append(-1)
        else:
            r_lst.append(0)
    return r_lst


def get_all_countries_name(df):
    country_list = df[get_first_titile(df)].tolist()
    # strip all the country
    for i in range(len(country_list)):
        country_list[i] = country_list[i].strip()
    return country_list


def get_first_titile(df):
    return df.columns.ravel().tolist()[0]


def strip_every_element(lst):
    lst = [x for x in lst if str(x) != 'nan']
    for i in range(len(lst)):
        lst[i] = lst[i].strip()
    return lst


def get_all_country_code(df, country_name):
    all_country_name = df[get_first_titile(df)].tolist()
    all_country_name = strip_every_element(all_country_name)
    all_country_code = df[df.columns.ravel().tolist()[1]].tolist()
    target_country_code = []

    for country in country_name:
        # Make sure it is in the dataframe
        if country in all_country_name:
            index = all_country_name.index(country)
            target_country_code.append(all_country_code[index])

    return strip_every_element(target_country_code)


def get_key_index(df):
    title = df.columns.ravel().tolist()
    subject_index, yr_index, value_index = 0, 0, 0

    for i in range(len(title)):
        if title[i] == "SUBJECT":
            subject_index = i
        elif title[i] == "TIME":
            yr_index = i
        elif title[i] == "VALUE":
            value_index = i
    return subject_index, yr_index, value_index


def get_max_yr(df):
    return max(df["TIME"].tolist())
