from BL7011.import_functions import import_broken_h5
import pytest


def test_import_broken_h5():
    # Path to a sample HDF5 file with missing frames
    filename = "BL7011/test_data/missing_frames16x16.h5"

    # Test case 1: Function should return a numpy array with correct shape
    assert import_broken_h5(filename).shape == (961, 16, 16)

    # Test case 1: Function should return a numpy array with float data type
    assert import_broken_h5(filename).dtype == float

    # Test case 1: Function should return a numpy array with the correct size
    assert import_broken_h5(filename).size == 961 * 16 * 16

    # Test case 2: Function should return the correct data at specific position
    assert import_broken_h5(filename)[0, 0, 0] == pytest.approx(701.6)

    # Test case 2: Function should handle region of interest (ROI) and return correct shape
    roi = [0, 10, 0, 10]
    assert import_broken_h5(filename, roi=roi).shape == (961, 10, 10)

    # Test case 2: Function should handle missing frames without raising an error
    import_broken_h5(filename, missing_frames=[1, 2])

    # Test case 2: Function should raise a ValueError when an incorrect number of missing frames is provided
    with pytest.raises(ValueError):
        import_broken_h5(filename, missing_frames=[1, 2, 3])
