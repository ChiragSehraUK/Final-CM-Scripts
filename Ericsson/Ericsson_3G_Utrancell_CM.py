import pandas as pd
from lxml import etree
import csv
import glob
import os
import argparse
import shutil

parser = argparse.ArgumentParser(description="Arguments for 3G Ericsson CM files")
parser.add_argument('COUNTRY', metavar='COUNTRY', type=str, help='country of CM files: VFRO')
parser.add_argument('TECH', metavar='TECH', type=str, help='technology of CM files')
args = parser.parse_args()
country = args.COUNTRY
tech = args.TECH
vendor = 'ericsson'

pathConfig_file = pd.read_csv("/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/pathConfig_ericsson.csv")

for i in pathConfig_file.index:
	if (pathConfig_file['country'][i].lower() == country.lower()) and (
			pathConfig_file['tech'][i].lower() == tech.lower()):
		sourcePath = pathConfig_file['sourcePath'][i]

tempPath = "/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/" + country + "/" + vendor + "/" + tech + "/"
destinationPath = "/home/valiance/Desktop/Cardinality/CM-Parsers/CM-Scripts-VM/" + country + "/" + vendor + "/" + tech \
                  + "/"

for xml_file in glob.glob(sourcePath + "/UTRAN*.xml"):
	print(xml_file)
	l, rncList = list(), list()
	context = etree.iterparse(xml_file, tag="{utranNrm.xsd}UtranCell")
	for event, elem in context:
		d = {
			"utrancell_id": None,
			"local_cell_id": None,
			"uarfcnUl": None,
			"uarfcnDl": None,
			"primary_scrambling_code": None,
			"primary_cpich_power": None,
			"maximum_transmission_power": None,
			"cid": None,
			"utrancell_userlabel": None,
			"lac": None,
			"rac": None,
			"administrative_state": None,
			"availability_state": None,
			"iub_link_ref": None,
			"join_reference": None,
			"iub_link_userlabel": None,
			"iub_link_id": None,
			"operational_state": None,
			"tps_power_lock_state": None
		}
		count = 0
		d["utrancell_id"] = elem.attrib["id"]
		for attribute in elem:
			if attribute.tag == "{utranNrm.xsd}attributes":
				for un in attribute:
					if un.tag == "{utranNrm.xsd}localCellId":
						d["local_cell_id"] = un.text
					if un.tag == "{utranNrm.xsd}uarfcnUl":
						d["uarfcnUl"] = un.text
					if un.tag == "{utranNrm.xsd}uarfcnDl":
						d["uarfcnDl"] = un.text
					if un.tag == "{utranNrm.xsd}primaryScramblingCode":
						d["primary_scrambling_code"] = un.text
					if un.tag == "{utranNrm.xsd}primaryCpichPower":
						d["primary_cpich_power"] = un.text
					if un.tag == "{utranNrm.xsd}maximumTransmissionPower":
						d["maximum_transmission_power"] = un.text
					if un.tag == "{utranNrm.xsd}cId":
						d["cid"] = un.text
					if un.tag == "{utranNrm.xsd}userLabel":
						d["utrancell_userlabel"] = un.text
					if un.tag == "{utranNrm.xsd}lac":
						d["lac"] = un.text
					if un.tag == "{utranNrm.xsd}rac":
						d["rac"] = un.text
			if attribute.tag == "{genericNrm.xsd}VsDataContainer" and count == 0:
				for datacontainer in attribute:
					for temp in datacontainer:
						for i in temp:
							if i.tag == "{EricssonSpecificAttributes.17.09.xsd}administrativeState":
								d["administrative_state"] = i.text
							if i.tag == "{EricssonSpecificAttributes.17.09.xsd}iubLinkRef":
								d["iub_link_ref"] = i.text
								d["join_reference"] = ",".join(i.text.split(",")[:5])
								d["iub_link_userlabel"] = i.text.split(",")[-1].split("=")[-1]
								d["iub_link_id"] = i.text.split(",")[-1].split("=")[-1]
							if i.tag == "{EricssonSpecificAttributes.17.09.xsd}operationalState":
								d["operational_state"] = i.text
							if i.tag == "{EricssonSpecificAttributes.17.09.xsd}tpsPowerLockState":
								d["tps_power_lock_state"] = i.text
					# d["country"] = "RO"
					# d["vendor"] = "Ericsson"
					# d["version"] = "32.615 V4.5"
					l.append(d)
					count = 1
		elem.clear()

	if not os.path.exists(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"):
		os.makedirs(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/")

	with open(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "Utrancell_" +
	          xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", "w") as write_file:
		headers = l[0].keys()
		csv_writer = csv.DictWriter(write_file, fieldnames=headers)
		csv_writer.writeheader()
		csv_writer.writerows(l)

	rncContext = etree.iterparse(xml_file, tag="{utranNrm.xsd}RncFunction")
	for event, elem in rncContext:
		d = dict()
		count = 0
		c = 0
		for attribute in elem:
			if attribute.tag == "{utranNrm.xsd}attributes":
				for un in attribute:
					if un.tag == "{utranNrm.xsd}userLabel" and c == 0:
						d["rnc_userlabel"] = un.text
						c = 1
					if un.tag == "{utranNrm.xsd}rncId":
						d["rnc_id"] = un.text
			if attribute.tag == "{genericNrm.xsd}VsDataContainer" and count == 0:
				for datacontainer in attribute:
					for temp in datacontainer:
						for i in temp:
							if i.tag == "{EricssonSpecificAttributes.17.09.xsd}primaryCnOperatorRef":
								d["cn_operator"] = i.text
								d["join_reference"] = ",".join(i.text.split(",")[:5])
							if i.tag == "{EricssonSpecificAttributes.17.09.xsd}rncType":
								d["rnc_type"] = i.text
					rncList.append(d)
					count = 1
		elem.clear()

	data = etree.iterparse(xml_file, tag="{configData.xsd}fileFooter")
	datetime = [y.attrib["dateTime"] for x, y in data][0]

	for i in rncList:
		i["datetime"] = datetime

	with open(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "RncFunction_" +
	          xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", "w") as write_file:
		headers = rncList[0].keys()
		csv_writer = csv.DictWriter(write_file, fieldnames=headers)
		csv_writer.writeheader()
		csv_writer.writerows(rncList)

	df1 = pd.read_csv(
		tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "Utrancell_" + xml_file.rsplit("/")[-1].rsplit(".")[
			0] + ".csv")
	df2 = pd.read_csv(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "RncFunction_" +
	                  xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv")

	df = pd.merge(df1, df2, on="join_reference")
	df.to_csv(destinationPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", index=False)

	# deleting the folder of files created
	print("Deleting the temporary created folders...")
	dir_path = tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0]
	shutil.rmtree(dir_path)
