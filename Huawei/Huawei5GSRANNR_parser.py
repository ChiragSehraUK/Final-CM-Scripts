import xml.etree.ElementTree as ET
import glob
import pandas as pd
import os
import csv
import time
import argparse
import shutil

parser = argparse.ArgumentParser(description="Arguments for 5G CM files")
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

for xml_file in glob.glob(sourcePath + "/SRANNBIExport_XML_NR*"):
	print(xml_file)
	tree = ET.parse(xml_file)
	root = tree.getroot()

	new_xml_file = xml_file
	gnodebfunction_list = list()
	nrcell_list = list()
	nrducell_list = list()
	nrducellalgoswitch_list = list()
	nrducellop_list = list()

	for filefooter in root.findall("{http://www.huawei.com/specs/SRAN}filefooter"):
		date_time = filefooter.attrib["datetime"]

	for netag in root.iter("{http://www.huawei.com/specs/SRAN}NE"):
		for moduletag in netag:
			for moitag in moduletag:
				if moitag.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == "GNODEBFUNCTION":
					gnodebfunction_dict = dict(gnodebfunction_gnbid=None, gnodebfunction_gnodebfunctionname=None,
					                           neversion=None)
					for attributetag in moitag:
						for btstag in attributetag:
							if btstag.tag == "{http://www.huawei.com/specs/SRAN}GNBID":
								gnodebfunction_dict['gnodebfunction_gnbid'] = btstag.text
								gnodebfunction_dict['neversion'] = netag.attrib["neversion"]

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}GNODEBFUNCTIONNAME":
								gnodebfunction_dict["gnodebfunction_gnodebfunctionname"] = btstag.text
					gnodebfunction_list.append(gnodebfunction_dict)

				if moitag.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == "NRCELL":
					nrcell_dict = dict(nrcell_cellactivestate=None, nrcell_cellname=None, nrcell_nrcellid=None,
					                   gcell_cellname=None, gnodebfunction_gnodebfunctionname=None)
					for attributetag in moitag:
						for btstag in attributetag:
							if btstag.tag == "{http://www.huawei.com/specs/SRAN}CELLACTIVESTATE":
								nrcell_dict["nrcell_cellactivestate"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}CELLNAME":
								nrcell_dict["nrcell_cellname"] = btstag.text
								nrcell_dict["gnodebfunction_gnodebfunctionname"] = btstag.text[:-1]

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}NRCELLID":
								nrcell_dict["nrcell_nrcellid"] = btstag.text
					nrcell_list.append(nrcell_dict)

				if moitag.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == "NRDUCELL":
					nrducell_dict = dict(
						nrducell_cellid=None, nrducell_dlbandwidth=None, nrducell_dlnarfcn=None,
						nrducell_duplexmode=None, nrducell_frequencyband=None, nrducell_lampsitecellflag=None,
						nrducell_nrducellactivestate=None, nrducell_nrducellid=None, nrducell_nrducellname=None,
						nrducell_physicalcellid=None, nrducell_slotassignment=None, nrducell_subcarrierspacing=None,
						nrducell_trackingareaid=None, nrducell_ulbandwidth=None, nrducell_ulnarfcn=None
					)
					for attributetag in moitag:
						for btstag in attributetag:
							if btstag.tag == "{http://www.huawei.com/specs/SRAN}CELLID":
								nrducell_dict["nrducell_cellid"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}DLBANDWIDTH":
								nrducell_dict["nrducell_dlbandwidth"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}DLNARFCN":
								nrducell_dict["nrducell_dlnarfcn"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}DUPLEXMODE":
								nrducell_dict["nrducell_duplexmode"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}FREQUENCYBAND":
								nrducell_dict["nrducell_frequencyband"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}LAMPSITECELLFLAG":
								nrducell_dict["nrducell_lampsitecellflag"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}NRDUCELLACTIVESTATE":
								nrducell_dict["nrducell_nrducellactivestate"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}NRDUCELLID":
								nrducell_dict["nrducell_nrducellid"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}NRDUCELLNAME":
								nrducell_dict["nrducell_nrducellname"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}PHYSICALCELLID":
								nrducell_dict["nrducell_physicalcellid"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}SLOTASSIGNMENT":
								nrducell_dict["nrducell_slotassignment"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}SUBCARRIERSPACING":
								nrducell_dict["nrducell_subcarrierspacing"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}TRACKINGAREAID":
								nrducell_dict["nrducell_trackingareaid"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}ULBANDWIDTH":
								nrducell_dict["nrducell_ulbandwidth"] = btstag.text

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}ULNARFCN":
								nrducell_dict["nrducell_ulnarfcn"] = btstag.text

					nrducell_list.append(nrducell_dict)

				if moitag.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == "NRDUCELLALGOSWITCH":
					nrducellalgoswitch_dict = {'nrducellalgoswitch_spectrumcloudswitch': None}
					for attributetag in moitag:
						for btstag in attributetag:
							if btstag.tag == "{http://www.huawei.com/specs/SRAN}SPECTRUMCLOUDSWITCH":
								nrducellalgoswitch_dict["nrducellalgoswitch_spectrumcloudswitch"] = btstag.text

					nrducellalgoswitch_list.append(nrducellalgoswitch_dict)
				if moitag.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == "NRDUCellOp":
					nrducellop_dict = {'nrducellop_operatorid': None}
					for attributetag in moitag:
						for btstag in attributetag:
							if btstag.tag == "{http://www.huawei.com/specs/SRAN}OperatorId":
								nrducellop_dict["nrducellop_operatorid"] = btstag.text
					nrducellop_list.append(nrducellop_dict)

	if not os.path.exists(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"):
		os.makedirs(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/")

	filenames = {
		"GNODEBFUNCTION.csv": gnodebfunction_list, "NRCELL.csv": nrcell_list, "NRDUCELL.csv": nrducell_list,
		# "NRDUCELLALGOSWITCH.csv": nrducellalgoswitch_list, "NRDUCellOp.csv": nrducellop_list
	}

	for key, value in filenames.items():
		with open(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + key,
		          "w") as write_file:
			if value:
				headers = value[0].keys()
				csv_writer = csv.DictWriter(write_file, fieldnames=headers)
				csv_writer.writeheader()
				csv_writer.writerows(value)

	gnodebfunction_file = pd.read_csv(
		tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[
			0] + "/" + "GNODEBFUNCTION.csv")
	nrcell_file = pd.read_csv(
		tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "NRCELL.csv")
	nrducell_file = pd.read_csv(
		tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "NRDUCELL.csv")
	# nrducellalgoswitch_file = pd.read_csv(
	# 	tempPath + "_Huawei_SRANNR_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[
	# 		0] + "/" + "NRDUCELLALGOSWITCH.csv")
	# nrducellop_list = pd.read_csv(
	# 	tempPath + "_Huawei_SRANNR_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "NRDUCELLOP.csv")

	nrcell_file["nrcell_cellname"] = nrcell_file["nrcell_cellname"].astype(str)
	nrducell_file["nrducell_nrducellname"] = nrducell_file["nrducell_nrducellname"].astype(str)
	gnodefunctionname_nrcell_merge = pd.merge(left=gnodebfunction_file, right=nrcell_file,
	                                          on="gnodebfunction_gnodebfunctionname")

	gnodefunctionname_nrcell_nrducell_merge = pd.merge(left=gnodefunctionname_nrcell_merge, right=nrducell_file,
	                                          left_on="nrcell_cellname", right_on="nrducell_nrducellname")

	gnodefunctionname_nrcell_nrducell_merge["datetime"] = date_time
	gnodefunctionname_nrcell_nrducell_merge.to_csv(
		destinationPath + new_xml_file.rsplit("/")[-1].rsplit(".")[
			0] + ".csv", index=False)

	# deleting the folder of files created
	print("Deleting the temporary created folders...")
	dir_path = tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0]
	shutil.rmtree(dir_path)
