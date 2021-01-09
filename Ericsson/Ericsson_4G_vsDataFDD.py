import pandas as pd
import csv
import glob
import os
import re
import argparse
import shutil
import subprocess

parser = argparse.ArgumentParser(description="Arguments for 4G Ericsson CM files")
parser.add_argument('COUNTRY', metavar='COUNTRY', type=str, help='country of CM files: VFES')
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

for xml_file in glob.glob(sourcePath + "/*401_4G*"):
	print(xml_file)

	# vsDataFDD parameters list
	d = dict()
	masterlist_eutrancellid = []
	masterlist_administrativestate = []
	masterlist_userlabel = []
	masterlist_earfcndl = []
	masterlist_earfcnul = []
	masterlist_dlchannel = []
	masterlist_ulchannel = []
	masterlist_freqband = []
	masterlist_cellid = []
	masterlist_layerid = []
	masterlist_groupid = []
	masterlist_subcellid = []
	masterlist_mcc = []
	masterlist_mnc = []
	masterlist_tac = []
	masterlist_reservedby = []
	masterlist_reservedby_join = []
	masterlist_xmlfilename = []

	# ENBID parameters list
	nd = dict()
	masterlist_enbid = []
	masterlist_sctpRef = []
	masterlist_sctpRef_join = []

	# creating temporary folder for results
	if not os.path.exists(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"):
		os.makedirs(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/")

	# dividing the files into multiple parts
	file_division = subprocess.run(
		["split", "-l 500", xml_file, tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"])

	files_to_process = sorted(glob.glob(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/*"))

	for small_file in files_to_process:
		with open(small_file, "r") as f:
			s = f.read().replace("\n", "")
			vsdataeutrancellfdd = re.findall("<es:vsDataEUtranCellFDD>(.*?)</es:vsDataEUtranCellFDD>", s)

			for i in vsdataeutrancellfdd:
				eutrancellid = re.search("<es:EUtranCellFDDId>(.*?)</es:EUtranCellFDDId>", i, re.IGNORECASE)
				if eutrancellid is not None:
					masterlist_eutrancellid.append(eutrancellid.group().split(">")[1].split("<")[0])
				else:
					masterlist_eutrancellid.append(None)

				userlabel = re.search("<es:userLabel>(.*?)</es:userLabel>", i, re.IGNORECASE)
				if userlabel is not None:
					masterlist_userlabel.append(userlabel.group().split(">")[1].split("<")[0])
				else:
					masterlist_userlabel.append(None)

				earfcndl = re.search("<es:earfcndl>(.*?)</es:earfcndl>", i, re.IGNORECASE)
				if earfcndl is not None:
					masterlist_earfcndl.append(earfcndl.group().split(">")[1].split("<")[0])
				else:
					masterlist_earfcndl.append(None)

				earfcnul = re.search("<es:earfcnul>(.*?)</es:earfcnul>", i, re.IGNORECASE)
				if earfcnul is not None:
					masterlist_earfcnul.append(earfcnul.group().split(">")[1].split("<")[0])
				else:
					masterlist_earfcnul.append(None)

				administrativestate = re.search("<es:administrativeState>(.*?)</es:administrativeState>", i,
				                                re.IGNORECASE)
				if earfcnul is not None:
					masterlist_administrativestate.append(administrativestate.group().split(">")[1].split("<")[0])
				else:
					masterlist_administrativestate.append(None)

				dlchannel = re.search("<es:dlChannelBandwidth>(.*?)</es:dlChannelBandwidth>", i, re.IGNORECASE)
				if dlchannel is not None:
					masterlist_dlchannel.append(dlchannel.group().split(">")[1].split("<")[0])
				else:
					masterlist_dlchannel.append(None)

				ulchannel = re.search("<es:ulChannelBandwidth>(.*?)</es:ulChannelBandwidth>", i, re.IGNORECASE)
				if ulchannel is not None:
					masterlist_ulchannel.append(ulchannel.group().split(">")[1].split("<")[0])
				else:
					masterlist_ulchannel.append(None)

				freqband = re.search("<es:freqBand>(.*?)</es:freqBand>", i, re.IGNORECASE)
				if freqband is not None:
					masterlist_freqband.append(freqband.group().split(">")[1].split("<")[0])
				else:
					masterlist_freqband.append(None)

				cellid = re.search("<es:cellId>(.*?)</es:cellId>", i, re.IGNORECASE)
				if cellid is not None:
					masterlist_cellid.append(cellid.group().split(">")[1].split("<")[0])
				else:
					masterlist_cellid.append(None)

				layerid = re.search("<es:physicalLayerCellId>(.*?)</es:physicalLayerCellId>", i, re.IGNORECASE)
				if layerid is not None:
					masterlist_layerid.append(layerid.group().split(">")[1].split("<")[0])
				else:
					masterlist_layerid.append(None)

				groupid = re.search("<es:physicalLayerCellIdGroup>(.*?)</es:physicalLayerCellIdGroup>", i,
				                    re.IGNORECASE)
				if groupid is not None:
					masterlist_groupid.append(groupid.group().split(">")[1].split("<")[0])
				else:
					masterlist_groupid.append(None)

				subcellid = re.search("<es:physicalLayerSubCellId>(.*?)</es:physicalLayerSubCellId>", i, re.IGNORECASE)
				if subcellid is not None:
					masterlist_subcellid.append(subcellid.group().split(">")[1].split("<")[0])
				else:
					masterlist_subcellid.append(None)

				mcc = re.search("<es:mcc>(.*?)</es:mcc>", i, re.IGNORECASE)
				masterlist_mcc.append(mcc.group().split(">")[1].split("<")[0])

				mnc = re.search("<es:mnc>(.*?)</es:mnc>", i, re.IGNORECASE)
				masterlist_mnc.append(mnc.group().split(">")[1].split("<")[0])

				tac = re.search("<es:tac>(.*?)</es:tac>", i, re.IGNORECASE)
				if tac is not None:
					masterlist_tac.append(tac.group().split(">")[1].split("<")[0])
				else:
					masterlist_tac.append(None)

				reservedbytag = re.search("<es:reservedBy>(.*?)</es:reservedBy>", i, re.IGNORECASE)
				if reservedbytag is not None:
					reservedby = reservedbytag.group().split(">")[1].split("<")[0]
					masterlist_reservedby.append(reservedby if len(reservedby) else None)

					reservedby_values = reservedby.split(",")
					reservedby_str = ",".join(reservedby_values[0:3])
					masterlist_reservedby_join.append(reservedby_str if len(reservedby_str) else None)
				else:
					masterlist_reservedby.append(None)
					masterlist_reservedby_join.append(None)

		with open(xml_file, "r") as fr:
			s = fr.read()
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

		with open(files_to_process[-1], "r") as read_file:
			value = read_file.read().replace("\n", "")
			datetime = re.findall("<fileFooter(.*?)/>", value)[0].split("=")[-1].strip('"')

	d["EUtranCellFDDId"] = masterlist_eutrancellid
	d["Userlabel"] = masterlist_userlabel
	d["earfcndl"] = masterlist_earfcndl
	d["earfcnul"] = masterlist_earfcnul
	d["administrativestate"] = masterlist_administrativestate
	d["dlChannelBandwidth"] = masterlist_dlchannel
	d["ulChannelBandwidth"] = masterlist_ulchannel
	d["freqBand"] = masterlist_freqband
	d["CellID"] = masterlist_cellid
	d["PhysicalLayerCellId"] = masterlist_layerid
	d["PhysicalLayerCellIdGroup"] = masterlist_groupid
	d["PhysicalLayerSubCellId"] = masterlist_subcellid
	d["MCC"] = masterlist_mcc
	d["MNC"] = masterlist_mnc
	d["TAC"] = masterlist_tac
	d["ReservedBy"] = masterlist_reservedby
	d["join_reference"] = masterlist_reservedby_join

	nd["eNBId"] = masterlist_enbid
	nd["sctpRef"] = masterlist_sctpRef
	nd["join_reference"] = masterlist_sctpRef_join
	nd["datetime"] = [datetime for i in masterlist_enbid]

	df = pd.DataFrame.from_dict(d)
	dataf = pd.DataFrame.from_dict(nd)

	df.to_csv(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "vsDataFDD_" +
	          xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", index=False)

	dataf.to_csv(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "vsENBID_" +
	             xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", index=False)

	# df1 = pd.read_csv(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "vsDataFDD_" +
	#                   xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", index=False)
	# df2 = pd.read_csv(tempPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "vsENBID_" +
	#                   xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", index=False)

	dataframe = pd.merge(df, dataf, on="join_reference")
	dataframe.to_csv(destinationPath + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" +
	                  xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", index=False)
