import xml.etree.ElementTree as ET
import glob
import pandas as pd
import os
import csv
import time
import argparse
import shutil

parser = argparse.ArgumentParser(description="Arguments for 4G CM files")
parser.add_argument('COUNTRY', metavar='COUNTRY', type=str, help='country of CM files')
parser.add_argument('TECH', metavar='TECH', type=str, help='technology of CM files')
args = parser.parse_args()
country = args.COUNTRY
tech = args.TECH
vendor = 'huawei'

pathConfig_file = pd.read_csv("/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/pathConfig.csv")

for i in pathConfig_file.index:
	if pathConfig_file['country'][i].lower() == country.lower():
		sourcePath = pathConfig_file['sourcePath'][i]
		# destinationPath = pathConfig_file['destinationPath'][i]

tempPath = "/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/" + country + "/" + vendor + "/" + tech + "/"
destinationPath = "/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/" + country + "/" + vendor + "/" + tech \
                  + "/"

begin_time = time.time()
print("Starting to run the script at: {}".format(time.ctime(int(begin_time))))

print("Source Path is : {}".format(sourcePath))
print("Temporary data is saved at: {}".format(tempPath))
print("Destination Path is : {}".format(destinationPath))
files_to_process = list()
for files in glob.glob(sourcePath + "/*"):
	# print(files)
	if ("LTE" in files) or ("BTS" in files):
		files_to_process.append(files)
print(files_to_process)
for f in files_to_process:
	for xml_file in glob.glob(f):
		print(xml_file)
		tree = ET.parse(xml_file)
		root = tree.getroot()

		new_xml_file = xml_file
		enodebfunction_list = list()
		cell_list = list()

		for filefooter in root.findall("{http://www.huawei.com/specs/SRAN}filefooter"):
			date_time = filefooter.attrib["datetime"]

		for netag in root.iter("{http://www.huawei.com/specs/SRAN}NE"):
			for moduletag in netag:
				for moitag in moduletag:
					if moitag.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == "CELL":
						cell_dict = {'cell_cellname': None, 'cell_localcellid': None, 'cell_freqband': None,
						             'cell_ulearfcncfgind': None, 'cell_dlearfcn': None, 'cell_ulbandwidth': None,
						             'cell_dlbandwidth': None, 'cell_cellactivestate': None, 'cell_adminstate': None,
						             'cell_userlabel': None, "cell_enodefunction_join": None, "neversion": None}
						for attributetag in moitag:
							for btstag in attributetag:
								if btstag.tag == "{http://www.huawei.com/specs/SRAN}CELLNAME":
									cell_dict['cell_cellname'] = btstag.text
									cell_dict['cell_enodefunction_join'] = btstag.text[:-2]
									cell_dict['neversion'] = netag.attrib["neversion"]

								if btstag.tag == "{http://www.huawei.com/specs/SRAN}LOCALCELLID":
									cell_dict["cell_localcellid"] = btstag.text

								if btstag.tag == "{http://www.huawei.com/specs/SRAN}FREQBAND":
									cell_dict["cell_freqband"] = btstag.text

								if btstag.tag == "{http://www.huawei.com/specs/SRAN}ULEARFCNCFGIND":
									cell_dict["cell_ulearfcncfgind"] = btstag.text

								if btstag.tag == "{http://www.huawei.com/specs/SRAN}DLEARFCN":
									cell_dict["cell_dlearfcn"] = btstag.text

								if btstag.tag == "{http://www.huawei.com/specs/SRAN}ULBANDWIDTH":
									cell_dict["cell_ulbandwidth"] = btstag.text

								if btstag.tag == "{http://www.huawei.com/specs/SRAN}DLBANDWIDTH":
									cell_dict["cell_dlbandwidth"] = btstag.text

								if btstag.tag == "{http://www.huawei.com/specs/SRAN}CELLACTIVESTATE":
									cell_dict["cell_cellactivestate"] = btstag.text

								if btstag.tag == "{http://www.huawei.com/specs/SRAN}CELLADMINSTATE":
									cell_dict["cell_adminstate"] = btstag.text

								if btstag.tag == "{http://www.huawei.com/specs/SRAN}USERLABEL":
									cell_dict["cell_userlabel"] = btstag.text
						cell_list.append(cell_dict)

					if moitag.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == "ENODEBFUNCTION":
						enodebfunction_dict = {'enodebfunction_enodebfunctionname': None,
						                       'enodebfunction_enodebid': None,
						                       "cell_enodefunction_join": None}
						for attributetag in moitag:
							for btstag in attributetag:
								if btstag.tag == "{http://www.huawei.com/specs/SRAN}ENODEBFUNCTIONNAME":
									enodebfunction_dict["enodebfunction_enodebfunctionname"] = btstag.text
									enodebfunction_dict['cell_enodefunction_join'] = btstag.text[:-1]

								if btstag.tag == "{http://www.huawei.com/specs/SRAN}ENODEBID":
									enodebfunction_dict["enodebfunction_enodebid"] = btstag.text
						enodebfunction_list.append(enodebfunction_dict)

		if not os.path.exists(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"):
			os.makedirs(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/")

		filenames = {
			"CELL.csv": cell_list, "ENODEBFUNCTION.csv": enodebfunction_list
		}

		for key, value in filenames.items():
			with open(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + key,
			          "w") \
					as write_file:
				if value:
					headers = value[0].keys()
					csv_writer = csv.DictWriter(write_file, fieldnames=headers)
					csv_writer.writeheader()
					csv_writer.writerows(value)

		cell_file = pd.read_csv(
			tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" +
			"CELL.csv")
		enodebfunction_file = pd.read_csv(
			tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0]
			+ "/" + "ENODEBFUNCTION.csv")

		cell_enodebfunction_merge = pd.merge(left=cell_file, right=enodebfunction_file,
		                                     on="cell_enodefunction_join")

		cell_enodebfunction_merge["datetime"] = date_time
		cell_enodebfunction_merge.to_csv(
			destinationPath + new_xml_file.rsplit("/")[-1].rsplit(".")[
				0] + ".csv", index=False)

		# deleting the folder of files created
		print("Deleting the temporary created folders...")
		dir_path = tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0]
		shutil.rmtree(dir_path)
