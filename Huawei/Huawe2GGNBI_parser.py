import xml.etree.ElementTree as ET
import glob
import pandas as pd
import os
import csv
import time
import argparse
import shutil

parser = argparse.ArgumentParser(description="Arguments for 2G CM files")
parser.add_argument('COUNTRY', metavar='COUNTRY', type=str, help='country of CM files')
parser.add_argument('TECH', metavar='TECH',type=str,help='technology of CM files')
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

for xml_file in glob.glob(sourcePath+"/GNBIExport*"):
    print(xml_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()

    new_xml_file = xml_file
    bts_list = list()
    gtrx_list = list()
    gcell_list = list()
    gcellbtspara_list = list()

    for filefooter in root.findall("{http://www.huawei.com/specs/SOM}filefooter"):
        date_time = filefooter.attrib["datetime"]

    for netag in root.iter("{http://www.huawei.com/specs/SOM}NE"):
        for moduletag in netag:
            for moitag in moduletag:
                if moitag.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == "GCELL":
                    gcell_dict = {'gcell_cellname': None, 'gcell_cellid': None, 'gcell_opname': None, 'gcell_lac': None,
                                  'gcell_rac': None, 'gcell_mcc': None, 'gcell_mnc': None, 'gcell_type': None,
                                  'bts_btsname': None, "neversion":None}
                    for attributetag in moitag:
                        for btstag in attributetag:
                            if btstag.tag == "{http://www.huawei.com/specs/SOM}CELLNAME":
                                # gcellcellname_list.append(btstag.text)
                                gcell_dict['gcell_cellname'] = btstag.text
                                gcell_dict['bts_btsname'] = btstag.text[:-1]
                                gcell_dict['neversion'] = netag.attrib["neversion"]

                            if btstag.tag == "{http://www.huawei.com/specs/SOM}CELLID":
                                # gcellcellid_list.append(btstag.text)
                                gcell_dict["gcell_cellid"] = btstag.text

                            if btstag.tag == "{http://www.huawei.com/specs/SOM}OPNAME":
                                # gcellopname_list.append(btstag.text)
                                gcell_dict["gcell_opname"] = btstag.text

                            if btstag.tag == "{http://www.huawei.com/specs/SOM}LAC":
                                # gcelllac_list.append(btstag.text)
                                gcell_dict["gcell_lac"] = btstag.text

                            if btstag.tag == "{http://www.huawei.com/specs/SOM}RAC":
                                # gcellrac_list.append(btstag.text)
                                gcell_dict["gcell_rac"] = btstag.text
                            if btstag.tag == "{http://www.huawei.com/specs/SOM}MCC":
                                # gcellmcc_list.append(btstag.text)
                                gcell_dict["gcell_mcc"] = btstag.text
                            if btstag.tag == "{http://www.huawei.com/specs/SOM}MNC":
                                # gcellmnc_list.append(btstag.text)
                                gcell_dict["gcell_mnc"] = btstag.text
                            if btstag.tag == "{http://www.huawei.com/specs/SOM}TYPE":
                                # gcelltype_list.append(btstag.text)
                                gcell_dict["gcell_type"] = btstag.text
                    gcell_list.append(gcell_dict)

                if moitag.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == "GTRX":
                    gtrx_dict = {'gtrx_cellid': None, 'gtrx_trxno': None, 'gtrx_gtrxname': None, 'gcell_cellname': None}
                    for attributetag in moitag:
                        for btstag in attributetag:
                            if btstag.tag == "{http://www.huawei.com/specs/SOM}CELLID":
                                gtrx_dict["gtrx_cellid"] = btstag.text

                            if btstag.tag == "{http://www.huawei.com/specs/SOM}TRXNO":
                                gtrx_dict["gtrx_trxno"] = btstag.text
                            # gtrxtrxno_list.append(btstag.text)

                            if btstag.tag == "{http://www.huawei.com/specs/SOM}TRXNAME":
                                gtrx_dict["gtrx_gtrxname"] = btstag.text
                                gtrx_dict["gcell_cellname"] = btstag.text[:7]
                    gtrx_list.append(gtrx_dict)

                if moitag.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == "BTS":
                    bts_dict = {'bts_btsid': None, 'bts_btsname': None, 'bts_btstype': None}
                    for attributetag in moitag:
                        for btstag in attributetag:
                            if btstag.tag == "{http://www.huawei.com/specs/SOM}BTSID":
                                bts_dict["bts_btsid"] = btstag.text

                            if btstag.tag == "{http://www.huawei.com/specs/SOM}BTSNAME":
                                bts_dict["bts_btsname"] = btstag.text

                            if btstag.tag == "{http://www.huawei.com/specs/SOM}BTSTYPE":
                                bts_dict["bts_btstype"] = btstag.text
                    bts_list.append(bts_dict)

                if moitag.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == "GCELLBTSSOFTPARA":
                    gcellbtspara_dict = {'gcellbtsoftpara_cellid': None, "gcellbtsoftpara_btsid": None}
                    for attributetag in moitag:
                        for btstag in attributetag:
                            if btstag.tag == "{http://www.huawei.com/specs/SOM}CELLID":
                                gcellbtspara_dict["gcellbtsoftpara_cellid"] = btstag.text
                            if btstag.tag == "{http://www.huawei.com/specs/SOM}BTSID":
                                gcellbtspara_dict["gcellbtsoftpara_btsid"] = btstag.text

                    gcellbtspara_list.append(gcellbtspara_dict)

    if not os.path.exists(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/"):
        os.makedirs(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/")

    filenames = {
        "BTS.csv": bts_list, "GCELL.csv": gcell_list, "GTRX.csv": gtrx_list, "GCELLBTSPARA.csv": gcellbtspara_list
    }

    for key, value in filenames.items():
        with open(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + key, "w") as write_file:
            if value:
                headers = value[0].keys()
                csv_writer = csv.DictWriter(write_file, fieldnames=headers)
                csv_writer.writeheader()
                csv_writer.writerows(value)

    gcell_file = pd.read_csv(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "GCELL.csv")
    bts_file = pd.read_csv(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "BTS.csv")
    gtrx_file = pd.read_csv(tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "GTRX.csv")
    gcellbtstpara_file = pd.read_csv(
        tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0] + "/" + "GCELLBTSPARA.csv")

    trx_gcell_merge = pd.merge(left=gcell_file, right=gtrx_file, on="gcell_cellname")
    trx_gcell_bts_merge = pd.merge(left=trx_gcell_merge, right=bts_file, on="bts_btsname")
    trx_gcell_bts_gcellbtstpara_merge = pd.merge(left=trx_gcell_bts_merge, right=gcellbtstpara_file,
                                                 left_on=["gcell_cellid", "bts_btsid"],
                                                 right_on=["gcellbtsoftpara_cellid", "gcellbtsoftpara_btsid"])

    trx_gcell_bts_gcellbtstpara_merge["datetime"] = date_time
    trx_gcell_bts_gcellbtstpara_merge.to_csv(destinationPath +
                                             new_xml_file.rsplit("/")[-1].rsplit(".")[0] + ".csv", index=False)

    # deleting the folder of files created
    print("Deleting the temporary created folders...")
    dir_path = tempPath + new_xml_file.rsplit("/")[-1].rsplit(".")[0]
    shutil.rmtree(dir_path)
