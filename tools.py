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


def repharse_data_and_type(df, sheet_name, SME=False):
    # Data collection: X and y
    X, y = [], []
    # Read the data using tools.
    all_country_lst, code_lst, type_lst = read_all_target_country()
    df_curr_sheet = pd.read_excel(df, sheet_name)
    titles = df_curr_sheet.columns.ravel().tolist()

    country_lst = df_curr_sheet[titles[0]].tolist()
    for i in range(len(country_lst)):
        # get the corresponding type of the country
        curr_country_type = type_lst[all_country_lst.index(country_lst[i])]
        for j in range(1, len(titles)):
            point = [int(titles[j]), df_curr_sheet.loc[i].tolist()[j]]
            if point[1] == ".." or point[1] == "":
                point[1] = float("nan")
            else:
                point = [int(titles[j]), float(df_curr_sheet.loc[i].tolist()[j])]
            # Check if this point is valid.
            if not SME:
                if int(curr_country_type) != 0:
                    X.append(point)
                    y.append(curr_country_type)
            else:
                X.append(point)
                y.append(curr_country_type)
    return X, y


def construct_dict_by_country_name(df, sheet_name):
    df_curr = pd.read_excel(df, sheet_name)
    titles = df_curr.columns.ravel().tolist()
    country_title = titles[0]
    countries = df_curr[country_title].tolist()

    dict = {}
    # loop over countries
    for i in range(len(countries)):
        for j in range(1, len(titles)):
            if type(df_curr.iloc[i][j]) == str:
                df_curr.iloc[i][j] = float("nan")
            data_point = [int(titles[j]), float(df_curr.iloc[i][j])]
            # Check if dict has the country or not.
            if countries[i] in dict:
                dict[countries[i]].append(data_point)
            else:
                dict[countries[i]] = [data_point]
    return dict
