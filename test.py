import urllib
import json
import os


url = 'http://vw-test.elasticbeanstalk.com/test'
json_obj = urllib.request.urlopen(url).read().decode('UTF-8')
data = json.loads(json_obj)
file = open(os.path.expanduser(r"C:\Utkarsh\Puneeth\Results.csv"), "wb")#INSERT RESULT PATH
file.write(b"OrderId,Flight_Start,Flight_end,Spot_Length,SpotId,Network,Forbid_hours,Forbid_daysofweek,Allocation_hours,Impressions_min,Impressions_max,Allocation_dayofweek,Budget_min,Budget_max,Allocation_spot_length" + b"\n")
for i in data["orders"]:
    order = i["order_id"]
    fstart = i["flight_start"]
    fend = i["flight_end"]
    spots = i ['spots']
    for  value in spots:    
        slen = value["spot_length"]
        sid = value["spot_id"]
    const = i["constraints"]
    fbd = const["forbid"]
    d = fbd
    network = [d["network"] for d in fbd if "network" in d]
    fhours = [d["hours"] for d in fbd  if "hours" in d]
    fdays = [d["days_of_week"] for d in fbd  if "days_of_week" in d]
    aln = const["allocation"]
    h = aln
    imp = [h["impressions"] for h in aln if "impressions" in h]
    imp_m =imp
    imp_mi = [imp_m["min"] for imp_m in imp if "min" in imp_m]
    imp_ma = [imp_m["max"] for imp_m in imp if "max" in imp_m]
    bgt = [h["budget"] for h in aln if "budget" in h]
    bgt_m  = bgt
    bgt_mi = [bgt_m["min"] for bgt_m in bgt if "min" in bgt_m]
    bgt_ma = [bgt_m["max"] for bgt_m in bgt if "max" in bgt_m]
    ahours = [h["hours"] for h in aln  if "hours" in h]
    adays = [h["days_of_week"] for h in aln  if "days_of_week" in h]
    aslen = [h["spot_length"] for h in aln  if "spot_length" in h]

    CombinedString = str(order) + "," + str(fstart) + "," + str(fend) + "," + str(slen) + "," + str(sid) + "," + str(network).replace(',','') + "," + str(fhours).replace(',','') + "," + str(fdays).replace(',','') + "," + str(ahours).replace(',','') + "," + str(imp_mi).replace(',','') + "," + str(imp_ma).replace(',','') + "," + str(adays).replace(',','') + "," + str(bgt_mi).replace(',','') + "," + str(bgt_ma).replace(',','') + "," + str(aslen).replace(',','') + '\n'
    file.write(bytes(CombinedString, encoding="ascii", errors='ignore'))
    print(CombinedString)

file.close()