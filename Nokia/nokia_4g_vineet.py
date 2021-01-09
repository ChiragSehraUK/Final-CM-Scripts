import glob
import csv
from lxml import etree
import re
import os
import pandas as pd

for xml_file in glob.glob("/home/chiragsehra/Downloads/BO16_20200525.xml"):
	print(xml_file)
	context = etree.iterparse(xml_file, tag="{raml20.xsd}managedObject")

	lnbts_list = []
	lncel_list = []
	mrbts_list = []

	for event, elem in context:

		if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "LNBTS":
			lnbts_dict = {
				"lnbts_siteId": None,
				"lnbts_mcc": None,
				"lnbts_mnc": None,
				"lnbts_name": None,
				"lnbts_btsType": None,
				"lnbts_enbName": None,
				"lnbts_operationalState": None,
				"lnbts_mrbts_id": None,
				"lnbts_id": None,
				"join_reference_2": None,
				"join_reference_1": None,
				"lnbts_managedObjectId": None
			}
			dist_name = elem.attrib["distName"]
			lnbts_dict["lnbts_mrbts_id"] = re.search("MRBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
			lnbts_dict["lnbts_id"] = re.search("LNBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
			lnbts_dict["join_reference_2"] = dist_name
			lnbts_dict["join_reference_1"] = "/".join(dist_name.split("/")[0:2])
			lnbts_dict["lnbts_managedObjectId"] = elem.attrib["id"]

			for e in elem:
				if e.attrib["name"] == "siteId":
					lnbts_dict["lnbts_siteId"] = e.text
				if e.attrib["name"] == "mcc":
					lnbts_dict["lnbts_mcc"] = e.text
				if e.attrib["name"] == "mnc":
					lnbts_dict["lnbts_mnc"] = e.text
				if e.attrib["name"] == "name":
					lnbts_dict["lnbts_name"] = e.text
				if e.attrib["name"] == "btsType":
					lnbts_dict["lnbts_btsType"] = e.text
				if e.attrib["name"] == "enbName":
					lnbts_dict["lnbts_enbName"] = e.text
				if e.attrib["name"] == "operationalState":
					lnbts_dict["lnbts_operationalState"] = e.text

			lnbts_list.append(lnbts_dict)

		if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "LNCEL":
			lncel_dict = {
				"lncel_mrbts_id": None,
				"lncel_lnbts_id": None,
				"lncel_id": None,
				"lncel_dist_name": None,
				"lncel_managedObjectId": None,
				"join_reference_2": None,
				"lncel_siteId": None,
				"lncel_mcc": None,
				"lncel_mnc": None,
				"lncel_name": None,
				"lncel_cellBarred": None,
				"lncel_cellName": None,
				"lncel_cellTechnology": None,
				"lncel_earfcn": None,
				"lncel_earfcnDL": None,
				"lncel_earfcnUL": None,
				"lncel_energySavingState": None,
				"lncel_eutraCelId": None,
				"lncel_lcrId": None,
				"lncel_phyCellId": None
			}
			dist_name = elem.attrib["distName"]
			lncel_dict["lncel_mrbts_id"] = re.search("MRBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
			lncel_dict["lncel_lnbts_id"] = re.search("LNBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
			lncel_dict["lncel_id"] = re.search("LNCEL-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
			lncel_dict["lncel_dist_name"] = dist_name
			lncel_dict["join_reference_2"] = "/".join(dist_name.split("/")[0:3])
			lncel_dict["lncel_managedObjectId"] = elem.attrib["id"]

			for e in elem:
				if e.attrib["name"] == "siteId":
					lncel_dict["lncel_siteId"] = e.text
				if e.attrib["name"] == "mcc":
					lncel_dict["lncel_mcc"] = e.text
				if e.attrib["name"] == "mnc":
					lncel_dict["lncel_mnc"] = e.text
				if e.attrib["name"] == "name":
					lncel_dict["lncel_name"] = e.text
				if e.attrib["name"] == "cellBarred":
					lncel_dict["lncel_cellBarred"] = e.text
				if e.attrib["name"] == "cellName":
					lncel_dict["lncel_cellName"] = e.text
				if e.attrib["name"] == "cellTechnology":
					lncel_dict["lncel_cellTechnology"] = e.text
				if e.attrib["name"] == "earfcn":
					lncel_dict["lncel_earfcn"] = e.text
				if e.attrib["name"] == "earfcnDL":
					lncel_dict["lncel_earfcnDL"] = e.text
				if e.attrib["name"] == "earfcnUL":
					lncel_dict["lncel_earfcnUL"] = e.text
				if e.attrib["name"] == "energySavingState":
					lncel_dict["lncel_energySavingState"] = e.text
				if e.attrib["name"] == "eutraCelId":
					lncel_dict["lncel_eutraCelId"] = e.text
				if e.attrib["name"] == "lcrId":
					lncel_dict["lncel_lcrId"] = e.text
				if e.attrib["name"] == "phyCellId":
					lncel_dict["lncel_phyCellId"] = e.text

			lncel_list.append(lncel_dict)

		if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "MRBTS" and len(
				elem.attrib["distName"].split("/")) == 2:
			mrbts_dict = {
				"mrbts_id": None,
				"join_reference_1": None,
				"managedObjectId": None,
				"mrbts_siteId": None,
				"mrbts_name": None,
				"mrbts_altitude": None,
				"mrbts_latitude": None,
				"mrbts_longitude": None,
				"mrbts_btsname": None,
				"mrbts_netype": None}
			dist_name = elem.attrib["distName"]
			mrbts_dict["mrbts_id"] = re.search("MRBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
			mrbts_dict["join_reference_1"] = dist_name
			mrbts_dict["managedObjectId"] = elem.attrib["id"]

			for e in elem:
				if e.attrib["name"] == "siteId":
					mrbts_dict["mrbts_siteId"] = e.text
				if e.attrib["name"] == "name":
					mrbts_dict["mrbts_name"] = e.text
				if e.attrib["name"] == "altitude":
					mrbts_dict["mrbts_altitude"] = e.text
				if e.attrib["name"] == "latitude":
					mrbts_dict["mrbts_latitude"] = e.text
				if e.attrib["name"] == "longitude":
					mrbts_dict["mrbts_longitude"] = e.text
				if e.attrib["name"] == "btsName":
					mrbts_dict["mrbts_btsname"] = e.text
				if e.attrib["name"] == "neType":
					mrbts_dict["mrbts_netype"] = e.text
			mrbts_list.append(mrbts_dict)
		elem.clear()

	if not os.path.exists("4G_Nokia_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"):
		os.makedirs("4G_Nokia_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/")

	filenames = {
		"LNCEL.csv": lncel_list, "LNBTS.csv": lnbts_list, "MRBTS.csv": mrbts_list,
	}

	for key, value in filenames.items():
		with open("4G_Nokia_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + key, "w") as write_file:
			headers = value[0].keys()
			csv_writer = csv.DictWriter(write_file, fieldnames=headers)
			csv_writer.writeheader()
			csv_writer.writerows(value)

	lnbts_file = pd.read_csv("4G_Nokia_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "LNBTS.csv")
	lncel_file = pd.read_csv("4G_Nokia_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "LNCEL.csv")
	mrbts_file = pd.read_csv("4G_Nokia_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "MRBTS.csv")

	df = pd.merge(mrbts_file, lnbts_file, on="join_reference_1")
	df = pd.merge(df, lncel_file, on="join_reference_2")

	df.to_csv("4G_Nokia_CM_files/" + "Flattened_" + xml_file.rsplit("/")[-1].rsplit(".")[0] +
	          ".csv", index=False)
