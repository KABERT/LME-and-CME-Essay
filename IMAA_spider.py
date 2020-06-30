from bs4 import BeautifulSoup
import requests
import csv


def getHTML(url):
    kv = {'user-agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, timeout=10, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "error"


def split_helper(content):
    # split years first
    year_start, year_end = content.find("["), content.find("]")
    years = content[year_start:year_end].strip('][').split(",")
    for i in range(len(years)):
        if len(years[i]) > 6:
            years[i] = years[i][:6]
        years[i] = int(years[i][1:-1])

    # Split var next
    var_start, var_end = content.find("[", year_end+1), content.find("]", year_end+1)
    var = content[var_start:var_end].strip('][').split(",")
    for i in range(len(var)):
        var[i] = int(var[i])

    # Split Currency in the end
    currency_start, currency_end = content.find("[", var_end + 1), content.find("]", var_end + 1)
    currency = content[currency_start:currency_end].strip('][').split(",")
    for i in range(len(currency)):
        currency[i] = float(currency[i])

    # Split the country name
    country_name_start = content.find("Acquisitions", currency_end + 1)
    if country_name_start == -1:
        country_name_start = content.find("Acquisition", currency_end + 1)
    country_name = content[country_name_start + len("Acquisitions"):].strip("\' ")
    return years, var, currency, country_name


def washing_data(html):
    soup = BeautifulSoup(html, features='lxml')
    raw_data = soup.find_all("script", {"type":"text/javascript"})
    year_collection, var_collection, currency_collection, name_collection = [], [], [], []
    for info in raw_data:
        scentence = info.get_text()
        # Check if the sentence is wanted
        if "years" in scentence:
            # Slice off the information that is no needed.
            position = scentence.find(";var chartid")
            # Make sure the substring is always in the scentence.
            if position != -1:
                year, var_number, currency_number, country_name = split_helper(scentence[:position])
                year_collection.append(year)
                var_collection.append(var_number)
                currency_collection.append(currency_number)
                name_collection.append(country_name)
            # Output there is an error has been occured
            else:
                print("There is no such substring in this scentence")
    return year_collection, var_collection, currency_collection, name_collection


def convert_data_into_csv(years, subject, country_name, path):
    # Wash the data and get ready to be written in the CSV
    data_collection = []
    for i in range(len(years)):
        dict_subject = {"Country Name": country_name[i]}
        for j in range(len(years[i])):
            dict_subject[years[i][j]] = subject[i][j]
        data_collection.append(dict_subject)

    f = open(path, "w")
    writer = csv.DictWriter(f, fieldnames=["Country Name", 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994,
                                           1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,
                                           2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
                            )
    writer.writeheader()
    for data in data_collection:
        writer.writerow(data)
    f.close()


if __name__ == "__main__":
    url = "https://imaa-institute.org/m-and-a-statistics-countries/"
    html = getHTML(url)
    years, var, curr, name = washing_data(html)
    convert_data_into_csv(years, var, name, "data/Var.csv")
    convert_data_into_csv(years, curr, name, "data/Currency.csv")
