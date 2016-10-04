# Author- Puneet Trivedi
# Date- 06/24/2016
# Description- Candidate Quiz 01 code


import urllib.request, json ,re,csv
url = "http://vw-test.elasticbeanstalk.com/test"
response = urllib.request.urlopen(url)
data = json.loads(response.read().decode('utf-8')) # took the data from the url and converted into the json format
# loaded the json formatted data
my_data=(data["orders"])
result_dict={}
spot_length_list=[15,30,60]
weekDayList=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
for dict in my_data:
    if not isinstance(dict["order_id"],int):
        result_dict[dict["order_id"]]="Order Id is not integer"    # this will tell the format of order_id
        continue
    if not re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d+\.\d{3}Z)',dict["flight_start"]):  # regex for iso 8601 date
        result_dict[dict["order_id"]]="Flight start date is not in ISO8601 format" # this will tell the format of date
        continue
    if not re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d+\.\d{3}Z)',dict["flight_end"]):
        result_dict[dict["order_id"]]="Flight end date is not in ISO8601 format" # same date format check
        continue
    if not (isinstance((dict["spots"][0]["spot_id"]),int) and ((dict["spots"][0]["spot_length"]==15)
            or (dict["spots"][0]["spot_length"]==30)
            or (dict["spots"][0]["spot_length"]==60))):
        result_dict[dict["order_id"]]="Spot id is not integer or invalid value for length"
        continue  # checks the spot_id and length, will give error if invalid
    if "constraints" in dict:
        if "forbid" in dict["constraints"]:
            for netList in dict["constraints"]["forbid"]:
                if "network" in netList:
                    if not isinstance(netList["network"],str):
                        result_dict[dict["order_id"]]="Network is not string"
                        break
                if "hours" in netList:
                    for hourList in netList["hours"]:
                        if not (isinstance(hourList,int) and (hourList>=0 and hourList<24)):
                         result_dict[dict["order_id"]]="Wrong range for hours"
                         break  # if condition checks if the hours in between 0 to 23
                if "days_of_week" in netList:
                    if (len(netList["days_of_week"])<1 or len(netList["days_of_week"])>7):
                         result_dict[dict["order_id"]]="Week array is no between 1-7"
                         break  # if condition checks the number of arrays in list is between 1-7
                    for weekList in netList["days_of_week"]:

                        if not (weekList in weekDayList and isinstance(weekList,str)):
                           result_dict[dict["order_id"]]="Wrong weekday value format"
                           break

        if "allocation" in dict["constraints"]:

            for allocationList in dict["constraints"]["allocation"]:
                if "hours" in allocationList:
                        for hourList in allocationList["hours"]:
                            if not (isinstance(hourList,int) and (hourList>=0 and hourList<24)):
                             result_dict[dict["order_id"]]="Wrong range for hours"
                             break
                if "impressions" in allocationList:

                    if "min" in allocationList["impressions"]:
                        if not (allocationList["impressions"]["min"]>=0 and allocationList["impressions"]["min"]<=1):
                            result_dict[dict["order_id"]]="Impression mimimum value not in between 0.0-1.0"
                            break  # defined condition of minimum value
                    if "max" in allocationList["impressions"]:
                            if not (allocationList["impressions"]["max"]>=0 and allocationList["impressions"]["max"]<=1):
                                result_dict[dict["order_id"]]="Impression maximum value not in between 0.0-1.0"
                                break # defined condition of maximum value
                if "days_of_week" in allocationList:
                    if (len(allocationList["days_of_week"])<1 or len(allocationList["days_of_week"])>7):
                             result_dict[dict["order_id"]]="Week array is no between 1-7"
                             break
                    for weekList in allocationList["days_of_week"]:
                            if not (weekList in weekDayList and isinstance(weekList,str)):
                               result_dict[dict["order_id"]]="Wrong weekday value format"

                               break

                if "budget" in allocationList:
                    if "min" in allocationList["budget"]:
                        if not (allocationList["budget"]["min"]>=0 and allocationList["budget"]["min"]<=10):
                            result_dict[dict["order_id"]]="Budget mimimum value not in 0-10"
                            break  # defined a condition of minimum budget
                    if "max" in allocationList["budget"]:
                            if not (allocationList["budget"]["max"]>=0 and allocationList["budget"]["max"]<=10):
                                result_dict[dict["order_id"]]="Budget maximum value not in between 0-10"
                                break  # defined a condition of maximum budget

                if "spot_length" in allocationList:
                    if not (isinstance(allocationList["spot_length"],int) and (allocationList["spot_length"] in spot_length_list)):
                        result_dict[dict["order_id"]]="Invalid value for spot length"
                        break    # checks the spot length to validate, i.e. 15,30,60

print(result_dict)
with open('Puneet_ans.csv','w',newline='') as csvfile:
    writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
    writer.writerow(['order_id','Error'])
    for key, value in result_dict.items():
        writer.writerow([key, value])






