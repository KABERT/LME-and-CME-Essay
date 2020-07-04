import pandas as pd
import csv
from openpyxl import load_workbook


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
            if df_curr.iloc[i][j] == ".." or df_curr.iloc[i][j] == "":
                df_curr.iloc[i][j] = float("nan")
            data_point = [int(titles[j]), float(df_curr.iloc[i].tolist()[j])]
            # Check if dict has the country or not.
            if countries[i] in dict:
                dict[countries[i]].append(data_point)
            else:
                dict[countries[i]] = [data_point]
    return dict


def joint_dictionary_together(first, second):
    if first == {}:
        first = second
    else:
        for k, v in second.items():
            # Check if the first dictionary has this country
            if k not in first:
                first[k] = second[k]
            for items in v:
                yr = items[0]
                flag = False
                for first_item in first[k]:
                    if first_item[0] == yr:
                        first_item[1] += items[1]
                        flag = True
                if not flag:
                    first[k].append(items)
    return first


def invert_dict_to_lst(dict, SME):
    X, y = [], []
    all_target_country, _, code = read_all_target_country()
    for country in all_target_country:
        if country in dict:
            data = dict[country]
            country_type = code[all_target_country.index(country)]
            if not SME:
                if country_type != 0:
                    X += data
                    y += [country_type] * len(data)
            else:
                X += data
                y += [country_type] * len(data)
    return X, y


def dict_to_write_helper(data_collection, target_countries, country_copy, df_name):
    lst_data, lst_yr = [], []
    for country in target_countries:
        if country not in data_collection:
            print(df_name, "is Missing: ", country_copy[target_countries.index(country)])
        else:
            lst_data.append(data_collection[country][1])
            lst_yr.append(data_collection[country][0])

    data_collection = []
    for i in range(len(lst_yr)):
        dict_subject = {"Country Name": country_copy[i]}
        for j in range(len(lst_yr[i])):
            dict_subject[lst_yr[i][j]] = lst_data[i][j]
        data_collection.append(dict_subject)

    f = open("data/temp.csv", "w")
    writer = csv.DictWriter(f, fieldnames=["Country Name", 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,
                                           2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
                            )
    writer.writeheader()
    for data in data_collection:
        writer.writerow(data)
    f.close()
    df_temp = pd.read_csv("data/temp.csv")
    # append_df_to_excel(df_temp, df_name)


def append_df_to_excel(df, sheet_name):
    path = "data/Washed_DD_T2_Five_Spheres_All_in_One.xlsx"
    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine='openpyxl')
    writer.book = book

    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
    writer.close()


def reformate_dict_to_output(dict):
    for keys in dict:
        data = dict[keys]
        yr_lst, data_lst = [], []
        for i in range(len(dict[keys])):
            yr_lst.append(data[i][0])
            data_lst.append(data[i][1]/2)
        dict[keys] = [yr_lst, data_lst]
    return dict

