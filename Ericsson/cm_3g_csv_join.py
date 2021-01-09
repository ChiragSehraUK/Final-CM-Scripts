import pandas as pd


df1 = pd.read_csv("cm_files/3G/3G_utrancell.csv")
df2 = pd.read_csv("cm_files/3G/3G_rncfunction.csv")


# df1 = pd.read_csv("cm_files/3G/3G_vsDataUtrancell.csv")
# df2 = pd.read_csv("cm_files/3G/3G_vsDataRncfunction.csv")


df = pd.merge(df1, df2, on="join_reference")
df.to_csv("cm_files/3G/Flattened_3G_RO_20200430.csv", index=False)
