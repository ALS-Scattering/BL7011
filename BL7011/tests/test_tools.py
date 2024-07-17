from BL7011.tools import (
    get_positions_from_bluesky_json,
    where_is_my_frame_missing,
    h5tree,
)
import numpy as np
import pytest


def test_get_positions_from_bluesky_json():
    # Path to a sample JSON file exported by Bluesky
    filename = "BL7011/test_data/bluesky_export.json"

    # Test case 1: Single motor name in a list
    assert get_positions_from_bluesky_json(filename, ["sample_lift"])

    # Test case 2: Multiple motor names in a list
    assert get_positions_from_bluesky_json(
        filename, ["sample_lift", "sample_translate"]
    )

    # Test case 3: Single motor name as a string
    assert get_positions_from_bluesky_json(filename, "sample_lift")

    # Test case 4: Motor name that doesn't exist should raise a Warning
    with pytest.raises(Warning):
        get_positions_from_bluesky_json(filename, "false_motor")


def test_where_is_my_frame_missing():
    # Path to a sample HDF5 file with missing frames
    filename = "BL7011/test_data/missing_frames16x16.h5"

    # Test case 1: Function should return a numpy array when plot=False
    assert isinstance(where_is_my_frame_missing(filename, plot=False), np.ndarray)

    # Test case 2: Length of the returned array should be 2
    assert len(where_is_my_frame_missing(filename)) == 2

    # Test case 3: The returned array should contain the specific missing frame numbers
    assert (where_is_my_frame_missing(filename) == np.array([2338, 4647])).all()

    # Test case 4: Function should return the correct missing frame numbers when plot=False
    assert (
        where_is_my_frame_missing(filename, plot=False) == np.array([2338, 4647])
    ).all()


def test_h5tree():
    # Path to a sample HDF5 file
    filename = "BL7011/test_data/missing_frames16x16.h5"

    # Test case: Function should return None
    assert h5tree(filename) is None
