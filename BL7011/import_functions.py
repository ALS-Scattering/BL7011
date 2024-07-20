import numpy as np
import h5py
from BL7011.tools import where_is_my_frame_missing
import tqdm
import matplotlib.pyplot as plt
import warnings as w


def import_broken_h5(
    h5filename: str,
    average: int = 10,
    verbose: bool = False,
    roi: list = [0, 2048, 0, 2048],
    missing_frames: list = [],
    eps: float = 0.3,
    for_roi: bool = False,
    save_to_h5: bool = False,
) -> np.array:
    """
    When in the bluesky exporter None is selected it exports the collected
    detector data in an .h5 file while the recorded metadata from labview
    is written to a .json file. This function returns the averaged data of the
    detectors.

    Parameters
    ----------
    h5filename : str
        Whole path of the .h5-file exported by bluesky exporter.
    average : int
        Averaging all X frames. Default is 10. If 1 is passed, no averaging will be done, and the false dataframes will
        be replaced by zeros.
    verbose : bool
        Print detailed information if True.
    roi : list
        Region of interest in the format [start_row, end_row, start_col, end_col].
    missing_frames: list
        List of missing frames can be also provided manually. where_is_my_frame_missing() funtion will be skipped.
    eps: float
        Value for the eps to pass the where_is_my_frame_missing() function.
    for_roi : bool
        Will only important a single frame to plot. Takes frame number as an argument as well.
    save_to_h5 : bool
        Will save to h5 file, if string is passed it will use it as filename.


    Returns
    -------
    data : np.array
        Data as np.array.
    """
    # Plot function to determine the roi while importing and averging.
    if for_roi:
        if isinstance(for_roi, bool):
            for_roi = 0
        f = h5py.File(h5filename, "r")
        data = np.array(f["entry"]["data"]["data"][for_roi, :, :])
        f.close()
        plt.figure()
        plt.imshow(data)
        return plt.show()

    if average == 0:
        raise ValueError("average can not be zero")

    if len(missing_frames) == 0:
        # Find missing frames in the data
        missing_frames = where_is_my_frame_missing(
            h5filename, plot=False, n_images=average, eps=eps
        )
    else:
        missing_frames = np.array(missing_frames)
    n_missing_frames = len(missing_frames)

    if verbose:
        print(f"{n_missing_frames} frames missing @  {missing_frames}")
        print("start reading and averaging ", h5filename)

    # function to load in the frames
    def load_frames(frame_min, frame_max):
        # Load frames from the h5 file within the specified range and ROI
        f = h5py.File(h5filename, "r")
        data = np.array(
            f["entry"]["data"]["data"][
                frame_min:frame_max, roi[0] : roi[1], roi[2] : roi[3]
            ]
        )
        f.close()
        return data

    # Open the h5 file to determine the number of recorded frames
    f = h5py.File(h5filename, "r")
    for_recorded_frames = np.array(f["entry"]["data"]["data"][:, :1, :1])
    actual_frame_size = np.array(f["entry"]["data"]["data"][0, :, :]).shape
    f.close()

    # Adjust the roi if actual frame size is smaller than the provided roi and warn the user
    if actual_frame_size[0] < roi[1] - roi[0]:
        roi[1] = actual_frame_size[0]
        roi[0] = 0
        w.warn(
            f"roi[0] and roi[1] adjusted to the actual frame size {actual_frame_size[0]} from the h5 file."
        )
    if actual_frame_size[1] < roi[3] - roi[2]:
        roi[3] = actual_frame_size[1]
        roi[2] = 0
        w.warn(
            f"roi[2] and roi[3] adjusted to the actual frame size {actual_frame_size[1]} from the h5 file."
        )

    # estimating the number of frames
    n_recorded_frames = len(for_recorded_frames)
    intended_n_frames = n_recorded_frames + n_missing_frames

    if verbose:
        print(f"n_recorded_frames: {n_recorded_frames}")
        print(f"intended_n_frames: {intended_n_frames}")

    # check if the number of recorded and expected frames match and if it aligns
    # with the number of provided frames as well
    if average != 1:
        guessed_n_frames_missing = average - n_recorded_frames % average
        if guessed_n_frames_missing != n_missing_frames:
            raise ValueError(
                f"{guessed_n_frames_missing} frames missing, but {n_missing_frames} frames provided"
                + "number of recorded frames does not match the expected number of frames minus the missing frames"
            )

    # Initialize variables for averaging process
    averages_list = []
    already_replaced, correction_in_round = 0, 0

    # Determine how many frames to correct in each round
    to_correct = np.floor(missing_frames / average)
    unique, counts = np.unique(to_correct, return_counts=True)
    to_correct = dict(zip(unique, counts))

    if average == 1:
        # Loop over the frames and perform averaging
        for n in tqdm.tqdm(range(0, n_recorded_frames)):
            if n in to_correct.keys():
                averages_list.append(np.zeros((roi[1] - roi[0], roi[3] - roi[2])))
                already_replaced += 1
                if verbose:
                    print(
                        f"correction zero shape: {np.zeros((roi[1] - roi[0], roi[3] - roi[2])).shape}"
                    )
            else:
                temp_data = load_frames(
                    frame_min=n * average,
                    frame_max=((n + 1) * average),
                )
                if np.isnan(temp_data).any():
                    w.warn(f"NaN values in the data at frame {n}")
                averages_list.append(np.array(temp_data).squeeze())
        if verbose:
            print(f"shape of the data: {np.array(averages_list[-1]).shape}")
    else:
        # Loop over the frames and perform averaging
        for n in tqdm.tqdm(range(0, intended_n_frames // average)):
            if n in to_correct.keys():
                correction_in_round = to_correct[n]
                if verbose:
                    print(f"corrections in round {correction_in_round}")

            temp_data = load_frames(
                frame_min=n * average - already_replaced,
                frame_max=((n + 1) * average - already_replaced - correction_in_round),
            )

            if np.isnan(temp_data).any():
                w.warn(f"NaN values in the data at frame {n}")

            # Averaging the data frames
            temp_data = np.mean(temp_data, axis=0)
            averages_list.append(temp_data)

            if correction_in_round != 0:
                already_replaced += correction_in_round
            # Reset the correction counter in the round
            correction_in_round = 0

    # Convert list to np.array.
    averages = np.array(averages_list)

    # Save to h5 if wanted
    if save_to_h5:
        # Manipulate the filenames
        if isinstance(save_to_h5, str):
            save_to_filename = save_to_h5
        else:
            cleaned_h5filename = h5filename.replace(".h5", "")
            save_to_filename = cleaned_h5filename + "_averages.h5"

        output_h5file = h5py.File(save_to_filename, "w")
        output_h5file.create_dataset("data", data=averages)
        output_h5file.close()

    # Check if the number of replaced frames matches the missing frames
    if already_replaced != n_missing_frames:
        raise ValueError("number of missing frames does not match the replacement")

    if verbose:
        print("converted and averaged")

    # Return the averaged data
    return averages
