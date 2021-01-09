import pandas as pd
import glob
import re

files = []

file_path = "/home/valiance/Desktop/Cardinality/Country Data/CM Data/VFES/4G/data/"

for xml in glob.glob(file_path + "*"):
    files.append(xml)

sortedFileNames = sorted(files, key=lambda x: x.rsplit('/')[-1].rsplit('_'))

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

for f in sortedFileNames:

    for xml_file in glob.glob(f):
        new = xml_file.replace("/home/valiance/Desktop/Cardinality/Country Data/CM Data/VFES/4G/data/", "")
        print(new)

        with open(xml_file, "r") as f:
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

                administrativestate = re.search("<es:administrativeState>(.*?)</es:administrativeState>", i, re.IGNORECASE)
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

                groupid = re.search("<es:physicalLayerCellIdGroup>(.*?)</es:physicalLayerCellIdGroup>", i, re.IGNORECASE)
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

df = pd.DataFrame.from_dict(d)
df.to_csv("cm_files/4G/4G_vsDataFDD.csv", index=False)










