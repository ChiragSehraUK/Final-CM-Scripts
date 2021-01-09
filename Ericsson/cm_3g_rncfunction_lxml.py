from lxml import etree
import csv
import glob
import pandas as pd


l = []
folder_name = "/home/valiance/Desktop/Cardinality/Country Data/CM Data/new_data/VFRO/RO_CM_3004/Ericsson_3G/"

for xml_file in glob.glob(folder_name + "UTRAN_TOPOLOGY.xml"):
    context = etree.iterparse(xml_file, tag="{utranNrm.xsd}RncFunction")
    new_xml_file = xml_file.replace("/home/valiance/Desktop/Cardinality/Country Data/CM Data", "")
    print(new_xml_file)

    for event, elem in context:
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
                        print(un.text)
            if attribute.tag == "{genericNrm.xsd}VsDataContainer" and count == 0:
                for datacontainer in attribute:
                    for temp in datacontainer:
                        for i in temp:
                            if i.tag == "{EricssonSpecificAttributes.17.09.xsd}primaryCnOperatorRef":
                                d["cn_operator"] = i.text
                                d["join_reference"] = ",".join(i.text.split(",")[:5])
                            if i.tag == "{EricssonSpecificAttributes.17.09.xsd}rncType":
                                d["rnc_type"] = i.text
                    l.append(d)
                    count = 1
        elem.clear()

    data = etree.iterparse(xml_file, tag="{configData.xsd}fileFooter")
    datetime = [y.attrib["dateTime"] for x, y in data][0]

    for i in l:
        i["datetime"] = datetime

print(len(l))
with open("cm_files/3G/3G_rncfunction.csv", "w") as write_file:
    headers = l[0].keys()
    csv_writer = csv.DictWriter(write_file, fieldnames=headers)
    csv_writer.writeheader()
    csv_writer.writerows(l)


