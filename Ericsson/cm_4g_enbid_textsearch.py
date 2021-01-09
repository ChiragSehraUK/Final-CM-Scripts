import pandas as pd
import glob
import re

files = []

file_path = "/home/valiance/Desktop/Cardinality/Country Data/CM Data/VFES/4G/data/"

for xml in glob.glob(file_path + "*"):
    files.append(xml)

sortedFileNames = sorted(files, key=lambda x: x.rsplit('/')[-1].rsplit('_'))

nd = dict()
masterlist_enbid = []
masterlist_sctpRef = []
masterlist_sctpRef_join = []

for f in sortedFileNames:
    for xml_file in glob.glob(f):
        new = xml_file.replace("/home/valiance/Desktop/Cardinality/Country Data/CM Data/VFES/4G/data/", "")
        print(new)
        with open(xml_file, "r") as f:
            s = f.read()
            vsDataENodeBFunction = re.findall("<es:vsDataENodeBFunction>(.*?)</es:vsDataENodeBFunction>", s)

            for i in vsDataENodeBFunction:
                enbid = re.search("<es:eNBId>(.*?)</es:eNBId>", i)
                masterlist_enbid.append(enbid.group().split(">")[1].split("<")[0])

                sctpReftag = re.search("<es:sctpRef>(.*?)</es:sctpRef>", i)
                sctpRef = sctpReftag.group().split(">")[1].split("<")[0]
                masterlist_sctpRef.append(sctpRef)

                sctpRef_values = sctpRef.split(",")
                sctpRef_str = ",".join(sctpRef_values[0:3])
                masterlist_sctpRef_join.append(sctpRef_str)

with open(sortedFileNames[-1], "r") as read_file:
    value = read_file.read().replace("\n", "")
    datetime = re.findall("<fileFooter(.*?)/>", value)[0].split("=")[-1].strip('"')

nd["eNBId"] = masterlist_enbid
nd["sctpRef"] = masterlist_sctpRef
nd["join_reference"] = masterlist_sctpRef_join
nd["datetime"] = [datetime for i in masterlist_enbid]

dataf = pd.DataFrame.from_dict(nd)
dataf.to_csv("cm_files/4G/4G_eNBId.csv", index=False)
