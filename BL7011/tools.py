import json
import numpy as np
import h5py
import matplotlib.pyplot as plt
import math
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import warnings as w


def get_positions_from_bluesky_json(jsonfilename: str, motornames: list = []) -> dict:
    """
    When in the bluesky exporter None is selected it exports the collected
    detector data in an .h5 file while the recorded metadata from labview
    is written to a .json file. This function extracts the motor positions
    of a given motors for all included scans in the .json file.


    Parameters
    ----------
    jsonfilename : str
        Whole path of the .json-file exported by bluesky exporter.
    motornames : list
        Names of the motor mentioned in the .json as list.

    Returns
    -------
    positions : dict
        Motor positions of the requested motornames.
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

    # if no motornames are given, take all motors
    for n in range(len(data)):
        try:
            available_motornames = list(data[n][1]["data"].keys())
            break
        except:
            pass

    # get motors which are not in the list
    motors_not_in_list = [
        item for item in motornames if item not in available_motornames
    ]

    if motors_not_in_list or not motornames:
        motornames = available_motornames
        if motors_not_in_list:
            w.warn(
                f"The following motors are not in the list: {motors_not_in_list}. "
                f"Available motors are: {available_motornames}. "
                "Taking all available motors.",
                UserWarning,
            )

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


def h5tree(h5filename: str, return_paths: bool = False) -> None:
    """
    Prints the structure of an HDF5 file and the shape of the stored datasets.
    Optionally returns all possible paths as a list of strings.

    Parameters
    ----------
    h5filename : str
        Full path of the .h5 file.
    return_paths : bool, optional
        Whether to return the paths of all datasets and groups (default is False).

    Returns
    -------
    None or list of str
        Prints the structure of the HDF5 file. If return_paths is True, returns a list of paths.
    """

    paths = []

    def recursive_print(val, pre="", path=""):
        """
        Recursively prints the structure of an h5py.Group, showing hierarchy with ASCII art.
        Optionally collects all paths.

        Parameters
        ----------
        val : h5py.Group
            The h5py.Group object to be printed.
        pre : str
            The prefix used to format the output to show hierarchy.
        path : str
            The current path in the HDF5 file.
        """
        items = len(val)  # Number of items in the current group
        for key, item in val.items():
            is_last_item = items == 1  # Check if this is the last item in the group
            items -= 1  # Decrement the item count

            current_path = f"{path}/{key}" if path else key
            if return_paths:
                paths.append(current_path)

            if isinstance(item, h5py.Group):
                # Print the group name with appropriate formatting
                print(pre + ("└── " if is_last_item else "├── ") + key)
                # Recursively print the contents of the group
                recursive_print(
                    item, pre + ("    " if is_last_item else "│   "), current_path
                )
            else:
                # Determine the shape of the dataset, or mark it as "scalar" if it doesn't have a length
                item_shape = item.shape if hasattr(item, "__len__") else "scalar"
                # Print the dataset name with its shape and appropriate formatting
                print(
                    pre + ("└── " if is_last_item else "├── ") + f"{key} ({item_shape})"
                )

    # Open the HDF5 file in read mode
    with h5py.File(h5filename, "r") as hf:
        print(f"\nfilename: {h5filename}")  # Print the filename
        print(hf)  # Print the HDF5 file object
        recursive_print(hf)  # Print the structure of the HDF5 file

    if return_paths:

        def filter_final_paths(paths):
            """
            Filters out non-final paths from a list of HDF5 paths.

            Parameters
            ----------
            paths : list of str
                List of HDF5 paths.

            Returns
            -------
            list of str
                List of final paths.
            """
            # Sort the paths to ensure that parent paths come before child paths
            paths.sort()

            final_paths = []
            for i, path in enumerate(paths):
                # Check if the current path is the final path by comparing with the next path in the sorted list
                if i + 1 == len(paths) or not paths[i + 1].startswith(path + "/"):
                    final_paths.append(path)

            return final_paths

        paths = filter_final_paths(paths)
        paths = sorted(paths)

        return paths
