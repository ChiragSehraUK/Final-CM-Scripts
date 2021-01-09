import pandas as pd
import re
import csv
import glob
import os
import argparse
import shutil
import subprocess

parser = argparse.ArgumentParser(description="Arguments for 3G Ericsson CM files")
parser.add_argument('COUNTRY', metavar='COUNTRY', type=str, help='country of CM files either VFES or VFPT')
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

for xml_file in glob.glob(sourcePath + "/*.xml"):
	print(xml_file)
	# initialization parameters for vsDataUtranCell extraction
	d = dict()
	masterlist_utrancell_id = []
	masterlist_local_cell_id = []
	masterlist_uarfcnUl = []
	masterlist_uarfcnDl = []
	masterlist_primary_scrambling_code = []
	masterlist_primary_cpich_power = []
	masterlist_maximum_transmission_power = []
	masterlist_cid = []
	masterlist_utrancell_userlabel = []
	masterlist_lac = []
	masterlist_rac = []
	masterlist_administrative_state = []
	masterlist_availability_status = []
	masterlist_iub_link_ref = []
	masterlist_join_reference = []
	masterlist_iub_link_userlabel = []
	masterlist_iub_link_id = []
	masterlist_operational_state = []
	masterlist_tps_power_lock_state = []

	# initialization parameters for vcDataRncFunction extraction
	nd = dict()
	masterlist_rncType = []
	masterlist_rnc_userlabel = []
	masterlist_rncid = []
	masterlist_cn_operator = []
	masterlist_rnc_join_reference = []
	masterlist_datetime = []

	# dividing the file into multiple parts
	if not os.path.exists(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"):
		os.makedirs(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/")

	file_division = subprocess.run(
		["split", "-l 500", xml_file, tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"])

	files_to_process = sorted(glob.glob(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/*"))

	for small_file in files_to_process:
		with open(small_file, "r") as f:
			s = f.read().replace("\n", "")
			vsdataeutrancellfdd = re.findall("<es:vsDataUtranCell>(.*?)</es:vsDataUtranCell>", s, re.IGNORECASE)

			for i in vsdataeutrancellfdd:
				utrancellid = re.search("<es:UtranCellId>(.*?)</es:UtranCellId>", i, re.IGNORECASE)
				if utrancellid is not None:
					masterlist_utrancell_id.append(utrancellid.group().split(">")[1].split("<")[0])
				else:
					masterlist_utrancell_id.append(None)

				localCellId = re.search("<es:localCellId>(.*?)</es:localCellId>", i, re.IGNORECASE)
				if localCellId is not None:
					masterlist_local_cell_id.append(localCellId.group().split(">")[1].split("<")[0])
				else:
					masterlist_local_cell_id.append(None)

				uarfcnDl = re.search("<es:uarfcnDl>(.*?)</es:uarfcnDl>", i, re.IGNORECASE)
				if uarfcnDl is not None:
					masterlist_uarfcnDl.append(uarfcnDl.group().split(">")[1].split("<")[0])
				else:
					masterlist_uarfcnDl.append(None)

				uarfcnUl = re.search("<es:uarfcnUl>(.*?)</es:uarfcnUl>", i, re.IGNORECASE)
				if uarfcnUl is not None:
					masterlist_uarfcnUl.append(uarfcnUl.group().split(">")[1].split("<")[0])
				else:
					masterlist_uarfcnUl.append(None)

				primaryScramblingCode = re.search("<es:primaryScramblingCode>(.*?)</es:primaryScramblingCode>", i,
				                                  re.IGNORECASE)
				if primaryScramblingCode is not None:
					masterlist_primary_scrambling_code.append(primaryScramblingCode.group().split(">")[1].split("<")[0])
				else:
					masterlist_primary_scrambling_code.append(None)

				primaryCpichPower = re.search("<es:primaryCpichPower>(.*?)</es:primaryCpichPower>", i, re.IGNORECASE)
				if primaryCpichPower is not None:
					masterlist_primary_cpich_power.append(primaryCpichPower.group().split(">")[1].split("<")[0])
				else:
					masterlist_primary_cpich_power.append(None)

				maximumTransmissionPower = re.search("<es:maximumTransmissionPower>(.*?)</es:maximumTransmissionPower>",
				                                     i, re.IGNORECASE)
				if maximumTransmissionPower is not None:
					masterlist_maximum_transmission_power.append(
						maximumTransmissionPower.group().split(">")[1].split("<")[0])
				else:
					masterlist_maximum_transmission_power.append(None)

				cId = re.search("<es:cId>(.*?)</es:cId>", i, re.IGNORECASE)
				if cId is not None:
					masterlist_cid.append(cId.group().split(">")[1].split("<")[0])
				else:
					masterlist_cid.append(None)

				userLabel = re.search("<es:userLabel>(.*?)</es:userLabel>", i, re.IGNORECASE)
				if userLabel is not None:
					masterlist_utrancell_userlabel.append(userLabel.group().split(">")[1].split("<")[0])
				else:
					masterlist_utrancell_userlabel.append(None)

				lac = re.search("<es:lac>(.*?)</es:lac>", i, re.IGNORECASE)
				if lac is not None:
					masterlist_lac.append(lac.group().split(">")[1].split("<")[0])
				else:
					masterlist_lac.append(None)

				rac = re.search("<es:rac>(.*?)</es:rac>", i, re.IGNORECASE)
				if rac is not None:
					masterlist_rac.append(rac.group().split(">")[1].split("<")[0])
				else:
					masterlist_rac.append(None)

				tpsPowerLockState = re.search("<es:tpsPowerLockState>(.*?)</es:tpsPowerLockState>", i, re.IGNORECASE)
				if tpsPowerLockState is not None:
					masterlist_tps_power_lock_state.append(tpsPowerLockState.group().split(">")[1].split("<")[0])
				else:
					masterlist_tps_power_lock_state.append(None)

				availabilityStatus = re.search("<es:availabilityStatus>(.*?)</es:availabilityStatus>", i, re.IGNORECASE)
				if availabilityStatus is not None:
					masterlist_availability_status.append(availabilityStatus.group().split(">")[1].split("<")[0])
				else:
					masterlist_availability_status.append(None)

				administrativeState = re.search("<es:administrativeState>(.*?)</es:administrativeState>", i,
				                                re.IGNORECASE)
				if administrativeState is not None:
					masterlist_administrative_state.append(administrativeState.group().split(">")[1].split("<")[0])
				else:
					masterlist_administrative_state.append(None)

				operationalState = re.search("<es:operationalState>(.*?)</es:operationalState>", i, re.IGNORECASE)
				if operationalState is not None:
					masterlist_operational_state.append(operationalState.group().split(">")[1].split("<")[0])
				else:
					masterlist_operational_state.append(None)

				iublink_ref = re.search("<es:iubLinkRef>(.*?)</es:iubLinkRef>", i, re.IGNORECASE)
				values = iublink_ref.group().split(">")[1].split("<")[0]
				masterlist_iub_link_ref.append(values if len(values) else None)

				iublink_values = values.split(",")
				join_reference = ",".join(iublink_values[0:5])
				iublink_userlabel = iublink_values[-1].split("=")[-1]
				iublink_id = iublink_values[-1].split("=")[-1]
				masterlist_iub_link_userlabel.append(iublink_userlabel)
				masterlist_iub_link_id.append(iublink_id)
				masterlist_join_reference.append(join_reference if len(join_reference) else None)

		# reading the file again for extraction of vsDataRncFunction block parameters
		with open(small_file, "r") as f:
			sd = f.read()
			# vsDataRncFunction = re.findall("<es:vsDataRncFunction>(?:.*\r?\n?)*?</es:vsDataRncFunction>", s, re.IGNORECASE)
			vsDataRncFunction = re.findall("<es:vsDataRncFunction>(.*?)</es:vsDataRncFunction>", sd, re.IGNORECASE)

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
				masterlist_rnc_join_reference.append(join_reference)

		with open(files_to_process[-1], "r") as read_file:
			value = read_file.read().replace("\n", "")
			datetime = re.findall("<fileFooter(.*?)/>", value)[0].split("=")[-1].strip('"')

	d["utrancell_id"] = masterlist_utrancell_id
	d["local_cell_id"] = masterlist_local_cell_id
	d["uarfcnUl"] = masterlist_uarfcnUl
	d["uarfcnDl"] = masterlist_uarfcnDl
	d["primary_scrambling_code"] = masterlist_primary_scrambling_code
	d["primary_cpich_power"] = masterlist_primary_cpich_power
	d["maximum_transmission_power"] = masterlist_maximum_transmission_power
	d["cid"] = masterlist_cid
	d["utrancell_userlabel"] = masterlist_utrancell_userlabel
	d["lac"] = masterlist_lac
	d["rac"] = masterlist_rac
	d["administrative_state"] = masterlist_administrative_state
	d["availability_status"] = masterlist_availability_status
	d["iub_link_ref"] = masterlist_iub_link_ref
	d["join_reference"] = masterlist_join_reference
	d["iub_link_userlabel"] = masterlist_iub_link_userlabel
	d["iub_link_id"] = masterlist_iub_link_id
	d["operational_state"] = masterlist_operational_state
	d["tps_power_lock_state"] = masterlist_tps_power_lock_state

	nd["rnc_userlabel"] = masterlist_rnc_userlabel
	nd["rnc_id"] = masterlist_rncid
	nd["cn_operator"] = masterlist_cn_operator
	nd["rnc_type"] = masterlist_rncType
	nd["join_reference"] = masterlist_rnc_join_reference
	nd["datetime"] = [datetime for i in masterlist_cn_operator]

	df = pd.DataFrame.from_dict(d)
	df.to_csv(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "vsDataUtranCell_" + xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", index=False)

	dataf = pd.DataFrame.from_dict(nd)
	dataf.to_csv(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "vsDataRncFunction_" + xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", index=False)

	final_dataframe = pd.merge(df, dataf, on="join_reference")
	final_dataframe.to_csv(destinationPath  + xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", index=False)

	# deleting the folder of files created
	print("Deleting the temporary created folders...")
	dir_path = tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0]
	shutil.rmtree(dir_path)
