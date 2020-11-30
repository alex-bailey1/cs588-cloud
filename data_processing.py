import csv
import json
from json import JSONEncoder
from datetime import datetime
from bson import json_util
import math
import numpy

class StationEncoder(JSONEncoder):
    def default(self, o):
        o.__dict__

class station:
    def __init__(self, stationid, highwayid, milepost, locationtext, upstream, downstream, stationsclass, numberlanes, latlon, length):
        self.stationid = stationid
        self.highwayid = highwayid
        self.milepost = milepost
        self.locationtext = locationtext
        self.upstream = upstream
        self.downstream = downstream
        self.stationsclass = stationsclass
        self.numberlanes = numberlanes
        self.latlon = latlon
        self.length = length
        # self.detectors = list()

    def stationid_print(self):
        print(self.stationid)

class time_item:
    def __init__(self, detectorid, startime, volume, speed, occupancy, status, dqflags):
        self.detectorid = detectorid
        self.startime = startime
        self.volume = volume
        self.speed = speed
        self.occupancy = occupancy
        self.status = status
        self.dqflags = dqflags

class detector:
    def __init__(self, detectorid, highwayid, milepost, locationtext, detectorclass, lanenumber, stationid):
        self.detectorid = detectorid
        self.highwayid = highwayid
        self.milepost = milepost
        self.locationtext = locationtext
        self.detectorclass = detectorclass
        self.lanenumber = lanenumber
        self.stationid = stationid
        self.time_items = list()


def make_detectors():

    detectors_list = list()

    with open("freeway_detectors.csv", newline='') as csvfile:
        detector_reader = csv.reader(csvfile, delimiter=",")

        first_row = True
        for row in detector_reader:
            if(first_row):
                first_row = False
            else:
                in_detectorid = int(row[0])
                in_highwayid = int(row[1])
                in_milepost = float(row[2])
                in_locationtext = row[3]
                in_detectorclass = int(row[4])
                in_lanenumber = int(row[5])
                in_stationid = int(row[6])

                detectors_list.append(detector(in_detectorid,in_highwayid, in_milepost, in_locationtext, in_detectorclass, in_lanenumber, in_stationid).__dict__)

    time_items_list = make_time_items()

    for item in detectors_list:
        print(item["detectorid"])
        for time_item in time_items_list:
            if(item["detectorid"] == time_item["detectorid"]):
                item["time_items"].append(time_item)

    return detectors_list


def make_time_items():
    time_items_list = list()
    time_format = '%Y-%m-%d %H:%M:%S'

    count = 0

    with open("freeway_loopdata.csv", newline='') as csvfile:
        time_item_reader = csv.reader(csvfile, delimiter=",")

        first_row = True
        for row in time_item_reader:
            count += 1
            if( (count % 100000) == 0):
                print(count)
                # break
            if(first_row):
                first_row = False
            else:

                
                in_detectorid = int(row[0])
                in_starttime = datetime.strptime(row[1][:-3], time_format)

                if(row[2]):
                   in_volume = int(row[2])
                else:
                    in_volume = None
                
                if(row[3]):
                    in_speed = int(row[3])
                else:
                    in_speed = None

                if(row[4]):
                    in_occupancy = int(row[4])
                else:
                    in_occupancy = None
                    
                if(row[5]):
                    in_status = int(row[5])                    
                else:
                    in_status = None

                if(row[6]):
                    in_dqflag = int(row[6])
                else:
                    in_dqflag = None

                time_items_list.append(time_item(in_detectorid, in_starttime, in_volume, in_speed, in_occupancy, in_status, in_dqflag).__dict__ )

    return time_items_list



def make_stations():
    stations_list = list()

    with open("freeway_stations.csv", newline='') as csvfile:
        station_reader = csv.reader(csvfile, delimiter=",")
        first_row = True

        for row in station_reader:
            if(first_row):
                first_row = False
            else:
                
                in_stationid = int(row[0])
                in_highwayid = int(row[1])
                in_milepost = float(row[2])
                in_locationtext = row[3]
                in_upstream = int(row[4])
                in_downstream = int(row[5])
                in_stationclass = int(row[6])
                in_numberlanes = int(row[7])
                in_latlon = row[8]
                in_length = float(row[9])

                stations_list.append(station(in_stationid, in_highwayid, in_milepost, in_locationtext, in_upstream, in_downstream, in_stationclass, in_numberlanes, in_latlon, in_length).__dict__)

    # detector_list = make_detectors()

    # for station_item in stations_list:
    #     print(station_item["stationid"])
    #     for detector_item in detector_list:
    #         if(station_item["stationid"] == detector_item["stationid"]):
    #             station_item["detectors"].append(detector_item)

    
    return stations_list


