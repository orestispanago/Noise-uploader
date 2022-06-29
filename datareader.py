import pandas as pd
import glob
import datetime

csv_files = glob.glob("*.txt") 

def date_parser(date_string):
    return datetime.datetime.strptime(date_string, "%y/%m/%d %H:%M:%S")

df_list = []
for f in csv_files:
    df = pd.read_csv(f, names=["date_time","temp", "batt",
                               "min_noise_db","max_noise_db"],
                     date_parser=date_parser, index_col="date_time",
                     sep="; ", comment=";", engine="python")
    df_list.append(df)
    
df_all = pd.concat(df_list)
df_all = df_all.resample('2min').mean()