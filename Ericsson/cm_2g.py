# Ericsson CM 2G Parser
# Allowed values for country:  VFRO VFDE
# Allowed values for tech: 2G

import pandas as pd
import csv
import xml.etree.ElementTree as ET
import glob
import os
import time
import argparse
import shutil

# parser = argparse.ArgumentParser(description="Arguments for 2G Ericsson CM files")
# parser.add_argument('COUNTRY', metavar='COUNTRY', type=str, help='country of CM files')
# parser.add_argument('TECH', metavar='TECH', type=str, help='technology of CM files')
# args = parser.parse_args()
# country = args.COUNTRY
# tech = args.TECH
# vendor = 'ericsson'
#
# pathConfig_file = pd.read_csv("/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/pathConfig.csv")
#
# for i in pathConfig_file.index:
# 	if pathConfig_file['country'][i].lower() == country.lower():
# 		sourcePath = pathConfig_file['sourcePath'][i]
#
# tempPath = "/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/" + country + "/" + vendor + "/" + tech + "/"
# destinationPath = "/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/" + country + "/" + vendor + "/" + tech \
#                   + "/"

file_path = "/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/CM-files/ericsson/"
file_name = "20200325.rn2osscs5_2G.txt"

domain_list = []
internal_cell_index = []
internal_cell_list = []
site_index = []
site_list = []
datetime = ""

with open(file_path + file_name, "r") as f:
	print(file_name)
	for index, line in enumerate(f):
		if ".utctime" in line:
			datetime = " ".join(line.split()[1:])
		if ".domain".lower() in line.strip().lower():
			domain_list.append((line.strip(), index + 1))

	for index, i in enumerate(domain_list):
		if i[0].lower() == ".domain INTERNAL_CELL".lower():
			internal_cell_index.append((i[1], domain_list[index + 1][1]))
		if i[0].lower() == ".domain SITE".lower():
			site_index.append((i[1], domain_list[index + 1][1]))

with open(file_path + file_name, "r") as f:
	internal_cell_id = ""
	s = f.readlines()

	for i in range(internal_cell_index[0][0], internal_cell_index[0][1]):
		if ".set " in s[i]:
			if s[i] not in internal_cell_id:
				if "PG" not in s[i]:
					internal_cell_id = s[i]
					temp_list1 = []
			else:
				internal_cell_dict = {
					"bsc_name": None, "cell_name": None, "ci": None, "mcc": None, "mnc": None,
					"trx_count": None, "c_sys_type": None, "cell_state": None, "cell_type": None,
					"lac": None, "rac": None, "bcchno": None, "join_reference": None
				}
				for data in temp_list1:
					if "BSC_NAME" == data.strip().split("=")[0]:
						internal_cell_dict["bsc_name"] = data.strip().split("=")[-1].replace('"', '')
					if "CELL_NAME" == data.strip().split("=")[0]:
						internal_cell_dict["cell_name"] = data.strip().split("=")[-1].replace('"', '')
					if "CI" == data.strip().split("=")[0]:
						internal_cell_dict["ci"] = data.strip().split("=")[-1].replace('"', '')
					if "MCC" == data.strip().split("=")[0]:
						internal_cell_dict["mcc"] = data.strip().split("=")[-1].replace('"', '')
					if "MNC" == data.strip().split("=")[0]:
						internal_cell_dict["mnc"] = data.strip().split("=")[-1].replace('"', '')
					if "TRX_COUNT" == data.strip().split("=")[0]:
						internal_cell_dict["trx_count"] = data.strip().split("=")[-1].replace('"', '')
					if "C_SYS_TYPE" == data.strip().split("=")[0]:
						internal_cell_dict["c_sys_type"] = data.strip().split("=")[-1].replace('"', '')
					if "CELL_STATE" == data.strip().split("=")[0]:
						internal_cell_dict["cell_state"] = data.strip().split("=")[-1].replace('"', '')
					if "CELL_TYPE" == data.strip().split("=")[0]:
						internal_cell_dict["cell_type"] = data.strip().split("=")[-1].replace('"', '')
					if "LAC" == data.strip().split("=")[0]:
						internal_cell_dict["lac"] = data.strip().split("=")[-1].replace('"', '')
					if "RAC" == data.strip().split("=")[0]:
						internal_cell_dict["rac"] = data.strip().split("=")[-1].replace('"', '')
					if "BCCHNO" == data.strip().split("=")[0]:
						internal_cell_dict["bcchno"] = data.strip().split("=")[-1].replace('"', '')
				internal_cell_dict["join_reference"] = internal_cell_id.split()[-1][:-2].replace('"', '')
				internal_cell_list.append(internal_cell_dict)
		else:
			temp_list1.append(s[i])

with open(file_path + file_name, "r") as f:
	site_id = ""
	s = f.readlines()

	for i in range(site_index[0][0], site_index[0][1]):
		if ".set " in s[i]:
			if s[i] not in site_id:
				if "PG" not in s[i]:
					site_id = s[i]
					temp_list2 = []
			else:
				site_dict = {
					"site_name": None, "join_reference": None, "datetime": None
				}
				for data in temp_list2:
					if "SITE_NAME" == data.strip().split("=")[0]:
						site_dict["site_name"] = data.strip().split("=")[-1].replace('"', '')
				site_dict["join_reference"] = site_id.split()[-1].replace('"', '')
				site_dict["datetime"] = datetime
				site_list.append(site_dict)
		else:
			temp_list2.append(s[i])

with open("/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/Ericsson/cm_files/2G/2g_internal_cell.csv", "w+") as internal_file:
	internal_headers = internal_cell_list[0].keys()
	internal_csv_writer = csv.DictWriter(internal_file, fieldnames=internal_headers)
	internal_csv_writer.writeheader()
	internal_csv_writer.writerows(internal_cell_list)

with open("/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/Ericsson/cm_files/2G/2g_site.csv", "w") as site_file:
	site_headers = site_list[0].keys()
	site_csv_writer = csv.DictWriter(site_file, fieldnames=site_headers)
	site_csv_writer.writeheader()
	site_csv_writer.writerows(site_list)

df1 = pd.read_csv("/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/Ericsson/cm_files/2G/2g_internal_cell.csv")
df2 = pd.read_csv("/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/Ericsson/cm_files/2G/2g_site.csv")

df = pd.merge(df1, df2, on="join_reference")
df.to_csv("/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/Ericsson/cm_files/2G/Flattened_2G_IE_20200702.csv", index=False)
