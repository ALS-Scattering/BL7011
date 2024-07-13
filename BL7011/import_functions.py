import numpy as np
import h5py
from .tools import where_is_my_frame_missing
import tqdm


def import_broken_h5(
    h5filename: str,
    average: int = 10,
    verbose: bool = False,
    roi: list = [0, 2048, 0, 2048],
    missing_frames: list = [],
    eps: float = 0.3,
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
        Averaging all X frames.
    verbose : bool
        Print detailed information if True.
    roi : list
        Region of interest in the format [start_row, end_row, start_col, end_col].
    missing_frames: list
        List of missing frames can be also provided manually. where_is_my_frame_missing() funtion will be skipped.
    eps: float
        Value for the eps to pass the where_is_my_frame_missing() function.
    Returns
    -------
    data : np.array
        Data as np.array.
    """

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

    if average == 0:
        raise ValueError("average can not be zero")

    if verbose:
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
    f.close()
    n_recorded_frames = len(for_recorded_frames)
    intended_n_frames = n_recorded_frames + n_missing_frames

    # Initialize variables for averaging process
    averages_list = []
    already_replaced = 0
    correction_in_round = 0

    # Determine how many frames to correct in each round
    to_correct = np.floor(missing_frames / average)
    unique, counts = np.unique(to_correct, return_counts=True)
    to_correct = dict(zip(unique, counts))

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
        # Averaging the data frames
        temp_data = np.mean(temp_data, axis=0)
        averages_list.append(temp_data)

        if correction_in_round != 0:
            already_replaced += correction_in_round
        # Reset the correction counter in the round
        correction_in_round = 0

    # Check if the number of replaced frames matches the missing frames
    if already_replaced != n_missing_frames:
        raise ValueError("number of missing frames does not match the replacement")

    if verbose:
        print("converted and averaged")

    # Return the averaged data as a numpy array
    return np.array(averages_list)
