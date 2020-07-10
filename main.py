import pandas as pd
from openpyxl import load_workbook

clean_by_row_lst = ['Collective Bargaining Coverage', "Employment Length < 1yr", "Employment Protection", ]


def get_country_info(path="data/target country.xlsx"):
    df = pd.read_excel(path)
    target_country_name, target_country_code, target_country_type = get_country_name(df), get_country_code(df), get_country_type(df)
    return target_country_name, target_country_code, target_country_type


def get_country_name(df):
    country_title = df.columns.ravel().tolist()[0]
    return strip_everything_in_lst(df[country_title].tolist())


def get_country_code(df):
    country_code_title = df.columns.ravel().tolist()[1]
    return strip_everything_in_lst(df[country_code_title].tolist())


def get_country_type(df):
    country_type_title = df.columns.ravel().tolist()[2]
    type_list = df[country_type_title].tolist()
    lst = []
    for i in range(len(type_list)):
        if type_list[i] == "LME":
            lst.append(1)
        elif type_list[i] == "CME":
            lst.append(-1)
        else:
            lst.append(0)
    return lst


def strip_everything_in_lst(lst):
    for i in range(len(lst)):
        if type(lst[i]) != float:
            lst[i] = lst[i].strip()
    return lst


def clean_all_data(input_path="data/DD_T2_Five_Spheres_All_in_One.xlsx", output_path="data/washed.xlsx"):
    df = pd.ExcelFile(input_path)
    sheets, df_collection = df.sheet_names[1:], []
    for i in range(len(sheets)):
        df_curr = pd.read_excel(df, sheets[i])
        # Check which type of the excel it is.
        if "Time" not in df_curr.columns.ravel().tolist():
            df_collection.append(clean_data_by_rows(df_curr, sheets[i]))
        else:
            df_collection.append(clean_data_by_name(df_curr, sheets[i]))
    write_df_to_excel(df_collection, output_path, sheets)



def clean_data_by_rows(df, sheet_name):
    r_df = pd.DataFrame()
    country_title = df.columns.ravel().tolist()[0]
    country_in_df = strip_everything_in_lst(df[country_title].tolist())
    target_country, target_code, _ = get_country_info()
    # Check it is country name or country code
    if len(country_in_df[1]) == 3:
        is_code = True
    else:
        is_code = False
    for i in range(len(target_country)):
        if not is_code:
            # Extract the wanted
            if target_country[i] in country_in_df:
                index = country_in_df.index(target_country[i])
                row = df.loc[index]
                r_df = r_df.append([pd.DataFrame(row).T])
            else:
                print(sheet_name + "is Missing: " + target_country[i])
                r_df = r_df.append(pd.Series(), ignore_index=True)
                r_df.iloc[i][0] = target_country[i]
        else:
            # if the id is country code. Not Executed in this project currently.
            if target_country[i] in country_in_df:
                index = country_in_df.index(target_country[i])
                row = df.loc[index]
                row[0] = target_country[i]
                r_df = r_df.append([pd.DataFrame(row).T])
            else:
                print(sheet_name + "is Missing: " + target_country[i])

    return wash_the_unused_col(r_df)


def clean_data_by_name(df, sheet_name, target=("WC_rights", "COORD", "25_34", "PC_25_64", "TOT", "UPPSRY_NTRY")):
    country_title = df.columns.ravel().tolist()[0]
    country_in_df = df[country_title].tolist()
    all_data = {}
    target_country, target_code, _ = get_country_info()
    # Check it is country name or country code
    print(sheet_name)
    if len(country_in_df[1]) == 3:
        is_code = True
    else:
        is_code = False
    # Check if all the target is in the dataframe.
    for i in range(len(target_country)):
        if is_code:
            if target_code[i] not in country_in_df:
                print(sheet_name + "is Missing: " + target_country[i])
        else:
            if target_country[i] not in country_in_df:
                print(sheet_name + "is Missing: " + target_country[i])
    yr_pos, objective_pos, val_pos = get_pos_helper(df)

    for i in range(len(country_in_df)):
        if not is_code:
            # Extract the code that is wanted
            if country_in_df[i] in target_country and df.iloc[i].tolist()[objective_pos] in target and\
                    2000 <= df.iloc[i][yr_pos] <= 2018:
                yr, val = df.iloc[i][yr_pos], df.iloc[i][val_pos]
                if country_in_df[i] in all_data:
                    all_data[country_in_df[i]][0].append(yr)
                    all_data[country_in_df[i]][1].append(val)
                else:
                    all_data[country_in_df[i]] = [[yr], [val]]
        else:
            if country_in_df[i] in target_code and df.iloc[i].tolist()[objective_pos] in target and\
                    2000 <= df.iloc[i][yr_pos] <= 2018:
                country_name = target_country[target_code.index(country_in_df[i])]
                yr, val = df.iloc[i][yr_pos], df.iloc[i][val_pos]
                if country_name in all_data:
                    all_data[country_name][0].append(yr)
                    all_data[country_name][1].append(val)
                else:
                    all_data[country_name] = [[yr], [val]]
    return reformat_dict_to_df(all_data)


def interpolation_data():
    pass


def plot_data():
    pass


def get_pos_helper(df):
    title = df.columns.ravel().tolist()
    return title.index("Time"), title.index("Subject"), title.index("Value")


def reformat_dict_to_df(all_data):
    all_year = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016,
                2017, 2018]
    for country in all_data:
        for i in range(len(all_year)):
            if all_year[i] not in all_data[country][0]:
                all_data[country][0].insert(i, all_year[i])
                all_data[country][1].insert(i, float("nan"))
    for country in all_data:
        all_data[country] = all_data[country][1]

    df_new = pd.DataFrame.from_dict(all_data, orient="index", columns=all_year)
    df_new.insert(0, "Country", df_new.index)
    return df_new


def write_df_to_excel(df_collection, output_path, sheets):
    for i in range(len(df_collection)):
        df = df_collection[i]
        if i == 0:
            df.to_excel(output_path, sheet_name=sheets[i], index=False)
        else:
            book = load_workbook(output_path)
            writer = pd.ExcelWriter(output_path, engine='openpyxl')
            writer.book = book

            df.to_excel(writer, sheet_name=sheets[i], index=False)
            writer.save()
            writer.close()


def wash_the_unused_col(df):
    titles, unused_col = df.columns.ravel().tolist(), []
    # Convert every column title into string
    for i in range(1, len(titles)):
        titles[i] = str(titles[i]).strip()
    df.columns = titles
    all_year = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016,
                2017, 2018]
    missing_yrs = []

    # Filtering the columns that is unnecessary.
    for i in range(1, len(titles)):
        if titles[i].isnumeric():
            if 2000 > int(titles[i]) or int(titles[i]) > 2018:
                unused_col.append(titles[i])
        else:
            unused_col.append(titles[i])

    for col in unused_col:
        df = df.drop(col, axis=1)

    # Adding the missing year to the column
    for i in range(len(all_year)):
        if str(all_year[i]) not in df:
            df.insert(i+1, str(all_year[i]), [""]*len(df[df.columns.ravel().tolist()[0]]))
    return df


if __name__ == "__main__":
    print(clean_all_data())
