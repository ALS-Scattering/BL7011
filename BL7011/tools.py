import json
import numpy as np
import h5py
import matplotlib.pyplot as plt
import math
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


def get_positions_from_bluesky_json(jsonfilename: str, motornames: list) -> dict:
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
            raise Warning(
                f"No motor positions found for {motorname}. Choose from the following: {available_motors}"
            )
        # attach motor name and positions to the dict
        all_positions[motorname] = position_list
    # return motor positions as a numpy array
    return all_positions


def where_is_my_frame_missing(
    h5filename: str, plot=False, n_images=10, eps=0.3, min_samples=10
) -> np.array:
    """
    When in the bluesky exporter None is selected it exports the collected
    detector data in an .h5 file while the recorded metadata from labview
    is written to a .json file. This function prints out where a missing frame
    can be inserted. The algorithm is using the DBSCAN module from sklearn to group
    the timestamp differences.


    Parameters
    ----------
    h5filename : str
        Whole path and name of the .json-file exported by bluesky exporter.
    plot : bool
        Plots out the differences in timestamps to evaluate.
    images : int
        Number of images per motor position.
    eps : float
        eps value to pass to the dbscan algorithm.

    Returns
    -------
    outliers : np.array
        Indexes where the frames are missing.

    """
    # reading in the file and selecting the time stamps
    f = h5py.File(h5filename, "r")
    scan_times = f["entry"]["instrument"]["NDAttributes"]["NDArrayTimeStamp"][:]
    f.close()

    # calculating how many images are missing. only works if less images are missing
    n_recorded = len(scan_times)
    n_missing = math.ceil(n_recorded / n_images) * n_images - n_recorded
    # taking the difference between the timestamps
    diff_scan_times = np.diff(scan_times)

    X = diff_scan_times.reshape(-1, 1)
    # Standardize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Define the DBSCAN model
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    # Fit the model to the data
    dbscan.fit(X_scaled)

    # Get the cluster labels (-1 represents outliers)
    labels = dbscan.labels_

    # Extract the indices of the outliers
    outliers = np.where(labels == -1)[0]

    # Get the outlier values
    outlier_values = diff_scan_times[outliers]
    n_outlier_values = len(outlier_values)

    # plot if wanted and highlight the outliers
    if plot:
        plt.figure()
        plt.scatter(
            range(len(diff_scan_times)), diff_scan_times, c="blue", label="Data points"
        )
        plt.scatter(outliers, outlier_values, c="red", label="Outliers")
        plt.title("Timestamp Differences with Outliers")
        plt.xlabel("Index")
        plt.ylabel("Timestamp Difference (seconds)")
        plt.legend()
        plt.show()

    if n_outlier_values != n_missing:
        raise ValueError(
            "Number of outlier values does not fit the missing expected number of frames. Try to adjust \
                         eps value."
        )

    # return the outlier indices
    return outliers


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
