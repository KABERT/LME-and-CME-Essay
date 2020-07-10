import pandas as pd


def clean(path="data/foreigncitation.tsv"):
    df = pd.read_csv(path, sep='\t')

    dict = {}
    for i in range(df.shape[0]):
        row = df.iloc[i]
        try:
            year, country, category = row[2][:4], row[4], row[-2]
            # Make sure country is not None
            if country == "":
                country = " "
            # Check if country is in the dictionary
            if country not in dict:
                dict[country] = {}
            # Check if year is in the dictionary
            data = dict[country]
            if year not in data:
                data[year] = [0, 0, 0]
            if category == "cited by applicant":
                data[year][0] += 1
            elif category == "cited by others":
                data[year][1] += 1
            else:
                data[year][2] += 1
        except:
            print(i)
    print(dict)




if __name__ == "__main__":
    clean()
