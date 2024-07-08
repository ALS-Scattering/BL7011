import json
import numpy as np 
import h5py

def get_positions_from_bluesky_json(jsonfilename:str, motornames:list) -> dict:
    """
    When in the bluesky exporter None is selected it exports the collected 
    detector data in an .h5 file while the recorded metadata from labview 
    is written to a .json file. This function extracts the motor positions
    of a given motors for all included scans in the .json file. 

    
    Parameters
    ----------
    jsonfilename : str
        whole path of the .json-file exported by bluesky exporter
    motornames : list
        names of the motor mentioned in the .json as list

    Returns
    -------
    positions : dict
        motor positions of the requested motornames
    """
    # Opening JSON file, Error handling will be done automatically when file not found
    f = open(jsonfilename)
    # returns JSON object as a dictionary
    data = json.load(f)
    # closing file
    f.close()
    # Iterating through the json
    # list

    if isinstance(motornames, str):
        motornames = [motornames]

    # create empty dict to catch the motor positions
    all_positions = {}

    for motorname in motornames:
        position_list = []
        if isinstance(data, list):
            # attache motor positions to the list
            for n in range(len(data)):
                try:
                    position_list.append(data[n][1]["data"][motorname][0])
                except:
                    pass
        else:
            raise SyntaxError("unknown format of .json file " + jsonfilename)
    
        # if no motor position was found, run through the file again and note down the available motors
        if len(position_list) == 0:
            for n in range(len(data)):
                try:
                    available_motors = list(data[n][1]["data"].keys())
                    break 
                except:
                    pass
            raise Warning(f"No motor positions found for {motorname}. Choose from the following: {available_motors}")
        # attach motor name and positions to the dict
        all_positions[motorname] = position_list
    # return motor positions as a numpy array
    return all_positions


def where_is_my_frame_missing(h5filename:str):
    
    """
    TODO - NOT FINISHED yet

    """
    f = h5py.File(h5filename, 'r+')
    scan_times = f["entry"]["instrument"]["NDAttributes"]["NDArrayTimeStamp"][:]
    f.close()
    frame_count = 1
    frame_count_list = []
    
    time_differences = []
    
    for i in range(len(scan_times)-1):
        time_difference = scan_times[i+1] - scan_times[i]
        time_differences.append(time_difference)
    
    min_time_difference = np.min(time_differences)
    max_time_difference = np.max(time_differences)
    #print(time_differences)
    for i in range(len(scan_times)-1):

        time_difference = scan_times[i+1] - scan_times[i]
        if time_difference < max_time_difference-min_time_difference:
            frame_count_list.append(frame_count)

            frame_count = 1

        else:

            frame_count += 1
            
    return np.argmin(np.array(frame_count_list))
