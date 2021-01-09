import xml.etree.ElementTree as ET
import glob
from pprint import pprint
import pandas as pd
import csv
import time

# UNIQUE ID: -> Country – eNodeBname – CELLNAME – LOCALCELLID-ENODEBID XSI type: ENODEBFUNCTION -> <ENODEBID>
# <ENODEBFUNCTIONNAME> XSI Ttype: CELL -> <CELLNAME> <LOCALCELLID> <FREQBAND> <ULEARFCNCFGIND> <DLEARFCN>
# <ULBANDWIDTH> <DLBANDWIDTH> <CELLACTIVESTATE> <CELLADMINSTATE>

begin_time = time.time()

for xml_file in glob.glob("C:/Users/Administrator/Downloads/VF-ES CM Huawei files/Huawei "
                          "2G3G4G5G/files/4G/SRANNBIExport*.xml"):
    # print(xml_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()
    new_xml_file = xml_file.replace("C:/Users/Administrator/Downloads/VF-ES CM Huawei files/Huawei 2G3G4G5G/files/4G",
                                    "")
    new_xml_file = new_xml_file[1:]
    print(new_xml_file)

    for filefooter in root.findall("{http://www.huawei.com/specs/SRAN}filefooter"):
        datetime = filefooter.attrib["datetime"]

    for netag in root.iter("{http://www.huawei.com/specs/SRAN}NE"):
        neversion = netag.attrib["neversion"]

    l = list()
    d = dict()
    mm_cellname, mm_cellid, mm_enodename, mm_enodebid, mm_datetime = [], [], [], [], []
    mm_freqband, mm_ulearfcnffgind, mm_dlearfnc, mm_ulbandwidth, mm_dlbandwidth, mm_cellactivestate, mm_celladminstate, mm_userlabel = [], [], [], [], [], [], [], []
    mm_neversion = []
    masterdict = dict()

    for netag in root.iter("{http://www.huawei.com/specs/SRAN}NE"):
        for moduletag in netag:
            enodebfunctionname_list = []
            enodebid_list = []
            cellname_list = []
            localcell_id_list = []
            freqband_list = []
            ulearfcncfgind_list = []
            dlearfcn_list = []
            ulbandwidth_list = []
            dlbandwidth_list = []
            cellactivestate_list = []
            celladminstate_list = []
            userlabel_list = []

            for moitag in moduletag:
                if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "CELL":
                    for attributetag in moitag:
                        for btstag in attributetag:
                            if btstag.tag == "{http://www.huawei.com/specs/SRAN}CELLNAME":
                                cellname_list.append(btstag.text)

                            if btstag.tag == "{http://www.huawei.com/specs/SRAN}LOCALCELLID":
                                localcell_id_list.append(btstag.text)

                            if btstag.tag == "{http://www.huawei.com/specs/SRAN}FREQBAND":
                                if btstag.text is None:
                                    freqband_list.append(None)
                                else:
                                    freqband_list.append(btstag.text)

                            if btstag.tag == "{http://www.huawei.com/specs/SRAN}ULEARFCNCFGIND":
                                if btstag.text is None:
                                    ulearfcncfgind_list.append(None)
                                else:
                                    ulearfcncfgind_list.append(btstag.text)

                            if btstag.tag == "{http://www.huawei.com/specs/SRAN}DLEARFCN":
                                if btstag.text is None:
                                    dlearfcn_list.append(None)
                                else:
                                    dlearfcn_list.append(btstag.text)

                            if btstag.tag == "{http://www.huawei.com/specs/SRAN}ULBANDWIDTH":
                                if btstag.text is None:
                                    ulbandwidth_list.append(None)
                                else:
                                    ulbandwidth_list.append(btstag.text)

                            if btstag.tag == "{http://www.huawei.com/specs/SRAN}DLBANDWIDTH":
                                if btstag.text is None:
                                    dlbandwidth_list.append(None)
                                else:
                                    dlbandwidth_list.append(btstag.text)

                            if btstag.tag == "{http://www.huawei.com/specs/SRAN}CELLACTIVESTATE":
                                if btstag.text is None:
                                    cellactivestate_list.append(None)
                                else:
                                    cellactivestate_list.append(btstag.text)

                            if btstag.tag == "{http://www.huawei.com/specs/SRAN}CELLADMINSTATE":
                                if btstag.text is None:
                                    celladminstate_list.append(None)
                                else:
                                    celladminstate_list.append(btstag.text)

                            if btstag.tag == "{http://www.huawei.com/specs/SRAN}USERLABEL":
                                if btstag.text is None:
                                    userlabel_list.append(None)
                                else:
                                    userlabel_list.append(btstag.text)

                if moitag.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "ENODEBFUNCTION":
                    for attributetag in moitag:
                        for btstag in attributetag:
                            if btstag.tag == "{http://www.huawei.com/specs/SRAN}ENODEBFUNCTIONNAME":
                                enodebfunctionname_list.append(btstag.text)

                            if btstag.tag == "{http://www.huawei.com/specs/SRAN}ENODEBID":
                                enodebid_list.append(btstag.text)

            d["cellname"] = cellname_list
            d["localcellid"] = localcell_id_list
            d["freqband"] = freqband_list
            d["ulearfcncfgind"] = ulearfcncfgind_list
            d["dleardcn"] = dlearfcn_list
            d["ulbandwidth"] = ulbandwidth_list
            d["dlbandwidth"] = dlbandwidth_list
            d["cellactivestate"] = cellactivestate_list
            d["celladminstate"] = celladminstate_list
            d["userlabel"] = userlabel_list

            d["enodefunctionname"] = enodebfunctionname_list
            d["enodebid"] = enodebid_list
            # pprint(d)

            mastercellname_list, mastercellid_list, masterenodebfunctionname_list, masterenodebid_list = [], [], [], []
            masterfreqband_list, mastereleardncnfgoind_list, masterdleardcn_list, masterulbandwidth_list, masterdlbandwidth_list, mastercellactivestate_list, mastercelladminstate_list, masteruserlabel_list = [], [], [], [], [], [], [], []

            if d["cellname"]:
                # print(dlbandwidth_list)
                for i in range(0, len(cellname_list)):
                    mastercellname_list.append(cellname_list[i])
                    mastercellid_list.append(localcell_id_list[i])
                    # print(i)
                    # print("ith",freqband_list[i])
                    # print("list",freqband_list)
                    # print("enodebfunction ith",enodebfunctionname_list[0])
                    # print("cellname ith",cellname_list[i])

                    if i >= len(freqband_list):
                        masterfreqband_list.append(None)
                    else:
                        masterfreqband_list.append(freqband_list[i])

                    if i >= len(ulearfcncfgind_list):
                        mastereleardncnfgoind_list.append(None)
                    else:
                        mastereleardncnfgoind_list.append(ulearfcncfgind_list[i])

                    if i >= len(dlearfcn_list):
                        masterdleardcn_list.append(None)
                    else:
                        masterdleardcn_list.append(dlearfcn_list[i])

                    if i >= len(ulbandwidth_list):
                        masterulbandwidth_list.append(None)
                    else:
                        masterulbandwidth_list.append(ulbandwidth_list[i])

                    if i >= len(dlbandwidth_list):
                        masterdlbandwidth_list.append(None)
                    else:
                        masterdlbandwidth_list.append(dlbandwidth_list[i])

                    if i >= len(cellactivestate_list):
                        mastercellactivestate_list.append(None)
                    else:
                        mastercellactivestate_list.append(cellactivestate_list[i])

                    if i >= len(celladminstate_list):
                        mastercelladminstate_list.append(None)
                    else:
                        mastercelladminstate_list.append(celladminstate_list[i])

                    if i >= len(userlabel_list):
                        masteruserlabel_list.append(None)
                    else:
                        masteruserlabel_list.append(userlabel_list[i])
                    masterenodebfunctionname_list.append(enodebfunctionname_list[0])
                    masterenodebid_list.append(enodebid_list[0])
            #
            mm_cellid.extend(mastercellid_list)
            mm_cellname.extend(mastercellname_list)
            mm_enodebid.extend(masterenodebid_list)
            mm_enodename.extend(masterenodebfunctionname_list)
            mm_freqband.extend(masterfreqband_list)
            mm_ulearfcnffgind.extend(mastereleardncnfgoind_list)
            mm_dlearfnc.extend(masterdleardcn_list)
            mm_ulbandwidth.extend(masterulbandwidth_list)
            mm_dlbandwidth.extend(masterdlbandwidth_list)
            mm_cellactivestate.extend(mastercellactivestate_list)
            mm_celladminstate.extend(mastercelladminstate_list)
            mm_userlabel.extend(masteruserlabel_list)

    for i in range(0, len(mm_cellname)):
        mm_datetime.append(datetime)

    for i in range(0,len(mm_cellname)):
        mm_neversion.append(neversion)

    df = pd.DataFrame(
        columns=["enodebname", "cellname", "localcellid", "enodebid", "freqband", "ulearfcnffgind", "dlearfnc",
                 "ulbandwidth", "dlbandwidth", "cellactivestate", "celladminstate", "userlabel", "datetime","neversion"])
    df['enodebname'] = mm_enodename
    df['cellname'] = mm_cellname
    df['localcellid'] = mm_cellid
    df['enodebid'] = mm_enodebid
    df["freqband"] = mm_freqband
    df["ulearfcnffgind"] = mm_ulearfcnffgind
    df["dlearfnc"] = mm_dlearfnc
    df["ulbandwidth"] = mm_ulbandwidth
    df["dlbandwidth"] = mm_dlbandwidth
    df["cellactivestate"] = mm_cellactivestate
    df["celladminstate"] = mm_celladminstate
    df["userlabel"] = mm_userlabel
    df["datetime"] = mm_datetime
    df["neversion"] = mm_neversion
    df.to_csv("VFES_SRAN_CM_files/" + new_xml_file.rsplit(".")[-2] + ".csv", index=False)

    # df.to_csv("sample.csv",index=False)
    print("CSV file saved successfully!")

print('It took {0:0.1f} seconds'.format(time.time() - begin_time))
