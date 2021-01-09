import glob
import csv
from lxml import etree
import re
import os
import pandas as pd

for xml_file in glob.glob("/home/chiragsehra/Downloads/BO16_20200525.xml"):
	print(xml_file)
	context = etree.iterparse(xml_file, tag="{raml20.xsd}managedObject")

	nrbts_list = []
	nrcell_list = []
	mrbts_list = []

	for event, elem in context:
		if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "NRBTS":
			nrbts_dict = {
				"nrbts_mrbts_id": None,
				"nrbts_id": None,
				"nrbts_managedObjectId": None,
				"nrbts_siteId": None,
				"nrbts_mcc": None,
				"nrbts_mnc": None,
				"nrbts_name": None,
				"nrbts_operationalState": None,
				"nrbts_actCarrierAggregation": None,
				"nrbts_maxNumOfUsersPerCpCell": None,
				"nrbts_ratType": None,
				"join_reference_2": None,
				"join_reference_1": None
			}

			dist_name = elem.attrib["distName"]
			nrbts_dict["nrbts_mrbts_id"] = re.search("MRBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
			nrbts_dict["nrbts_id"] = re.search("NRBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
			nrbts_dict["join_reference_2"] = dist_name
			nrbts_dict["join_reference_1"] = "/".join(dist_name.split("/")[0:2])
			nrbts_dict["nrbts_managedObjectId"] = elem.attrib["id"]

			for e in elem:
				if e.attrib["name"] == "siteId":
					nrbts_dict["nrbts_siteId"] = e.text
				if e.attrib["name"] == "mcc":
					nrbts_dict["nrbts_mcc"] = e.text
				if e.attrib["name"] == "mnc":
					nrbts_dict["nrbts_mnc"] = e.text
				if e.attrib["name"] == "name":
					nrbts_dict["nrbts_name"] = e.text
				if e.attrib["name"] == "actCarrierAggregation":
					nrbts_dict["nrbts_actCarrierAggregation"] = e.text
				if e.attrib["name"] == "maxNumOfUsersPerCpCell":
					nrbts_dict["nrbts_maxNumOfUsersPerCpCell"] = e.text
				if e.attrib["name"] == "operationalState":
					nrbts_dict["nrbts_operationalState"] = e.text
				if e.attrib["name"] == "ratType":
					nrbts_dict["nrbts_ratType"] = e.text
			nrbts_list.append(nrbts_dict)

		if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "NRCELL":
			nrcell_dict = {
				"nrcell_mrbts_id": None,
				"nrcell_nrbts_id": None,
				"nrcell_id": None,
				"nrcell_dist_name": None,
				"nrcell_managedObjectId": None,
				"nrcell_siteId": None,
				"nrcell_mcc": None,
				"nrcell_mnc": None,
				"nrcell_name": None,
				"nrcell_administrativeState": None,
				"nrcell_availabilityStatus": None,
				"nrcell_operationalState": None,
				"nrcell_cellName": None,
				"nrcell_cellTechnology": None,
				"nrcell_physCellId": None,
				"nrcell_ssPbchBlockPower": None,
				"nrcell_pMax": None,
				"nrcell_ssbScs": None,
				"nrcell_chBw": None,
				"nrcell_lcrId": None,
				"nrcell_fiveGsTac": None,
				"nrcell_freqBandIndicatorNR": None,
				"nrcell_gscn": None,
				"nrcell_nrCellIdentity": None,
				"nrcell_nrarfcn": None,
				"nrcell_trackingAreaDN": None,
				"nrcell_nrCellType": None,
				"join_reference_2": None
			}
			dist_name = elem.attrib["distName"]
			nrcell_dict["nrcell_mrbts_id"] = re.search("MRBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
			nrcell_dict["nrcell_nrbts_id"] = re.search("NRBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
			nrcell_dict["nrcell_id"] = re.search("NRCELL-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
			nrcell_dict["nrcell_dist_name"] = dist_name
			nrcell_dict["join_reference_2"] = "/".join(dist_name.split("/")[0:3])
			nrcell_dict["nrcell_managedObjectId"] = elem.attrib["id"]

			for e in elem:
				if e.attrib["name"] == "siteId":
					nrcell_dict["nrcell_siteId"] = e.text
				if e.attrib["name"] == "mcc":
					nrcell_dict["nrcell_mcc"] = e.text
				if e.attrib["name"] == "mnc":
					nrcell_dict["nrcell_mnc"] = e.text
				if e.attrib["name"] == "name":
					nrcell_dict["nrcell_name"] = e.text
				if e.attrib["name"] == "administrativeState":
					nrcell_dict["nrcell_administrativeState"] = e.text
				if e.attrib["name"] == "cellName":
					nrcell_dict["nrcell_cellName"] = e.text
				if e.attrib["name"] == "cellTechnology":
					nrcell_dict["nrcell_cellTechnology"] = e.text
				if e.attrib["name"] == "physCellId":
					nrcell_dict["nrcell_physCellId"] = e.text
				if e.attrib["name"] == "ssPbchBlockPower":
					nrcell_dict["nrcell_ssPbchBlockPower"] = e.text
				if e.attrib["name"] == "pMax":
					nrcell_dict["nrcell_pMax"] = e.text
				if e.attrib["name"] == "ssbScs":
					nrcell_dict["nrcell_ssbScs"] = e.text
				if e.attrib["name"] == "chBw":
					nrcell_dict["nrcell_chBw"] = e.text
				if e.attrib["name"] == "lcrId":
					nrcell_dict["nrcell_lcrId"] = e.text
				if e.attrib["name"] == "fiveGsTac":
					nrcell_dict["nrcell_fiveGsTac"] = e.text
				if e.attrib["name"] == "freqBandIndicatorNR":
					nrcell_dict["nrcell_freqBandIndicatorNR"] = e.text
				if e.attrib["name"] == "gscn":
					nrcell_dict["nrcell_gscn"] = e.text
				if e.attrib["name"] == "nrCellIdentity":
					nrcell_dict["nrcell_nrCellIdentity"] = e.text
				if e.attrib["name"] == "nrarfcn":
					nrcell_dict["nrcell_nrarfcn"] = e.text
				if e.attrib["name"] == "operationalState":
					nrcell_dict["nrcell_operationalState"] = e.text
				if e.attrib["name"] == "trackingAreaDN":
					nrcell_dict["nrcell_trackingAreaDN"] = e.text
				if e.attrib["name"] == "availabilityStatus":
					nrcell_dict["nrcell_availabilityStatus"] = e.text
				if e.attrib["name"] == "nrCellType":
					nrcell_dict["nrcell_nrCellType"] = e.text
			nrcell_list.append(nrcell_dict)

		if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "MRBTS" and len(
				elem.attrib["distName"].split("/")) == 2:
			mrbts_dict = {
				"mrbts_id": None,
				"mrbts_managedObjectId": None,
				"join_reference_1": None
			}
			dist_name = elem.attrib["distName"]
			mrbts_dict["mrbts_id"] = re.search("MRBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
			mrbts_dict["join_reference_1"] = dist_name
			mrbts_dict["mrbts_managedObjectId"] = elem.attrib["id"]
			mrbts_list.append(mrbts_dict)

		elem.clear()

	if not os.path.exists("5G_Nokia_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"):
		os.makedirs("5G_Nokia_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/")

	filenames = {
		"NRCELL.csv": nrcell_list, "NRBTS.csv": nrbts_list, "MRBTS.csv": mrbts_list,
	}

	for key, value in filenames.items():
		with open("5G_Nokia_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + key, "w") as write_file:
			headers = value[0].keys()
			csv_writer = csv.DictWriter(write_file, fieldnames=headers)
			csv_writer.writeheader()
			csv_writer.writerows(value)

	nrbts_file = pd.read_csv("5G_Nokia_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "NRTBS.csv")
	nrcell_file = pd.read_csv("5G_Nokia_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "NRCELL.csv")
	mrbts_file = pd.read_csv("5G_Nokia_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "MRBTS.csv")

	df = pd.merge(mrbts_file, nrbts_file, on="join_reference_1")
	df = pd.merge(df, nrcell_file, on="join_reference_2")

	df.to_csv("5G_Nokia_CM_files/" + "Flattened_" + xml_file.rsplit("/")[-1].rsplit(".")[0] +
	          ".csv", index=False)
