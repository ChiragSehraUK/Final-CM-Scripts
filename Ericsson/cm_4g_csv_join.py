import pandas as pd

df1 = pd.read_csv("cm_files/4G/4G_vsDataFDD.csv")
df2 = pd.read_csv("cm_files/4G/4G_eNBId.csv")


df = pd.merge(df1, df2, on="join_reference")
df.to_csv("cm_files/4G/Flattened_4G_ES_20200818.csv", index=False)
