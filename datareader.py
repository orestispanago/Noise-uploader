import pandas as pd
import glob
import datetime
import json

csv_files = glob.glob("22/*/*/*.txt") 

def date_parser(date_string):
    return datetime.datetime.strptime(date_string, "%y/%m/%d %H:%M:%S")

df_list = []
skipped_files=0
for f in csv_files:
    try:    
        df = pd.read_csv(f, names=["date_time","temp", "batt",
                                   "min_noise_db","max_noise_db"],
                         date_parser=date_parser, index_col="date_time",
                         sep="; ", comment=";", engine="python")
        df_list.append(df)
    except:
        skipped_files +=1
        
df_all = pd.concat(df_list)
df_all = df_all.resample('2min').mean()

df_all.to_csv("output.csv")

nans = df_all.isna().any(axis=1).sum()
report = {
    "Start date": str(df_all.index[0]),
    "End date": str(df_all.index[-1]),
    "Total files": len(csv_files),
    "Read": len(csv_files) - skipped_files,
    "Skipped": skipped_files,
    "Timeseries length": len(df_all),
    "Missing rows": int(nans),
    "Missing rows (%)": round(100*nans/len(df_all),2)}

with open('report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=4)
