import json
import numpy as np 
import h5py
import matplotlib.pyplot as plt


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


def where_is_my_frame_missing(h5filename:str, plot=False):
    """
    When in the bluesky exporter None is selected it exports the collected 
    detector data in an .h5 file while the recorded metadata from labview 
    is written to a .json file. This function prints out where a missing frame
    can be inserted. Only works so far if only one frame is missing.

    
    Parameters
    ----------
    h5filename : str
        whole path of the .json-file exported by bluesky exporter
    plot : bool
        plots out the differences in timestamps to evaluate

    Returns
    -------
    here : int
        index where the frame is missing

    """
    # reading in the file and selecting the time stamps
    f = h5py.File(h5filename, 'r+')
    scan_times = f["entry"]["instrument"]["NDAttributes"]["NDArrayTimeStamp"][:]
    f.close()

    # taking the difference between the timestamps
    diff_scan_times = np.diff(scan_times)

    # plot if wanted
    if plot:
        plt.figure()
        plt.plot(diff_scan_times,marker="o")
        plt.show()

    # trying to find the time which is only once present
    # this will be the area where the frame is missing 
    # start with 2 decimal points 
    for n in reversed(range(0,2)):
        diff_scan_times = np.around(diff_scan_times, n)
        unique, counts = np.unique(diff_scan_times, return_counts=True)
        dict_uniqques = dict(zip(unique, counts))

        # checkout how many ones there are in dict_uniques
        ct_1 = 0
        for i in list(dict_uniqques.keys()):
            # increase counter when scan duration is only once in the list
            if dict_uniqques[i] == 1:
                ct_1 += 1 
                i_ = i 
        
        # save the value if only one one found and break the loop
        if ct_1 == 1:
            here = np.argwhere(diff_scan_times == i_)
            break
            
    return int(here.flatten())


def h5tree(h5filename : str) -> None:
    """
    Simple to print out the structure of a H5 file and the shape of the stored datasets.

    Parameters
    ----------
    h5filename : str
        Whole path of the .h5-file.


    Returns
    -------
    None , but prints the structure of the h5 file.
    """
    def recursive_print(val, pre=""):
        items = len(val)
        for key, item in val.items():
            is_last_item = items == 1
            items -= 1
            
            if isinstance(item, h5py.Group):
                print(pre + ('└── ' if is_last_item else '├── ') + key)
                recursive_print(item, pre + ('    ' if is_last_item else '│   '))
            else:
                item_shape = item.shape if hasattr(item, '__len__') else 'scalar'
                # print(item_shape)
                print(pre + ('└── ' if is_last_item else '├── ') + f"{key} ({item_shape})")

    with h5py.File(h5filename, 'r') as hf:
        print(hf)
        recursive_print(hf)
