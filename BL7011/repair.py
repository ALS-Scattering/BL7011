from BL7011.import_functions import import_broken_h5
from BL7011.tools import get_positions_from_bluesky_json
from warnings import warn as w
import h5py
import numpy as np


def uncorrupted_h5_structure() -> list:
    """
    This function returns the structure of the uncorrupted h5 file.

    Returns
    -------
    structure : list
        List of the structure of the uncorrupted h5 file.
    """
    return [
        "entry1/end_time",
        "entry1/instrument_1/detector_1/count_time",
        "entry1/instrument_1/detector_1/data",
        "entry1/instrument_1/detector_1/description",
        "entry1/instrument_1/detector_1/detector_readout_time",
        "entry1/instrument_1/detector_1/distance",
        "entry1/instrument_1/detector_1/exposures",
        "entry1/instrument_1/detector_1/period",
        "entry1/instrument_1/detector_1/x_pixel_size",
        "entry1/instrument_1/detector_1/y_pixel_size",
        "entry1/instrument_1/labview_data/DIAG112_Diode_diode",
        "entry1/instrument_1/labview_data/DetectorDiodeCurrent_diode",
        "entry1/instrument_1/labview_data/EPUPOL_diode",
        "entry1/instrument_1/labview_data/EPU_Polarization",
        "entry1/instrument_1/labview_data/EPU_Polarization_user_setpoint",
        "entry1/instrument_1/labview_data/LS_LLHTA",
        "entry1/instrument_1/labview_data/LS_LLHTA_user_setpoint",
        "entry1/instrument_1/labview_data/LS_LLHTB",
        "entry1/instrument_1/labview_data/LS_LLHTB_user_setpoint",
        "entry1/instrument_1/labview_data/XS111LeftBladecurrent_diode",
        "entry1/instrument_1/labview_data/XS111RLRL_diode",
        "entry1/instrument_1/labview_data/XS111RightBladecurrent_diode",
        "entry1/instrument_1/labview_data/beamline_energy",
        "entry1/instrument_1/labview_data/beamline_energy_user_setpoint",
        "entry1/instrument_1/labview_data/det_translate",
        "entry1/instrument_1/labview_data/det_translate_user_setpoint",
        "entry1/instrument_1/labview_data/detector_rotate",
        "entry1/instrument_1/labview_data/detector_rotate_user_setpoint",
        "entry1/instrument_1/labview_data/diagnostic",
        "entry1/instrument_1/labview_data/diagnostic_user_setpoint",
        "entry1/instrument_1/labview_data/fake",
        "entry1/instrument_1/labview_data/fake_user_setpoint",
        "entry1/instrument_1/labview_data/pinhole_x",
        "entry1/instrument_1/labview_data/pinhole_x_user_setpoint",
        "entry1/instrument_1/labview_data/pinhole_y",
        "entry1/instrument_1/labview_data/pinhole_y_user_setpoint",
        "entry1/instrument_1/labview_data/sample_lift",
        "entry1/instrument_1/labview_data/sample_lift_user_setpoint",
        "entry1/instrument_1/labview_data/sample_rotate_steppertheta",
        "entry1/instrument_1/labview_data/sample_rotate_steppertheta_user_setpoint",
        "entry1/instrument_1/labview_data/sample_top",
        "entry1/instrument_1/labview_data/sample_top_user_setpoint",
        "entry1/instrument_1/labview_data/sample_translate",
        "entry1/instrument_1/labview_data/sample_translate_user_setpoint",
        "entry1/instrument_1/labview_data/sample_vertical_rotation",
        "entry1/instrument_1/labview_data/sample_vertical_rotation_user_setpoint",
        "entry1/instrument_1/labview_data/sample_vertical_translate",
        "entry1/instrument_1/labview_data/sample_vertical_translate_user_setpoint",
        "entry1/instrument_1/labview_data/sample_wedge",
        "entry1/instrument_1/labview_data/sample_wedge_user_setpoint",
        "entry1/instrument_1/labview_data/slit_bottom",
        "entry1/instrument_1/labview_data/slit_bottom_user_setpoint",
        "entry1/instrument_1/labview_data/slit_left",
        "entry1/instrument_1/labview_data/slit_left_user_setpoint",
        "entry1/instrument_1/labview_data/slit_right",
        "entry1/instrument_1/labview_data/slit_right_user_setpoint",
        "entry1/instrument_1/labview_data/slit_top",
        "entry1/instrument_1/labview_data/slit_top_user_setpoint",
        "entry1/instrument_1/labview_data/theta2thetaboth",
        "entry1/instrument_1/labview_data/theta2thetaboth_user_setpoint",
        "entry1/instrument_1/name",
        "entry1/instrument_1/source_1/energy",
        "entry1/instrument_1/source_1/name",
        "entry1/instrument_1/source_1/wavelength",
        "entry1/run_id",
        "entry1/sample_1/geometry_1",
        "entry1/sample_1/name",
        "entry1/start_time",
    ]


