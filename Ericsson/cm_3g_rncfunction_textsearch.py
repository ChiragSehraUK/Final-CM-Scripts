import pandas as pd
import glob
import re

files = []

file_path = "/home/valiance/Desktop/Cardinality/Country Data/CM Data/new_data/VFDE/vfde-ERICSSON cm files/20200624.rn2enm401_3g/data/"

for xml in glob.glob(file_path + "*"):
    files.append(xml)

sortedFileNames = sorted(files, key=lambda x: x.rsplit('/')[-1].rsplit('_'))

nd = dict()
masterlist_rncType = []
masterlist_rnc_userlabel = []
masterlist_rncid = []
masterlist_cn_operator = []
masterlist_join_reference = []
masterlist_datetime = []

for f in sortedFileNames:
    for xml_file in glob.glob(f):
        new = xml_file.replace("/home/valiance/Desktop/Cardinality/Country Data/CM Data/new_data/VFDE/vfde-ERICSSON cm files/20200624.rn2enm401_3g/data/", "")

        print(new)
        with open(xml_file, "r") as f:
            s = f.read()
            # vsDataRncFunction = re.findall("<es:vsDataRncFunction>(?:.*\r?\n?)*?</es:vsDataRncFunction>", s, re.IGNORECASE)
            vsDataRncFunction = re.findall("<es:vsDataRncFunction>(.*?)</es:vsDataRncFunction>", s, re.IGNORECASE)

            for i in vsDataRncFunction:
                rncType = re.search("<es:rncType>(.*?)</es:rncType>", i, re.IGNORECASE)
                if rncType is not None:
                    masterlist_rncType.append(rncType.group().split(">")[1].split("<")[0])
                else:
                    masterlist_rncType.append(None)

                rnc_userLabel = re.search("<es:userLabel>(.*?)</es:userLabel>", i, re.IGNORECASE)
                if rnc_userLabel is not None:
                    masterlist_rnc_userlabel.append(rnc_userLabel.group().split(">")[1].split("<")[0])
                else:
                    masterlist_rnc_userlabel.append(None)

                rncid = re.search("<es:rncId>(.*?)</es:rncId>", i, re.IGNORECASE)
                if rncid is not None:
                    masterlist_rncid.append(rncid.group().split(">")[1].split("<")[0])
                else:
                    masterlist_rncid.append(None)

                cn_operator = re.search("<es:primaryCnOperatorRef>(.*?)</es:primaryCnOperatorRef>", i, re.IGNORECASE)
                values = cn_operator.group().split(">")[1].split("<")[0]
                masterlist_cn_operator.append(values)

                rnc_values = values.split(",")
                join_reference = ",".join(rnc_values[0:5])
                masterlist_join_reference.append(join_reference)

with open(sortedFileNames[-1], "r") as read_file:
    value = read_file.read().replace("\n", "")
    datetime = re.findall("<fileFooter(.*?)/>", value)[0].split("=")[-1].strip('"')

nd["rnc_userlabel"] = masterlist_rnc_userlabel
nd["rnc_id"] = masterlist_rncid
nd["cn_operator"] = masterlist_cn_operator
nd["rnc_type"] = masterlist_rncType
nd["join_reference"] = masterlist_join_reference
nd["datetime"] = [datetime for i in masterlist_cn_operator]

dataf = pd.DataFrame.from_dict(nd)
dataf.to_csv("cm_files/3G/3G_vsDataRncfunction.csv", index=False)


