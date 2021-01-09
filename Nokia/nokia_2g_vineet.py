import glob
import csv
from lxml import etree
import re
import os
import pandas as pd

for xml_file in glob.glob("C:/Users/Administrator/Downloads/VFIT-CM-27Sept/CM-20200927T153713Z-001/CM/*.xml"):
    print(xml_file)
    context = etree.iterparse(xml_file, tag="{raml20.xsd}managedObject")
    new_xml_file = xml_file.replace("C:/Users/Administrator/Downloads/VFIT-CM-27Sept/CM-20200927T153713Z-001/CM", "")
    new_xml_file = new_xml_file[1:]
    print(new_xml_file)
    bsc_list, bcf_list, bts_list, trx_list, mrbts_list = [], [], [], [], []

    for event, elem in context:
        if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "BSC":
            bsc_dict = {
                "bsc_id": None,
                "bsc_managedObjectId": None,
                "bsc_siteId": None,
                "bsc_name": None,
                "bsc_neSwRelease": None,
                "join_reference_1": None
            }
            dist_name = elem.attrib["distName"]
            bsc_dict["bsc_id"] = re.search("BSC-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            bsc_dict["join_reference_1"] = dist_name
            bsc_dict["bsc_managedObjectId"] = elem.attrib["id"]

            for e in elem:
                if e.attrib["name"] == "siteId":
                    bsc_dict["bsc_siteId"] = e.text
                if e.attrib["name"] == "name":
                    bsc_dict["bsc_name"] = e.text
                if e.attrib["name"] == "neSwRelease":
                    bsc_dict["bsc_neSwRelease"] = e.text
            bsc_list.append(bsc_dict)

        if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "BCF":
            bcf_dict = {
                "bcf_bsc_id": None,
                "bcf_id": None,
                "bcf_managedObjectId": None,
                "bcf_siteId": None,
                "bcf_name": None,
                "bcf_adminState": None,
                "bcf_bcfType": None,
                "bcf_address": None,
                "join_reference_2": None,
                "join_reference_1": None
            }
            dist_name = elem.attrib["distName"]
            bcf_dict["bcf_bsc_id"] = re.search("BSC-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            bcf_dict["bcf_id"] = re.search("BCF-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            bcf_dict["join_reference_2"] = dist_name
            bcf_dict["join_reference_1"] = "/".join(dist_name.split("/")[0:2])
            bcf_dict["bcf_managedObjectId"] = elem.attrib["id"]

            for e in elem:
                if e.attrib["name"] == "siteId":
                    bcf_dict["bcf_siteId"] = e.text
                if e.attrib["name"] == "name":
                    bcf_dict["bcf_name"] = e.text
                if e.attrib["name"] == "adminState":
                    bcf_dict["bcf_adminState"] = e.text
                if e.attrib["name"] == "bcfType":
                    bcf_dict["bcf_bcfType"] = e.text
                if e.attrib["name"] == "address":
                    bcf_dict["bcf_address"] = e.text
            bcf_list.append(bcf_dict)

        if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "BTS":
            bts_dict = {
                "bts_bsc_id": None,
                "bts_bcf_id": None,
                "bts_id": None,
                "bts_managedObjectId": None,
                "bts_siteId": None,
                "bts_cellId": None,
                "bts_sectorId": None,
                "bts_segmentId": None,
                "bts_locationAreaIdMCC": None,
                "bts_locationAreaIdMNC": None,
                "bts_name": None,
                "bts_nwName": None,
                "bts_frequencyBandInUse": None,
                "bts_adminState": None,
                "bts_bsIdentityCodeBCC": None,
                "bts_bsIdentityCodeNCC": None,
                "bts_locationAreaIdLAC": None,
                "bts_rac": None,
                "bts_segmentName": None,
                "bts_bcch_freq": None,
                "bts_CellType": None,
                "join_reference_2": None,
                "join_reference_3": None
            }
            dist_name = elem.attrib["distName"]
            bts_dict["bts_bsc_id"] = re.search("BSC-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            bts_dict["bts_bcf_id"] = re.search("BCF-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            bts_dict["bts_id"] = re.search("BTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            bts_dict["join_reference_2"] = "/".join(dist_name.split("/")[0:3])
            bts_dict["join_reference_3"] = dist_name
            bts_dict["bts_managedObjectId"] = elem.attrib["id"]

            for e in elem:
                if e.attrib["name"] == "siteId":
                    bts_dict["bts_siteId"] = e.text
                if e.attrib["name"] == "locationAreaIdMCC":
                    bts_dict["bts_locationAreaIdMCC"] = e.text
                if e.attrib["name"] == "locationAreaIdMNC":
                    bts_dict["bts_locationAreaIdMNC"] = e.text
                if e.attrib["name"] == "name":
                    bts_dict["bts_name"] = e.text
                if e.attrib["name"] == "frequencyBandInUse":
                    bts_dict["bts_frequencyBandInUse"] = e.text
                if e.attrib["name"] == "adminState":
                    bts_dict["bts_adminState"] = e.text
                if e.attrib["name"] == "bsIdentityCodeBCC":
                    bts_dict["bts_bsIdentityCodeBCC"] = e.text
                if e.attrib["name"] == "bsIdentityCodeNCC":
                    bts_dict["bts_bsIdentityCodeNCC"] = e.text
                if e.attrib["name"] == "cellId":
                    bts_dict["bts_cellId"] = e.text
                if e.attrib["name"] == "locationAreaIdLAC":
                    bts_dict["bts_locationAreaIdLAC"] = e.text
                if e.attrib["name"] == "nwName":
                    bts_dict["bts_nwName"] = e.text
                if e.attrib["name"] == "rac":
                    bts_dict["bts_rac"] = e.text
                if e.attrib["name"] == "sectorId":
                    bts_dict["bts_sectorId"] = e.text
                if e.attrib["name"] == "segmentId":
                    bts_dict["bts_segmentId"] = e.text
                if e.attrib["name"] == "segmentName":
                    bts_dict["bts_segmentName"] = e.text
                if e.attrib["name"] == "bcch_freq":
                    bts_dict["bts_bcch_freq"] = e.text
                if e.attrib["name"] == "CellType":
                    bts_dict["bts_CellType"] = e.text
            bts_list.append(bts_dict)

        if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "TRX":
            trx_dict = {
                "trx_bsc_id": None,
                "trx_bcf_id": None,
                "trx_bts_id": None,
                "trx_id": None,
                "trx_dist_name": None,
                "trx_managedObjectId": None,
                "trx_siteId": None,
                "trx_name": None,
                "trx_initialFrequency": None,
                "trx_adminState": None,
                "trx_channel0Type": None,
                "trx_channel1Type": None,
                "trx_channel2Type": None,
                "trx_channel3Type": None,
                "trx_channel4Type": None,
                "trx_channel5Type": None,
                "trx_channel6Type": None,
                "trx_channel7Type": None,
                "join_reference_3": None
            }
            dist_name = elem.attrib["distName"]
            trx_dict["trx_bsc_id"] = re.search("BSC-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            trx_dict["trx_bcf_id"] = re.search("BCF-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            trx_dict["trx_bts_id"] = re.search("BTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            trx_dict["trx_id"] = re.search("TRX-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            trx_dict["join_reference_3"] = "/".join(dist_name.split("/")[0:4])
            trx_dict["trx_dist_name"] = dist_name
            trx_dict["trx_managedObjectId"] = elem.attrib["id"]

            for e in elem:
                if e.attrib["name"] == "siteId":
                    trx_dict["trx_siteId"] = e.text
                if e.attrib["name"] == "name":
                    trx_dict["trx_name"] = e.text
                if e.attrib["name"] == "initialFrequency":
                    trx_dict["trx_initialFrequency"] = e.text
                if e.attrib["name"] == "adminState":
                    trx_dict["trx_adminState"] = e.text
                if e.attrib["name"] == "channel0Type":
                    trx_dict["trx_channel0Type"] = e.text
                if e.attrib["name"] == "channel1Type":
                    trx_dict["trx_channel1Type"] = e.text
                if e.attrib["name"] == "channel2Type":
                    trx_dict["trx_channel2Type"] = e.text
                if e.attrib["name"] == "channel3Type":
                    trx_dict["trx_channel3Type"] = e.text
                if e.attrib["name"] == "channel4Type":
                    trx_dict["trx_channel4Type"] = e.text
                if e.attrib["name"] == "channel5Type":
                    trx_dict["trx_channel5Type"] = e.text
                if e.attrib["name"] == "channel6Type":
                    trx_dict["trx_channel6Type"] = e.text
                if e.attrib["name"] == "channel7Type":
                    trx_dict["trx_channel7Type"] = e.text
            trx_list.append(trx_dict)

        if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "MRBTS" and "BSC" in elem.attrib[
            "distName"] and "BCF" in elem.attrib["distName"] and len(elem.attrib["distName"].split("/")) == 4:
            mrbts_dict = {
                "mrbts_bsc_id": None,
                "mrbts_bcf_id": None,
                "mrbts_id": None,
                "mrbts_dist_name": None,
                "mrbts_managedObjectId": None,
                "join_reference_2": None
            }
            dist_name = elem.attrib["distName"]
            mrbts_dict["mrbts_bsc_id"] = re.search("BSC-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            mrbts_dict["mrbts_bcf_id"] = re.search("BCF-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            mrbts_dict["mrbts_id"] = re.search("MRBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            mrbts_dict["join_reference_2"] = "/".join(dist_name.split("/")[0:3])
            mrbts_dict["mrbts_dist_name"] = dist_name
            mrbts_dict["mrbts_managedObjectId"] = elem.attrib["id"]

            mrbts_list.append(mrbts_dict)

        elem.clear()

    data = etree.iterparse(xml_file)
    for x, y in data:
        if y.tag == "{raml20.xsd}log":
            datetime = y.attrib["dateTime"]
        y.clear()

    if not os.path.exists("2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"):
        os.makedirs("2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/")

    filenames = {
        "BSC.csv": bsc_list, "BCF.csv": bcf_list, "BTS.csv": bts_list,
        "TRX.csv": trx_list, "MRBTS.csv": mrbts_list
    }

    for key, value in filenames.items():
        with open("2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + key,
                  "w") as write_file:
            if len(value):
                headers = value[0].keys()
                csv_writer = csv.DictWriter(write_file, fieldnames=headers)
                csv_writer.writeheader()
                csv_writer.writerows(value)

    try:
        bsc_dict
    except NameError:
        bsc_dict = {
            "bsc_id": None,
            "bsc_managedObjectId": None,
            "bsc_siteId": None,
            "bsc_name": None,
            "bsc_neSwRelease": None,
            "join_reference_1": None
        }
    try:
        bcf_dict
    except NameError:
        bcf_dict = {
            "bcf_bsc_id": None,
            "bcf_id": None,
            "bcf_managedObjectId": None,
            "bcf_siteId": None,
            "bcf_name": None,
            "bcf_adminState": None,
            "bcf_bcfType": None,
            "bcf_address": None,
            "join_reference_2": None,
            "join_reference_1": None
        }
    try:
        bts_dict
    except NameError:
        bts_dict = {
            "bts_bsc_id": None,
            "bts_bcf_id": None,
            "bts_id": None,
            "bts_managedObjectId": None,
            "bts_siteId": None,
            "bts_cellId": None,
            "bts_sectorId": None,
            "bts_segmentId": None,
            "bts_locationAreaIdMCC": None,
            "bts_locationAreaIdMNC": None,
            "bts_name": None,
            "bts_nwName": None,
            "bts_frequencyBandInUse": None,
            "bts_adminState": None,
            "bts_bsIdentityCodeBCC": None,
            "bts_bsIdentityCodeNCC": None,
            "bts_locationAreaIdLAC": None,
            "bts_rac": None,
            "bts_segmentName": None,
            "bts_bcch_freq": None,
            "bts_CellType": None,
            "join_reference_2": None,
            "join_reference_3": None
        }
    try:
        trx_dict
    except NameError:
        trx_dict = {
            "trx_bsc_id": None,
            "trx_bcf_id": None,
            "trx_bts_id": None,
            "trx_id": None,
            "trx_dist_name": None,
            "trx_managedObjectId": None,
            "trx_siteId": None,
            "trx_name": None,
            "trx_initialFrequency": None,
            "trx_adminState": None,
            "trx_channel0Type": None,
            "trx_channel1Type": None,
            "trx_channel2Type": None,
            "trx_channel3Type": None,
            "trx_channel4Type": None,
            "trx_channel5Type": None,
            "trx_channel6Type": None,
            "trx_channel7Type": None,
            "join_reference_3": None
        }
    try:
        mrbts_dict
    except NameError:
        mrbts_dict = {
            "mrbts_bsc_id": None,
            "mrbts_bcf_id": None,
            "mrbts_id": None,
            "mrbts_dist_name": None,
            "mrbts_managedObjectId": None,
            "join_reference_2": None
        }

    if os.path.isfile(
            "2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "BSC.csv") and os.path.getsize(
        "2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "BSC.csv") > 0:
        bsc_file = pd.read_csv("2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "BSC.csv")
    else:
        bsc_file = pd.DataFrame(columns=bsc_dict.keys())
    if os.path.isfile(
            "2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "BCF.csv") and os.path.getsize(
        "2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "BCF.csv") > 0:
        bcf_file = pd.read_csv("2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "BCF.csv")
    else:
        bcf_file = pd.DataFrame(columns=bcf_dict.keys())
    if os.path.isfile(
            "2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "BTS.csv") and os.path.getsize(
        "2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "BTS.csv") > 0:
        bts_file = pd.read_csv("2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "BTS.csv")
    else:
        bts_file = pd.DataFrame(columns=bts_dict.keys())
    if os.path.isfile(
            "2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "TRX.csv") and os.path.getsize(
        "2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "TRX.csv") > 0:
        trx_file = pd.read_csv("2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "TRX.csv")
    else:
        trx_file = pd.DataFrame(columns=trx_dict.keys())
    if os.path.isfile(
            "2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "MRBTS.csv") and os.path.getsize(
        "2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "MRBTS.csv") > 0:
        mrbts_file = pd.read_csv("2G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "MRBTS.csv")
    else:
        mrbts_file = pd.DataFrame(columns=mrbts_dict.keys())

    if (not bsc_file.empty) and (not bcf_file.empty):
        df = pd.merge(bsc_file, bcf_file, on="join_reference_1")
    elif (not bsc_file.empty) and bcf_file.empty:
        df = bsc_file
    elif (not bcf_file.empty) and bsc_file.empty:
        df = bcf_file
    elif bsc_file.empty and bcf_file.empty:
        df = pd.DataFrame()

    if not bts_file.empty:
        df = pd.merge(df, bts_file, on="join_reference_2")
    else:
        df = pd.concat([df, pd.DataFrame(
            columns=["bts_bsc_id", "bts_bcf_id", "bts_id", "bts_managedObjectId", "bts_siteId", "bts_cellId",
                     "bts_sectorId", "bts_segmentId", "bts_locationAreaIdMCC", "bts_locationAreaIdMNC", "bts_name",
                     "bts_nwName", "bts_frequencyBandInUse", "bts_adminState", "bts_bsIdentityCodeBCC",
                     "bts_bsIdentityCodeNCC", "bts_locationAreaIdLAC", "bts_rac", "bts_segmentName", "bts_bcch_freq",
                     "bts_CellType", "join_reference_2", "join_reference_3"])])

    if not trx_file.empty:
        df = pd.merge(df, trx_file, on="join_reference_3")
    else:
        df = pd.concat([df, pd.DataFrame(
            columns=["trx_bsc_id", "trx_bcf_id", "trx_bts_id", "trx_id", "trx_dist_name", "trx_managedObjectId",
                     "trx_siteId", "trx_name", "trx_initialFrequency", "trx_adminState", "trx_channel0Type",
                     "trx_channel1Type", "trx_channel2Type", "trx_channel3Type", "trx_channel4Type",
                     "trx_channel5Type", "trx_channel6Type", "trx_channel7Type", "join_reference_3"])])
    if not mrbts_file.empty:
        df = pd.merge(df, mrbts_file, on="join_reference_2")
    else:
        df = pd.concat([df, pd.DataFrame(columns=["mrbts_bsc_id", "mrbts_bcf_id", "mrbts_id", "mrbts_dist_name",
                                                  "mrbts_managedObjectId", "join_reference_2"])])
    df["datetime"] = datetime
    df.to_csv(
        "2G_Nokia_CM_files/" + "Flattened_" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] +
        ".csv", index=False)