def h5repair(
    h5filename: str,
    jsonfilename: str = "",
    outputfilename: str = "",
    average: int = 10,
    verbose: bool = False,
    roi: list = [0, 2048, 0, 2048],
    missing_frames: list = [],
    eps: float = 0.3,
) -> None:
    """
    When in the bluesky exporter None is selected it exports the collected detector data in an .h5 file while the
    recorded metadata from labview is written to a .json file. This function returns the averaged data of the detectors
    and the labview data from the json file and writes a new h5 file in the the style of the uncorrupted
    Nexus files.
    """

    # Import the data and average it accordingly
    h5data = import_broken_h5(h5filename, average, verbose, roi, missing_frames, eps)

    if verbose:
        print(h5data.shape)

    # get all the motor positions and save them into a dict
    if jsonfilename != "":
        labview_data = get_positions_from_bluesky_json(jsonfilename)
    else:
        try:
            # try to match the json file to the h5 file
            jsonfilename = h5filename.replace("_0.h5", "_documents.json")
            labview_data = get_positions_from_bluesky_json(jsonfilename)
        except:
            raise ValueError("No json file found")

    for n in labview_data.keys():
        if not len(labview_data[n]) == h5data.shape[0]:
            w(
                f"Length of motor positions {n} does not match the length of the data. "
                f"Motor positions: {len(labview_data[n])}, Data: {h5data.shape[0]}."
            )
    # match names from the labview data with the file path structure of the uncorrupted h5 files
    labview_data_keys = list(labview_data.keys())

    # Creating a dictionary to store matches
    matches = {key: None for key in labview_data_keys}

    # Matching elements
    for element in labview_data_keys:
        for item in uncorrupted_h5_structure():
            if item.endswith(element):
                matches[element] = item
                break

    # Printing the matches
    if verbose:
        for key, value in matches.items():
            print(f"{key}: {value}")

    # Writing the new h5 file
    if outputfilename == "":
        outputfilename = h5filename.replace(".h5", "_repaired.h5")

    with h5py.File(outputfilename, "w") as f:
        for key in matches.keys():
            if matches[key] is not None:
                path = matches[key]
                # Create groups and datasets according to the path structure
                parts = path.split("/")
                group = f
                for part in parts[:-1]:
                    if part not in group:
                        group = group.create_group(part)
                    else:
                        group = group[part]

                # Create a dataset at the final location (using some example data)
                dataset_name = parts[-1]
                # Example data: could be random or specific values
                data = labview_data[key]
                group.create_dataset(dataset_name, data=data)
            else:
                # for the None values create a new group
                group = f
                group.create_dataset(key, data=labview_data[key])
        if verbose:
            print(f"New h5 file written to {outputfilename}")

        # Now add the data from the detector add to "entry1/instrument_1/detector_1/data"
        group = f
        group = group["entry1"]
        group = group["instrument_1"]
        group.create_group("detector_1")
        group = group["detector_1"]

        # Save data as displayed into the uncorrupted h5 files as (a, 1, b, c)
        h5data = np.expand_dims(h5data, axis=1)
        group.create_dataset("data", data=h5data)

    return None
