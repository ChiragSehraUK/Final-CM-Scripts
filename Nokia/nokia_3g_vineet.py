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
    data = etree.iterparse(xml_file, tag="{raml20.xsd}log")
    for x, y in data:
        if y.tag == "{raml20.xsd}log":
            datetime = y.attrib["dateTime"]
        y.clear()

    rnc_list, wbts_list, wcel_list, mrbts_list = [], [], [], []

    for event, elem in context:

        if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "RNC":
            rnc_dict = {
                "rnc_id": None,
                "rnc_managedObjectId": None,
                "rnc_siteId": None,
                "rnc_name": None,
                "rnc_RNCName": None,
                "rnc_CommonMCC": None,
                "rnc_CommonMNC": None,
                "join_reference_1": None
            }
            dist_name = elem.attrib["distName"]
            rnc_dict["rnc_id"] = re.search("RNC-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            rnc_dict["join_reference_1"] = "/".join(dist_name.split("/")[0:2])
            rnc_dict["rnc_managedObjectId"] = elem.attrib["id"]

            for e in elem:
                if e.attrib["name"] == "siteId":
                    rnc_dict["rnc_siteId"] = e.text
                if e.attrib["name"] == "name":
                    rnc_dict["rnc_name"] = e.text
                if e.attrib["name"] == "RNCName":
                    rnc_dict["rnc_RNCName"] = e.text
                if e.attrib["name"] == "CommonMCC":
                    rnc_dict["rnc_CommonMCC"] = e.text
                if e.attrib["name"] == "CommonMNC":
                    rnc_dict["rnc_CommonMNC"] = e.text
            rnc_list.append(rnc_dict)

        if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "WBTS":
            wbts_dict = {
                "wbts_rnc_id": None,
                "wbts_id": None,
                "wbts_managedObjectId": None,
                "wbts_siteId": None,
                "wbts_name": None,
                "wbts_NEType": None,
                "wbts_type": None,
                "join_reference_2": None,
                "join_reference_1": None
            }
            dist_name = elem.attrib["distName"]
            wbts_dict["wbts_rnc_id"] = re.search("RNC-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            wbts_dict["wbts_id"] = re.search("WBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            wbts_dict["join_reference_2"] = dist_name
            wbts_dict["join_reference_1"] = "/".join(dist_name.split("/")[0:2])
            wbts_dict["wbts_managedObjectId"] = elem.attrib["id"]

            for e in elem:
                if e.attrib["name"] == "siteId":
                    wbts_dict["wbts_siteId"] = e.text
                if e.attrib["name"] == "name":
                    wbts_dict["wbts_name"] = e.text
                if e.attrib["name"] == "NEType":
                    wbts_dict["wbts_NEType"] = e.text
                if e.attrib["name"] == "type":
                    wbts_dict["wbts_type"] = e.text
            wbts_list.append(wbts_dict)

        if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "WCEL":
            wcel_dict = {
                "wcel_rnc_id": None,
                "wcel_wbts_id": None,
                "wcel_id": None,
                "wcel_dist_name": None,
                "wcel_managedObjectId": None,
                "wcel_siteId": None,
                "wcel_WCELMCC": None,
                "wcel_WCELMNC": None,
                "wcel_name": None,
                "wcel_CId": None,
                "wcel_LAC": None,
                "wcel_RAC": None,
                "wcel_SAC": None,
                "wcel_MaxNumberHSDPAUsers": None,
                "wcel_PriScrCode": None,
                "wcel_SectorID": None,
                "wcel_UARFCN": None,
                "wcel_WCelState": None,
                "wcel_CellType": None,
                "join_reference_2": None
            }
            dist_name = elem.attrib["distName"]
            wcel_dict["wcel_rnc_id"] = re.search("RNC-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            wcel_dict["wcel_wbts_id"] = re.search("WBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            wcel_dict["wcel_id"] = re.search("WCEL-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            wcel_dict["wcel_dist_name"] = dist_name
            wcel_dict["join_reference_2"] = "/".join(dist_name.split("/")[0:3])
            wcel_dict["wcel_managedObjectId"] = elem.attrib["id"]

            for e in elem:
                if e.attrib["name"] == "siteId":
                    wcel_dict["wcel_siteId"] = e.text
                if e.attrib["name"] == "WCELMCC":
                    wcel_dict["wcel_WCELMCC"] = e.text
                if e.attrib["name"] == "WCELMNC":
                    wcel_dict["wcel_WCELMNC"] = e.text
                if e.attrib["name"] == "name":
                    wcel_dict["wcel_name"] = e.text
                if e.attrib["name"] == "CId":
                    wcel_dict["wcel_CId"] = e.text
                if e.attrib["name"] == "LAC":
                    wcel_dict["wcel_LAC"] = e.text
                if e.attrib["name"] == "RAC":
                    wcel_dict["wcel_RAC"] = e.text
                if e.attrib["name"] == "SAC":
                    wcel_dict["wcel_SAC"] = e.text
                if e.attrib["name"] == "MaxNumberHSDPAUsers":
                    wcel_dict["wcel_MaxNumberHSDPAUsers"] = e.text
                if e.attrib["name"] == "PriScrCode":
                    wcel_dict["wcel_PriScrCode"] = e.text
                if e.attrib["name"] == "SectorID":
                    wcel_dict["wcel_SectorID"] = e.text
                if e.attrib["name"] == "UARFCN":
                    wcel_dict["wcel_UARFCN"] = e.text
                if e.attrib["name"] == "WCelState":
                    wcel_dict["wcel_WCelState"] = e.text
                if e.attrib["name"] == "CellType":
                    wcel_dict["wcel_CellType"] = e.text
            wcel_list.append(wcel_dict)

        if elem.tag == "{raml20.xsd}managedObject" and elem.attrib["class"] == "MRBTS" and "RNC" in elem.attrib[
            "distName"] and "WBTS" in elem.attrib["distName"] and len(elem.attrib["distName"].split("/")) == 4:
            mrbts_dict = {
                "mrbts_rnc_id": None,
                "mrbts_wbts_id": None,
                "mrbts_id": None,
                "mrbts_dist_name": None,
                "mrbts_managedObjectId": None,
                "join_reference_1": None
            }

            dist_name = elem.attrib["distName"]
            mrbts_dict["mrbts_rnc_id"] = re.search("RNC-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            mrbts_dict["mrbts_wbts_id"] = re.search("WBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            mrbts_dict["mrbts_id"] = re.search("MRBTS-([aA0-zZ9]*)", elem.attrib["distName"]).group(1)
            mrbts_dict["join_reference_1"] = "/".join(dist_name.split("/")[0:2])
            mrbts_dict["mrbts_dist_name"] = dist_name
            mrbts_dict["mrbts_managedObjectId"] = elem.attrib["id"]

            mrbts_list.append(mrbts_dict)

        elem.clear()

    if not os.path.exists("3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"):
        os.makedirs("3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/")

    filenames = {
        "RNC.csv": rnc_list, "WBTS.csv": wbts_list, "WCEL.csv": wcel_list, "MRBTS.csv": mrbts_list
    }

    for key, value in filenames.items():
        with open("3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + key, "w") as write_file:
            # print(value)
            if value:
                headers = value[0].keys()
                csv_writer = csv.DictWriter(write_file, fieldnames=headers)
                csv_writer.writeheader()
                csv_writer.writerows(value)

    try:
        rnc_dict
    except NameError:
        rnc_dict = {
            "rnc_id": None,
            "rnc_managedObjectId": None,
            "rnc_siteId": None,
            "rnc_name": None,
            "rnc_RNCName": None,
            "rnc_CommonMCC": None,
            "rnc_CommonMNC": None,
            "join_reference_1": None
        }
    try:
        wbts_dict
    except NameError:
        wbts_dict = {
            "wbts_rnc_id": None,
            "wbts_id": None,
            "wbts_managedObjectId": None,
            "wbts_siteId": None,
            "wbts_name": None,
            "wbts_NEType": None,
            "wbts_type": None,
            "join_reference_2": None,
            "join_reference_1": None
        }
    try:
        wcel_dict
    except NameError:
        wcel_dict = {
            "wcel_rnc_id": None,
            "wcel_wbts_id": None,
            "wcel_id": None,
            "wcel_dist_name": None,
            "wcel_managedObjectId": None,
            "wcel_siteId": None,
            "wcel_WCELMCC": None,
            "wcel_WCELMNC": None,
            "wcel_name": None,
            "wcel_CId": None,
            "wcel_LAC": None,
            "wcel_RAC": None,
            "wcel_SAC": None,
            "wcel_MaxNumberHSDPAUsers": None,
            "wcel_PriScrCode": None,
            "wcel_SectorID": None,
            "wcel_UARFCN": None,
            "wcel_WCelState": None,
            "wcel_CellType": None,
            "join_reference_2": None
        }
    try:
        mrbts_dict
    except NameError:
        mrbts_dict = {
            "mrbts_rnc_id": None,
            "mrbts_wbts_id": None,
            "mrbts_id": None,
            "mrbts_dist_name": None,
            "mrbts_managedObjectId": None,
            "join_reference_1": None
        }

    if os.path.isfile(
            "3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "RNC.csv") and os.path.getsize(
        "3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "RNC.csv") > 0:
        rnc_file = pd.read_csv("3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "RNC.csv")
    else:
        rnc_file = pd.DataFrame(columns=rnc_dict.keys())
    if os.path.isfile(
            "3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "WBTS.csv") and os.path.getsize(
        "3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "WBTS.csv") > 0:
        wbts_file = pd.read_csv("3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "WBTS.csv")
    else:
        wbts_file = pd.DataFrame(columns=wbts_dict.keys())
    if os.path.isfile(
            "3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "WCEL.csv") and os.path.getsize(
        "3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "WCEL.csv") > 0:
        wcel_file = pd.read_csv("3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "WCEL.csv")
    else:
        wcel_file = pd.DataFrame(columns=wcel_dict.keys())
    if os.path.isfile(
            "3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "MRBTS.csv") and os.path.getsize(
        "3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "MRBTS.csv") > 0:
        mrbts_file = pd.read_csv("3G_Nokia_CM_files/" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "MRBTS.csv")
    else:
        mrbts_file = pd.DataFrame(columns=mrbts_dict.keys())

    if (not rnc_file.empty) and (not wbts_file.empty):
        df = pd.merge(rnc_file, wbts_file, on="join_reference_1")
    elif (not rnc_file.empty) and wbts_file.empty:
        df = rnc_file
    elif rnc_file.empty and (not wbts_file.empty):
        df = wbts_file
    elif rnc_file.empty and wbts_file.empty:
        df = pd.DataFrame()
    if not wcel_file.empty:
        df = pd.merge(df, wcel_file, on="join_reference_2")
    else:
        df = pd.concat([df, pd.DataFrame(columns=wcel_dict.keys())])
    if not mrbts_file.empty:
        df = pd.merge(df, mrbts_file, on="join_reference_1")
    else:
        df = pd.merge(df, pd.DataFrame(columns=mrbts_dict.keys()))

    df["datetime"] = datetime
    # print(df.shape)

    df.to_csv("3G_Nokia_CM_files/" + "Flattened_" + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", index=False)
