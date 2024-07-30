from BL7011.import_functions import import_broken_h5
import pytest


@pytest.mark.parametrize(
    "filename, average",
    [
        ("BL7011/test_data/missing_frames/ccd_data16x16.h5", 10),
        ("BL7011/test_data/missing_frames/ccd_data16x16_2.h5", 1),
    ],
)
def test_import_broken_h5(filename, average):

    with pytest.warns(UserWarning):
        # USER WARNING: when the chose roi was larger than the data shape
        roi = [0, 2048, 0, 2048]  # default roi
        # Test case: Function should return a numpy array with correct shape
        assert len(import_broken_h5(filename, average=average, roi=roi).shape) == 3

        # Test case: Function should return a numpy array with float data type
        assert import_broken_h5(filename, average=average, roi=roi).dtype == float

        # Test case: Function should return a numpy array with the correct size
        assert import_broken_h5(filename, average=average, roi=roi).size > 0

        # Test case: If average 1 is provided the missing frame shoulde be replaced by zeros
        assert (
            len(
                import_broken_h5(
                    filename, average=average, roi=roi, verbose=False
                ).shape
            )
            == 3
        )

        # Test case: Function should handle missing frames without raising an error
        ls = []
        for n in range(5):
            try:
                import_broken_h5(filename, average=average, missing_frames=ls)
                break
            except:
                ls.append(n)

    # Test case: Function should raise a ValueError when an incorrect number of missing frames is provided
    with pytest.raises(ValueError):
        import_broken_h5(filename, missing_frames=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    # Test case: If average is 0, function should raise a ValueError
    with pytest.raises(ValueError):
        import_broken_h5(filename, average=0)

    # Test case: Function should handle region of interest (ROI) and return correct shape
    roi = [0, 10, 0, 10]
    assert import_broken_h5(filename, average=average, roi=roi).shape[1:] == (10, 10)