def output_json():
    # stations_list = make_stations()

    # # print(stations_list[0])

    # # json_dump = json.dumps(stations_list, indent=4, default=json_util.default)
    # i = 0
    # for station in stations_list:
    #     json_dump = json.dumps(station, indent=4, default=json_util.default)
    #     with open("json_outputs" + str(i) + ".json", "w") as outfile:
    #         outfile.write(json_dump)
    #     i +=1 


    detector_list = make_detectors()

    # detector_list = numpy.array(detector_list)

    # array_of_detect_list = numpy.array_split(detector_list, 10)

    # print("length of array_of_detect_list[0]: " + str(array_of_detect_list.shape))

    i = 0
    for detector in detector_list:
        new_detectors = list()
        time_item_list = numpy.copy(detector["time_items"])
        np_time_item_list = numpy.asarray(time_item_list)
        # print("total length: " + str(len(np_time_item_list)))
        t_i_split = numpy.array_split(np_time_item_list, 10)
        # print("shape of t_i_split: " + str(t_i_split.shape))
        # print(t_i_split[0])
        # print()
        # print()
        # print(t_i_split[1])

        # print(t_i_split[0] == t_i_split[1])
        # num = math.ceil(len(time_item_list)/10)
        # list0 = time_item_list[0:num]
        # list1 = time_item_list[num:num*2]
        # list2 = time_item_list[2*num:3*num]
        # list3 = time_item_list[3*num:4*num]
        # list4 = time_item_list[4*num:5*num]
        # list5 = time_item_list[5*num:6*num]
        # list6 = time_item_list[6*num:7*num]
        # list7 = time_item_list[7*num:8*num]
        # list8 = time_item_list[8*num:9*num]
        # list9 = time_item_list[9*num:]
        
        for j in range(0, 10):
            temp_detector = detector.copy()
            # print(temp_detector)
            # print("length of original: " + str(len(temp_detector["time_items"])))
            # print("length of insert: " + str(len(t_i_split[j].tolist())))
            temp_detector["time_items"] = t_i_split[j].tolist()
            # print("length after: " + str(len(temp_detector["time_items"])))
            # print(temp_detector)
            new_detectors.append(temp_detector)

        # temp_detector0 = detector
        # temp_detector0["time_item"] = list0
        # new_detectors.append(temp_detector0)

        # temp_detector1 = detector
        # temp_detector1["time_item"] = list1
        # new_detectors.append(temp_detector1)

        # temp_detector2 = detector
        # temp_detector2["time_item"] = list2
        # new_detectors.append(temp_detector2)

        # temp_detector3 = detector
        # temp_detector3["time_item"] = list3
        # new_detectors.append(temp_detector3)

        # temp_detector4 = detector
        # temp_detector4["time_item"] = list4
        # new_detectors.append(temp_detector4)

        # temp_detector5 = detector
        # temp_detector5["time_item"] = list5
        # new_detectors.append(temp_detector5)


        # temp_detector6 = detector
        # temp_detector6["time_item"] = list6
        # new_detectors.append(temp_detector6)

        # temp_detector7 = detector
        # temp_detector7["time_item"] = list7
        # new_detectors.append(temp_detector7)

        # temp_detector8 = detector
        # temp_detector8["time_item"] = list8
        # new_detectors.append(temp_detector8)

        # temp_detector9 = detector
        # temp_detector9["time_item"] = list9
        # new_detectors.append(temp_detector9)


        json_dump = json.dumps(new_detectors, indent=4, default=json_util.default)

        with open("detector_output" + str(i) + ".json", "w") as outfile:
            outfile.write(json_dump)

        i += 1


    # i = 0
    # for detector in detector_list:
    #     json_dump = json.dumps(detector, indent=4, default=json_util.default)

    #     with open("detector_output" + str(i) + ".json", "w") as outfile:
    #         outfile.write(json_dump)
        
    #     i += 1
    

#ouput stations to json, without detectors
def output_stations():
    stations_list = make_stations()
    
    json_dump = json.dumps(stations_list, indent=4, default=json_util.default)
    
    with open("station_outputs.json", "w") as outfile:
        outfile.write(json_dump)



# output_json()
output_stations()