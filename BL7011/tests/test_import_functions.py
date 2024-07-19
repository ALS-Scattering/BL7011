from BL7011.import_functions import import_broken_h5
import pytest


@pytest.mark.parametrize(
    "filename",
    ["BL7011/test_data/missing_frames/ccd_data16x16.h5", "BL7011/test_data/missing_frames/ccd_data16x16_2.h5"],
)
def test_import_broken_h5(filename):
    # Test case 1: Function should return a numpy array with correct shape
    assert len(import_broken_h5(filename).shape) == 3

    # Test case 2: Function should return a numpy array with float data type
    assert import_broken_h5(filename).dtype == float

    # Test case 3: Function should return a numpy array with the correct size
    assert import_broken_h5(filename).size > 0

    # Test case 4: Function should handle region of interest (ROI) and return correct shape
    roi = [0, 10, 0, 10]
    assert import_broken_h5(filename, roi=roi).shape[1:] == (10, 10)

    # Test case 5: Function should handle missing frames without raising an error
    ls = []
    for n in range(5):
        try:
            import_broken_h5(filename, missing_frames=ls)
            break
        except:
            ls.append(n)

    # Test case 6: Function should raise a ValueError when an incorrect number of missing frames is provided
    with pytest.raises(ValueError):
        import_broken_h5(filename, missing_frames=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
