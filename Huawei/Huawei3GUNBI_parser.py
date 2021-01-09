import xml.etree.ElementTree as ET
import glob
import pandas as pd
from pprint import pprint
import time
import os
import collections
import csv
import argparse
import shutil

parser = argparse.ArgumentParser(description="Arguments for 3G CM files")
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


for xml_file in glob.glob(sourcePath + "/UNBIExport*"):
    if "RT" in xml_file:
        flag = True
    elif "RF" in xml_file:
        flag = False

    tree = ET.parse(xml_file)
    root = tree.getroot()
    new_xml_file = xml_file

    for filefooter in root.findall("{http://www.huawei.com/specs/SOM}filefooter"):
        datetime = filefooter.attrib["datetime"]

    unodeb_list = []
    ucell_list = []
    radio_adjnode_list = []
    transmission_adjnode_list = []
    radio_ippath_list = []
    transmission_ippath_list = []
    upcpich_list = []

    for netag in root.iter("{http://www.huawei.com/specs/SOM}NE"):
        for moduletag in netag:
            if flag:
                if moduletag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "Radio":
                    for moitag in moduletag:
                        if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "UCELL":
                            ucell_dict = {
                                "neid": None,
                                "ucell_cellname": None,
                                "ucell_locell": None,
                                "ucell_nodebname": None,
                                "ucell_cellid": None,
                                "ucell_lac": None,
                                "ucell_rac": None,
                                "ucell_maxtxpower": None,
                                "ucell_uarfcndownlink": None,
                                "ucell_uarfcnuplink": None,
                                "ucell_cnopgrpindex": None,
                                "ucell_pscrambcode": None, "ucell_actstatus": None, "ucell_blkstatus": None
                            }
                            for attributetag in moitag:
                                for btstag in attributetag:
                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}CELLNAME":
                                        ucell_dict["ucell_cellname"] = btstag.text
                                        ucell_dict["neid"] = netag.attrib["neid"]

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}LOCELL":
                                        ucell_dict["ucell_locell"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}NODEBNAME":
                                        ucell_dict["ucell_nodebname"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}CELLID":
                                        ucell_dict["ucell_cellid"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}LAC":
                                        ucell_dict["ucell_lac"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}RAC":
                                        ucell_dict["ucell_rac"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}MAXTXPOWER":
                                        ucell_dict["ucell_maxtxpower"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}UARFCNDOWNLINK":
                                        ucell_dict["ucell_uarfcndownlink"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}UARFCNUPLINK":
                                        ucell_dict["ucell_uarfcnuplink"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}CNOPGRPINDEX":
                                        ucell_dict["ucell_cnopgrpindex"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}PSCRAMBCODE":
                                        ucell_dict["ucell_pscrambcode"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}ACTSTATUS":
                                        ucell_dict["ucell_actstatus"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}BLKSTATUS":
                                        ucell_dict["ucell_blkstatus"] = btstag.text
                            ucell_list.append(ucell_dict)

                        if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "UNODEB":
                            unodeb_dict = {
                                "unodeb_nodebname": None, "unodeb_nodebid": None
                            }
                            for attributetag in moitag:
                                for btstag in attributetag:
                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}NODEBNAME":
                                        unodeb_dict["unodeb_nodebname"] = btstag.text
                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}NODEBID":
                                        unodeb_dict["unodeb_nodebid"] = btstag.text
                            unodeb_list.append(unodeb_dict)

                        if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "ADJNODE":
                            radio_adjnode_dict = {
                                "radio_adjnode_nodebid": None, "radio_adjnode_name": None, "radio_adjnode_ani": None
                            }
                            for attributetag in moitag:
                                for btstag in attributetag:
                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}NODEBID":
                                        radio_adjnode_dict["radio_adjnode_nodebid"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}NAME":
                                        radio_adjnode_dict["radio_adjnode_name"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}ANI":
                                        radio_adjnode_dict["radio_adjnode_ani"] = btstag.text
                            radio_adjnode_list.append(radio_adjnode_dict)

                        if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "IPPATH":
                            radio_ippath_dict = {
                                "radio_ippath_ani": None, "radio_ippath_pathid": None, "radio_ippath_patht": None
                            }
                            for attributetag in moitag:
                                for btstag in attributetag:
                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}ANI":
                                        radio_ippath_dict["radio_ippath_ani"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}PATHID":
                                        radio_ippath_dict["radio_ippath_pathid"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}PATHT":
                                        radio_ippath_dict["radio_ippath_patht"] = btstag.text
                            radio_ippath_list.append(radio_ippath_dict)

                        if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "UPCPICH":
                            upcpich_dict = {
                                "upcpich_maxpcpichpower": None, "upcpich_pcpichpower": None,
                                "upcpich_minpcpichpower": None, "upcpich_cellid": None
                            }
                            for attributetag in moitag:
                                for btstag in attributetag:
                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}MAXPCPICHPOWER":
                                        upcpich_dict["upcpich_maxpcpichpower"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}PCPICHPOWER":
                                        upcpich_dict["upcpich_pcpichpower"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}MINPCPICHPOWER":
                                        upcpich_dict["upcpich_minpcpichpower"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}CELLID":
                                        upcpich_dict["upcpich_cellid"] = btstag.text

                            upcpich_list.append(upcpich_dict)

                if moduletag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "Transmission":
                    for moitag in moduletag:
                        if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "ADJNODE":
                            transmission_adjnode_dict = {
                                "transmission_adjnode_nodebid": None, "transmission_adjnode_name": None,
                                "transmission_adjnode_ani": None
                            }
                            for attributetag in moitag:
                                for btstag in attributetag:
                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}NAME":
                                        transmission_adjnode_dict["transmission_adjnode_name"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}NODEBID":
                                        transmission_adjnode_dict["transmission_adjnode_nodebid"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}ANI":
                                        transmission_adjnode_dict["transmission_adjnode_ani"] = btstag.text
                            transmission_adjnode_list.append(transmission_adjnode_dict)

                        if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "IPPATH":
                            transmission_ippath_dict = {
                                "transmission_ippath_ani": None, "transmission_ippath_pathid": None,
                                "transmission_ippath_patht": None
                            }
                            for attributetag in moitag:
                                for btstag in attributetag:
                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}ANI":
                                        transmission_ippath_dict["transmission_ippath_ani"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}PATHID":
                                        transmission_ippath_dict["transmission_ippath_pathid"] = btstag.text

                                    if btstag.tag == "{http://www.huawei.com/specs/SOM}PATHT":
                                        transmission_ippath_dict["transmission_ippath_patht"] = btstag.text
                            transmission_ippath_list.append(transmission_ippath_dict)


            else:
                for moitag in moduletag:
                    if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "UCELL":
                        ucell_dict = {
                            "neid": None,
                            "ucell_cellname": None,
                            "ucell_locell": None,
                            "ucell_nodebname": None,
                            "ucell_cellid": None,
                            "ucell_lac": None,
                            "ucell_rac": None,
                            "ucell_maxtxpower": None,
                            "ucell_uarfcndownlink": None,
                            "ucell_uarfcnuplink": None,
                            "ucell_cnopgrpindex": None,
                            "ucell_pscrambcode": None, "ucell_actstatus": None, "ucell_blkstatus": None
                        }
                        for attributetag in moitag:
                            for btstag in attributetag:
                                if btstag.tag == "{http://www.huawei.com/specs/SOM}CELLNAME":
                                    ucell_dict["ucell_cellname"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}LOCELL":
                                    ucell_dict["ucell_locell"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}NODEBNAME":
                                    ucell_dict["ucell_nodebname"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}CELLID":
                                    ucell_dict["ucell_cellid"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}LAC":
                                    ucell_dict["ucell_lac"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}RAC":
                                    ucell_dict["ucell_rac"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}MAXTXPOWER":
                                    ucell_dict["ucell_maxtxpower"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}UARFCNDOWNLINK":
                                    ucell_dict["ucell_uarfcndownlink"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}UARFCNUPLINK":
                                    ucell_dict["ucell_uarfcnuplink"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}CNOPGRPINDEX":
                                    ucell_dict["ucell_cnopgrpindex"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}PSCRAMBCODE":
                                    ucell_dict["ucell_pscrambcode"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}ACTSTATUS":
                                    ucell_dict["ucell_actstatus"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}BLKSTATUS":
                                    ucell_dict["ucell_blkstatus"] = btstag.text
                        ucell_list.append(ucell_dict)

                    if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "UNODEB":
                        unodeb_dict = {
                            "unodeb_nodebname": None, "unodeb_nodebid": None
                        }
                        for attributetag in moitag:
                            for btstag in attributetag:
                                if btstag.tag == "{http://www.huawei.com/specs/SOM}NODEBNAME":
                                    unodeb_dict["unodeb_nodebname"] = btstag.text
                                    unodebnodebname_list = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}NODEBID":
                                    unodeb_dict["unodeb_nodebid"] = btstag.text

                            unodeb_list.append(unodeb_dict)

                    if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "ADJNODE":
                        radio_adjnode_dict = {
                            "radio_adjnode_nodebid": None, "radio_adjnode_name": None, "radio_adjnode_ani": None
                        }
                        for attributetag in moitag:
                            for btstag in attributetag:
                                if btstag.tag == "{http://www.huawei.com/specs/SOM}NODEBID":
                                    radio_adjnode_dict["radio_adjnode_nodebid"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}NAME":
                                    radio_adjnode_dict["radio_adjnode_name"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}ANI":
                                    radio_adjnode_dict["radio_adjnode_ani"] = btstag.text
                        radio_adjnode_list.append(radio_adjnode_dict)

                    if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "IPPATH":
                        radio_ippath_dict = {
                            "radio_ippath_ani": None, "radio_ippath_pathid": None, "radio_ippath_patht": None
                        }
                        for attributetag in moitag:
                            for btstag in attributetag:
                                if btstag.tag == "{http://www.huawei.com/specs/SOM}ANI":
                                    radio_ippath_dict["radio_ippath_ani"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}PATHID":
                                    radio_ippath_dict["radio_ippath_pathid"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}PATHT":
                                    radio_ippath_dict["radio_ippath_patht"] = btstag.text

                    if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "UPCPICH":
                        upcpich_dict = {
                            "upcpich_maxpcpichpower": None, "upcpich_pcpichpower": None,
                            "upcpich_minpcpichpower": None, "upcpich_cellid": None
                        }
                        for attributetag in moitag:
                            for btstag in attributetag:
                                if btstag.tag == "{http://www.huawei.com/specs/SOM}MAXPCPICHPOWER":
                                    upcpich_dict["upcpich_maxpcpichpower"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}PCPICHPOWER":
                                    upcpich_dict["upcpich_pcpichpower"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}MINPCPICHPOWER":
                                    upcpich_dict["upcpich_minpcpichpower"] = btstag.text

                                if btstag.tag == "{http://www.huawei.com/specs/SOM}CELLID":
                                    upcpich_dict["upcpich_cellid"] = btstag.text

    if not os.path.exists(tempPath  + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"):
        os.makedirs(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/")

    if flag:
        filenames = {
            "UCELL.csv": ucell_list, "UNODEB.csv": unodeb_list, "RADIO_ADJNODE.csv": radio_adjnode_list,
            "RADIO_IPPATH.csv": radio_ippath_list, "UPCPICH.csv": upcpich_list,
            "TRANSMISSION_ADJNODE.csv": transmission_adjnode_list,
            "TRANSMISSION_IPPATH.csv": transmission_ippath_list
        }
    else:
        filenames = {
            "UCELL.csv": ucell_list, "UNODEB.csv": unodeb_list, "RADIO_ADJNODE.csv": radio_adjnode_list,
            "RADIO_IPPATH.csv": radio_ippath_list, "UPCPICH.csv": upcpich_list
        }

    for key, value in filenames.items():
        with open(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + key,
                  "w") as write_file:
            if len(value):
                headers = value[0].keys()
                csv_writer = csv.DictWriter(write_file, fieldnames=headers)
                csv_writer.writeheader()
                csv_writer.writerows(value)

    ucell_file = pd.read_csv(
        tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "UCELL.csv")
    unodeb_file = pd.read_csv(
        tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "UNODEB.csv")
    transmission_adjnode_file = pd.read_csv(
        tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" +
        "TRANSMISSION_ADJNODE.csv")
    # transmission_ippath_file = pd.read_csv("UNBI_CM_files/" + xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" +
    # "TRANSMISSION_IPPATH.csv")
    upcpich_file = pd.read_csv(
       tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "UPCPICH.csv")

    ucell_unodeb_merge = pd.merge(left=ucell_file, right=unodeb_file, left_on=["ucell_locell"],
                                  right_on=["unodeb_nodebid"])
    ucell_unodeb_adjnode_merge = pd.merge(left=ucell_unodeb_merge, right=transmission_adjnode_file,
                                          left_on=["unodeb_nodebid"], right_on=["transmission_adjnode_nodebid"])
    ucell_unodeb_adjnode_upcpich_merge = pd.merge(left=ucell_unodeb_adjnode_merge, right=upcpich_file,
                                                  left_on=["ucell_cellid"], right_on=["upcpich_cellid"])

    ucell_unodeb_adjnode_upcpich_merge["datetime"] = datetime
    # new_xml_file = new_xml_file.replace("\\", "/")
    ucell_unodeb_adjnode_upcpich_merge.to_csv(
        destinationPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", index=False)

    # deleting the folder of files created
    print("Deleting the temporary created folders...")
    dir_path = tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0]
    shutil.rmtree(dir_path)

