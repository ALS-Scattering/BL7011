from BL7011.tools import (
    get_positions_from_bluesky_json,
    where_is_my_frame_missing,
    h5tree,
)
import numpy as np
import pytest


labview_files = [
    "BL7011/test_data/missing_frames/labview.json",
    "BL7011/test_data/missing_frames/labview_2.json",
]
ccd_data_files = [
    "BL7011/test_data/missing_frames/ccd_data16x16.h5",
    "BL7011/test_data/missing_frames/ccd_data16x16_2.h5",
]

# adding the uncorrupted file to the test the h5tree function
all_h5_files = ccd_data_files + ["BL7011/test_data/uncorrupted_frames/nexus16x16.h5"]


@pytest.mark.parametrize("filename", labview_files)
def test_get_positions_from_bluesky_json(filename):
    # Test case: Single motor name in a list
    assert get_positions_from_bluesky_json(filename, ["sample_lift"])

    # Test case: Multiple motor names in a list
    assert get_positions_from_bluesky_json(
        filename, ["sample_lift", "sample_translate"]
    )

    # Test case: Single motor name as a string
    assert get_positions_from_bluesky_json(filename, "sample_lift")

    # Test case: Motor name that doesn't exist should raise a Warning and return dict with all motors instead
    with pytest.warns(UserWarning):
        assert len(get_positions_from_bluesky_json(filename, "false_motor").keys()) > 0
        assert (
            len(get_positions_from_bluesky_json(filename, ["false_motor"]).keys()) > 0
        )

    # Test case 5: Motor name that doesn't exist should use all motors
    assert get_positions_from_bluesky_json(filename)


@pytest.mark.parametrize("filename", ccd_data_files)
def test_where_is_my_frame_missing(filename):
    # Test case: Function should return a numpy array with size > 0
    assert where_is_my_frame_missing(filename).size > 0

    # Test case: Function should return a numpy array when plot=False
    assert isinstance(where_is_my_frame_missing(filename, plot=False), np.ndarray)

    # Test case: Function should return 1D numpy array
    assert len(where_is_my_frame_missing(filename, plot=False).shape) == 1


@pytest.mark.parametrize("filename", all_h5_files)
def test_h5tree(filename):
    # Test case: Function should return None when return_paths is False
    assert h5tree(filename) is None

    # Test case: Function should return a list when return_paths is True
    assert isinstance(h5tree(filename, return_paths=True), list)

    # Test case: Function should return a list with length > 0
    assert len(h5tree(filename, return_paths=True)) > 0

    # Test case: Test if the returned list contains only strings
    assert all(isinstance(path, str) for path in h5tree(filename, return_paths=True))
