import pandas as pd
import openpyxl



def writeToFile(data, filename):
    d = pd.DataFrame.from_dict(data)
    df = pd.DataFrame(data=d, index=None)
    df.to_excel(filename, index=False)


def read_xlsx(filename):
    return pd.read_excel(filename, encoding='utf-8', keep_default_na=False)


def test(filename):
    data = read_xlsx(filename)
    print(data[:100])

directory = "C:/Users/CCS/Documents/Election Data/Election-0.xlsx"
test(directory)
