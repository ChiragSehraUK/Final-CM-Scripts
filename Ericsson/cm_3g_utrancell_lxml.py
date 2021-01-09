from lxml import etree
import csv
import glob
from pprint import pprint


l = []
folder_name = "/home/valiance/Desktop/Cardinality/Country Data/CM Data/new_data/VFRO/RO_CM_3004/Ericsson_3G/"

for xml_file in glob.glob(folder_name + "UTRAN_TOPOLOGY.xml"):
    context = etree.iterparse(xml_file, tag="{utranNrm.xsd}UtranCell")
    new_xml_file = xml_file.replace("/home/valiance/Desktop/Cardinality/Country Data/CM Data", "")
    print(new_xml_file)

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
        print(elem.attrib["id"])
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

print(len(l))
with open("cm_files/3G/3G_utrancell.csv", "w") as write_file:
    headers = l[0].keys()
    csv_writer = csv.DictWriter(write_file, fieldnames=headers)
    csv_writer.writeheader()
    csv_writer.writerows(l)


