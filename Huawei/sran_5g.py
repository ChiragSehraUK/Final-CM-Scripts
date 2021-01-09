import xml.etree.ElementTree as ET
import glob
from pprint import pprint
import pandas as pd
import csv
import time
import argparse
import shutil

parser = argparse.ArgumentParser(description="Arguments for 5G CM files")
parser.add_argument('COUNTRY', metavar='COUNTRY', type=str, help='country of CM files')
args = parser.parse_args()
country = args.COUNTRY

pathConfig_file = pd.read_csv("/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/pathConfig.csv")

for i in pathConfig_file.index:
	if pathConfig_file['country'][i].lower() == country.lower():
		sourcePath = pathConfig_file['sourcePath'][i]
		# destinationPath = pathConfig_file['destinationPath'][i]

tempPath = "/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/" + country
destinationPath = "/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/" + country

begin_time = time.time()
print("Starting to run the script at: {}".format(time.ctime(int(begin_time))))
print("Source Path is : {}".format(sourcePath))
print("Temporary data is saved at: {}".format(tempPath))
print("Destination Path is : {}".format(destinationPath))

for xml_file in glob.glob(sourcePath + "/SRANNBIExport_XML_NR*"):
	tree = ET.parse(xml_file)
	root = tree.getroot()

	new_xml_file = xml_file
	print(new_xml_file)

	for filefooter in root.findall("{http://www.huawei.com/specs/SRAN}filefooter"):
		date_time = filefooter.attrib["datetime"]

	# for netag in root.findall("{http://www.huawei.com/specs/SRAN}NE"):
	#    neversion = netag.attrib["neversion"]

	mm_gnodebfunction_gnbid_list = []
	mm_gnodebfunction_gnodebfunctionname_list = []
	mm_nrcell_cellactivestate_list = []
	mm_nrcell_cellname_list = []
	mm_nrcell_nrcellid_list = []
	mm_nrducell_cellid_list = []
	mm_nrducell_dlbandwidth_list = []
	mm_nrducell_dlnarfcn_list = []
	mm_nrducell_duplexmode_list = []
	mm_nrducell_frequencyband_list = []
	mm_nrducell_lampsitecellflag_list = []
	mm_nrducell_nrducellactivestate_list = []
	mm_nrducell_nrducellid_list = []
	mm_nrducell_nrducellname_list = []
	mm_nrducell_physicalcellid_list = []
	mm_nrducell_slotassignment_list = []
	mm_nrducell_subcarrierspacing_list = []
	mm_nrducell_trackingareaid_list = []
	mm_nrducell_ulbandwidth_list = []
	mm_nrducell_ulnarfcn_list = []
	mm_nrducellalgoswitch_spectrumcloudswitch_list = []
	mm_nrducellop_operatorid_list = []
	mm_datetime_list = []
	mm_neversion_list = []
	l = list()
	d = dict()

	for netag in root.iter("{http://www.huawei.com/specs/SRAN}NE"):
		neversion = netag.attrib["neversion"]
		for moduletag in netag:
			# define lists here
			gnodebfunction_gnbid_list, gnodebfunction_gnodebfunctionname_list = [], []
			nrcell_cellactivestate_list, nrcell_cellname_list, nrcell_nrcellid_list, nrcell_nrcellid_list = [], [], [], []
			nrducell_cellid_list = []
			nrducell_dlbandwidth_list = []
			nrducell_dlnarfcn_list = []
			nrducell_duplexmode_list = []
			nrducell_frequencyband_list = []
			nrducell_lampsitecellflag_list = []
			nrducell_nrducellactivestate_list = []
			nrducell_nrducellid_list = []
			nrducell_nrducellname_list = []
			nrducell_physicalcellid_list = []
			nrducell_slotassignment_list = []
			nrducell_subcarrierspacing_list = []
			nrducell_trackingareaid_list = []
			nrducell_ulbandwidth_list = []
			nrducell_ulnarfcn_list = []
			nrducellalgoswitch_spectrumcloudswitch_list, nrducellop_operatorid_list = [], []

			for moitag in moduletag:
				if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "GNODEBFUNCTION":
					for attributetag in moitag:
						for btstag in attributetag:
							if btstag.tag == "{http://www.huawei.com/specs/SRAN}GNBID":
								gnodebfunction_gnbid_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}GNODEBFUNCTIONNAME":
								gnodebfunction_gnodebfunctionname_list.append(btstag.text)

				if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "NRCELL":
					for attributetag in moitag:
						for btstag in attributetag:
							if btstag.tag == "{http://www.huawei.com/specs/SRAN}CELLACTIVESTATE":
								nrcell_cellactivestate_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}CELLNAME":
								nrcell_cellname_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}NRCELLID":
								if btstag.text is None:
									nrcell_nrcellid_list.append(None)
								else:
									nrcell_nrcellid_list.append(btstag.text)

				if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "NRDUCELL":
					for attributetag in moitag:
						for btstag in attributetag:
							if btstag.tag == "{http://www.huawei.com/specs/SRAN}CELLID":
								nrducell_cellid_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}DLBANDWIDTH":
								nrducell_dlbandwidth_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}DLNARFCN":
								if btstag.text is None:
									nrducell_dlnarfcn_list.append(None)
								else:
									nrducell_dlnarfcn_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}DUPLEXMODE":
								if btstag.text is None:
									nrducell_duplexmode_list.append(None)
								else:
									nrducell_duplexmode_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}FREQUENCYBAND":
								if btstag.text is None:
									nrducell_frequencyband_list.append(None)
								else:
									nrducell_frequencyband_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}LAMPSITECELLFLAG":
								if btstag.text is None:
									nrducell_lampsitecellflag_list.append(None)
								else:
									nrducell_lampsitecellflag_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}NRDUCELLACTIVESTATE":
								nrducell_nrducellactivestate_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}NRDUCELLID":
								nrducell_nrducellid_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}NRDUCELLNAME":
								if btstag.text is None:
									nrducell_nrducellname_list.append(None)
								else:
									nrducell_nrducellname_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}PHYSICALCELLID":
								if btstag.text is None:
									nrducell_physicalcellid_list.append(None)
								else:
									nrducell_physicalcellid_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}SLOTASSIGNMENT":
								if btstag.text is None:
									nrducell_slotassignment_list.append(None)
								else:
									nrducell_slotassignment_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}SUBCARRIERSPACING":
								if btstag.text is None:
									nrducell_subcarrierspacing_list.append(None)
								else:
									nrducell_subcarrierspacing_list.append(btstag.text)

							if btstag.tag == "{http://www.huawei.com/specs/SRAN}TRACKINGAREAID":
								if btstag.text is None:
									nrducell_trackingareaid_list.append(None)
								else:
									nrducell_trackingareaid_list.append(btstag.text)
							if btstag.tag == "{http://www.huawei.com/specs/SRAN}ULBANDWIDTH":
								if btstag.text is None:
									nrducell_ulbandwidth_list.append(None)
								else:
									nrducell_ulbandwidth_list.append(btstag.text)
							if btstag.tag == "{http://www.huawei.com/specs/SRAN}ULNARFCN":
								if btstag.text is None:
									nrducell_ulnarfcn_list.append(None)
								else:
									nrducell_ulnarfcn_list.append(btstag.text)

				if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "NRDUCELLALGOSWITCH":
					for attributetag in moitag:
						for btstag in attributetag:
							if btstag.tag == "{http://www.huawei.com/specs/SRAN}SPECTRUMCLOUDSWITCH":
								nrducellalgoswitch_spectrumcloudswitch_list.append(btstag.text)

				if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "NRDUCellOp":
					for attributetag in moitag:
						for btstag in attributetag:
							if btstag.tag == "{http://www.huawei.com/specs/SRAN}OperatorId":
								nrducellop_operatorid_list.append(btstag.text)

			d['gnodebfunction_gnbid'] = gnodebfunction_gnbid_list
			d['gnodebfunction_gnodebfunctionname'] = gnodebfunction_gnodebfunctionname_list
			d['nrcell_cellactivestate'] = nrcell_cellactivestate_list
			d['nrcell_cellname'] = nrcell_cellname_list
			d['nrcell_nrcellid'] = nrcell_nrcellid_list
			d['nrducell_cellid'] = nrducell_cellid_list
			d['nrducell_dlbandwidth'] = nrducell_dlbandwidth_list
			d['nrducell_dlnarfcn'] = nrducell_dlnarfcn_list
			d['nrducell_duplexmode'] = nrducell_duplexmode_list
			d['nrducell_frequencyband'] = nrducell_frequencyband_list
			d['nrducell_lampsitecellflag'] = nrducell_lampsitecellflag_list
			d['nrducell_nrducellactivestate'] = nrducell_nrducellactivestate_list
			d['nrducell_nrducellid'] = nrducell_nrducellid_list
			d['nrducell_nrducellname'] = nrducell_nrducellname_list
			d['nrducell_physicalcellid'] = nrducell_physicalcellid_list
			d['nrducell_slotassignment'] = nrducell_slotassignment_list
			d['nrducell_subcarrierspacing'] = nrducell_subcarrierspacing_list
			d['nrducell_trackingareaid'] = nrducell_trackingareaid_list
			d['nrducell_ulbandwidth'] = nrducell_ulbandwidth_list
			d['nrducell_ulnarfcn'] = nrducell_ulnarfcn_list
			d['nrducellalgoswitch_spectrumcloudswitch'] = nrducellalgoswitch_spectrumcloudswitch_list
			d['nrducellop_operatorid'] = nrducellop_operatorid_list

			# print(d["gnodebfunction_gnbid"])
			# print(d["nrcell_cellname"])
			master_gnodebfunction_gnbid_list = []
			master_gnodebfunction_gnodebfunctionname_list = []
			master_nrcell_cellactivestate_list = []
			master_nrcell_cellname_list = []
			master_nrcell_nrcellid_list = []
			master_nrducell_cellid_list = []
			master_nrducell_dlbandwidth_list = []
			master_nrducell_dlnarfcn_list = []
			master_nrducell_duplexmode_list = []
			master_nrducell_frequencyband_list = []
			master_nrducell_lampsitecellflag_list = []
			master_nrducell_nrducellactivestate_list = []
			master_nrducell_nrducellid_list = []
			master_nrducell_nrducellname_list = []
			master_nrducell_physicalcellid_list = []
			master_nrducell_slotassignment_list = []
			master_nrducell_subcarrierspacing_list = []
			master_nrducell_trackingareaid_list = []
			master_nrducell_ulbandwidth_list = []
			master_nrducell_ulnarfcn_list = []
			master_nrducellalgoswitch_spectrumcloudswitch_list = []
			master_nrducellop_operatorid_list = []

			new_gnodebfunction_gnbid_list, new_gnodebfunction_gnodebfunctionname_list = [], []
			new_nrcell_nrcellname_list, new_nrcell_nrcellid_list = [], []

			for c, cellname in enumerate(d["nrcell_cellname"]):
				for n, nodebname in enumerate(d["gnodebfunction_gnodebfunctionname"]):
					new_nrcell_nrcellname_list.append(cellname)
					new_nrcell_nrcellid_list.append(d["nrducell_nrducellid"][c])
					new_gnodebfunction_gnodebfunctionname_list.append(nodebname)
					new_gnodebfunction_gnbid_list.append(d["gnodebfunction_gnbid"][0])

			# print("new_gnodebfunction_gnodebfunctionname_list", new_gnodebfunction_gnodebfunctionname_list)
			# print("new_nrcell_nrcellname_list", new_nrcell_nrcellname_list)

			if d["nrcell_cellname"]:
				for i in range(0, len(new_nrcell_nrcellname_list)):
					master_nrcell_cellname_list.append(new_nrcell_nrcellname_list[i])
					master_nrcell_nrcellid_list.append(new_nrcell_nrcellid_list[i])
					master_gnodebfunction_gnodebfunctionname_list.append(new_gnodebfunction_gnodebfunctionname_list[i])
					master_gnodebfunction_gnbid_list.append(new_gnodebfunction_gnbid_list[i])

					if i >= len(nrcell_cellactivestate_list):
						master_nrcell_cellactivestate_list.append(None)
					else:
						master_nrcell_cellactivestate_list.append(nrcell_cellactivestate_list[i])

					if i >= len(nrducell_cellid_list):
						master_nrducell_cellid_list.append(None)
					else:
						master_nrducell_cellid_list.append(nrducell_cellid_list[i])

					if i >= len(nrducell_dlbandwidth_list):
						master_nrducell_dlbandwidth_list.append(None)
					else:
						master_nrducell_dlbandwidth_list.append(nrducell_dlbandwidth_list[i])

					if i >= len(nrducell_dlnarfcn_list):
						master_nrducell_dlnarfcn_list.append(None)
					else:
						master_nrducell_dlnarfcn_list.append(nrducell_dlnarfcn_list[i])

					if i >= len(nrducell_frequencyband_list):
						master_nrducell_frequencyband_list.append(None)
					else:
						master_nrducell_frequencyband_list.append(nrducell_frequencyband_list[i])

					if i >= len(nrducell_duplexmode_list):
						master_nrducell_duplexmode_list.append(None)
					else:
						master_nrducell_duplexmode_list.append(nrducell_duplexmode_list[i])

					if i >= len(nrducell_nrducellactivestate_list):
						master_nrducell_nrducellactivestate_list.append(None)
					else:
						master_nrducell_nrducellactivestate_list.append(nrducell_nrducellactivestate_list[i])

					if i >= len(nrducell_lampsitecellflag_list):
						master_nrducell_lampsitecellflag_list.append(None)
					else:
						master_nrducell_lampsitecellflag_list.append(nrducell_lampsitecellflag_list[i])

					if i >= len(nrducell_nrducellid_list):
						master_nrducell_nrducellid_list.append(None)
					else:
						master_nrducell_nrducellid_list.append(nrducell_nrducellid_list[i])

					if i >= len(nrducell_nrducellname_list):
						master_nrducell_nrducellname_list.append(None)
					else:
						master_nrducell_nrducellname_list.append(nrducell_nrducellname_list[i])

					if i >= len(nrducell_physicalcellid_list):
						master_nrducell_physicalcellid_list.append(None)
					else:
						master_nrducell_physicalcellid_list.append(nrducell_physicalcellid_list[i])

					if i >= len(nrducell_slotassignment_list):
						master_nrducell_slotassignment_list.append(None)
					else:
						master_nrducell_slotassignment_list.append(nrducell_slotassignment_list[i])

					if i >= len(nrducell_subcarrierspacing_list):
						master_nrducell_subcarrierspacing_list.append(None)
					else:
						master_nrducell_subcarrierspacing_list.append(nrducell_subcarrierspacing_list[i])

					if i >= len(nrducell_trackingareaid_list):
						master_nrducell_trackingareaid_list.append(None)
					else:
						master_nrducell_trackingareaid_list.append(nrducell_trackingareaid_list[i])

					if i >= len(nrducell_ulbandwidth_list):
						master_nrducell_ulbandwidth_list.append(None)
					else:
						master_nrducell_ulbandwidth_list.append(nrducell_ulbandwidth_list[i])

					if i >= len(nrducell_ulnarfcn_list):
						master_nrducell_ulnarfcn_list.append(None)
					else:
						master_nrducell_ulnarfcn_list.append(nrducell_ulnarfcn_list[i])

					if i >= len(nrducellalgoswitch_spectrumcloudswitch_list):
						master_nrducellalgoswitch_spectrumcloudswitch_list.append(None)
					else:
						master_nrducellalgoswitch_spectrumcloudswitch_list.append(
							nrducellalgoswitch_spectrumcloudswitch_list[i])

					if i >= len(nrducellop_operatorid_list):
						master_nrducellop_operatorid_list.append(None)
					else:
						master_nrducellop_operatorid_list.append(nrducellop_operatorid_list[i])

			mm_gnodebfunction_gnbid_list.extend(master_gnodebfunction_gnbid_list)
			mm_gnodebfunction_gnodebfunctionname_list.extend(master_gnodebfunction_gnodebfunctionname_list)
			mm_nrcell_cellactivestate_list.extend(master_nrcell_cellactivestate_list)
			mm_nrcell_cellname_list.extend(master_nrcell_cellname_list)
			mm_nrcell_nrcellid_list.extend(master_nrcell_nrcellid_list)
			mm_nrducell_cellid_list.extend(master_nrducell_cellid_list)
			mm_nrducell_dlbandwidth_list.extend(master_nrducell_dlbandwidth_list)
			mm_nrducell_dlnarfcn_list.extend(master_nrducell_dlnarfcn_list)
			mm_nrducell_duplexmode_list.extend(master_nrducell_duplexmode_list)
			mm_nrducell_frequencyband_list.extend(master_nrducell_frequencyband_list)
			mm_nrducell_lampsitecellflag_list.extend(master_nrducell_lampsitecellflag_list)
			mm_nrducell_nrducellactivestate_list.extend(master_nrducell_nrducellactivestate_list)
			mm_nrducell_nrducellid_list.extend(master_nrducell_nrducellid_list)
			mm_nrducell_nrducellname_list.extend(master_nrducell_nrducellname_list)
			mm_nrducell_physicalcellid_list.extend(master_nrducell_physicalcellid_list)
			mm_nrducell_slotassignment_list.extend(master_nrducell_slotassignment_list)
			mm_nrducell_subcarrierspacing_list.extend(master_nrducell_subcarrierspacing_list)
			mm_nrducell_trackingareaid_list.extend(master_nrducell_trackingareaid_list)
			mm_nrducell_ulbandwidth_list.extend(master_nrducell_ulbandwidth_list)
			mm_nrducell_ulnarfcn_list.extend(master_nrducell_ulnarfcn_list)
			mm_nrducellalgoswitch_spectrumcloudswitch_list.extend(master_nrducellalgoswitch_spectrumcloudswitch_list)
			mm_nrducellop_operatorid_list.extend(master_nrducellop_operatorid_list)

	for i in range(0, len(mm_nrcell_cellname_list)):
		mm_datetime_list.append(date_time)
		mm_neversion_list.append(neversion)

	df = pd.DataFrame(
		columns=["gnodebfunction_gnbid", "gnodebfunction_gnodebfunctionname", "nrcell_cellactivestate",
		         "nrcell_cellname", "nrcell_nrcellid", "nrducell_cellid", "nrducell_dlbandwidth", "nrducell_dlnarfcn",
		         "nrducell_duplexmode", "nrducell_frequencyband", "nrducell_lampsitecellflag",
		         "nrducell_nrducellactivestate", "nrducell_nrducellid", "nrducell_nrducellname",
		         "nrducell_physicalcellid", "nrducell_slotassignment", "nrducell_subcarrierspacing",
		         "nrducell_trackingareaid", "nrducell_ulbandwidth", "nrducell_ulnarfcn",
		         "nrducellalgoswitch_spectrumcloudswitch", "nrducellop_operatorid", "datetime", "neversion"])

	df["gnodebfunction_gnbid"] = mm_gnodebfunction_gnbid_list
	df["gnodebfunction_gnodebfunctionname"] = mm_gnodebfunction_gnodebfunctionname_list
	df["nrcell_cellactivestate"] = mm_nrcell_cellactivestate_list
	df["nrcell_cellname"] = mm_nrcell_cellname_list
	df["nrcell_nrcellid"] = mm_nrcell_nrcellid_list
	df["nrducell_cellid"] = mm_nrducell_cellid_list
	df["nrducell_dlbandwidth"] = mm_nrducell_dlbandwidth_list
	df["nrducell_dlnarfcn"] = mm_nrducell_dlnarfcn_list
	df["nrducell_duplexmode"] = mm_nrducell_duplexmode_list
	df["nrducell_frequencyband"] = mm_nrducell_frequencyband_list
	df["nrducell_lampsitecellflag"] = mm_nrducell_lampsitecellflag_list
	df["nrducell_nrducellactivestate"] = mm_nrducell_nrducellactivestate_list
	df["nrducell_nrducellid"] = mm_nrducell_nrducellid_list
	df["nrducell_nrducellname"] = mm_nrducell_nrducellname_list
	df["nrducell_physicalcellid"] = mm_nrducell_physicalcellid_list
	df["nrducell_slotassignment"] = mm_nrducell_slotassignment_list
	df["nrducell_subcarrierspacing"] = mm_nrducell_subcarrierspacing_list
	df["nrducell_trackingareaid"] = mm_nrducell_trackingareaid_list
	df["nrducell_ulbandwidth"] = mm_nrducell_ulbandwidth_list
	df["nrducell_ulnarfcn"] = mm_nrducell_ulnarfcn_list
	df["nrducellalgoswitch_spectrumcloudswitch"] = mm_nrducellalgoswitch_spectrumcloudswitch_list
	df["nrducellop_operatorid"] = mm_nrducellop_operatorid_list
	df["datetime"] = mm_datetime_list
	df["neversion"] = mm_neversion_list

	df.to_csv("VFES_5G_CM_files/" + new_xml_file.rsplit(".")[-2] + ".csv", index=False)

	print("CSV file saved successfully!")

print('It took {0:0.1f} seconds'.format(time.time() - begin_time))
