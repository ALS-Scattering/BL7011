from BL7011.repair import h5repair
import pytest


@pytest.mark.parametrize(
    "filename_h5, filename_json, average, roi",
    [
        (
            "BL7011/test_data/missing_frames/ccd_data16x16.h5",
            "BL7011/test_data/missing_frames/labview.json",
            10,
            [0, 10, 0, 10],
        ),
        (
            "BL7011/test_data/missing_frames/ccd_data16x16_2.h5",
            "BL7011/test_data/missing_frames/labview_2.json",
            1,
            [0, 10, 0, 10],
        ),
    ],
)
def test_h5repair(filename_h5, filename_json, average, roi):
    assert (
        h5repair(
            filename_h5,
            jsonfilename=filename_json,
            roi=roi,
            average=average,
            verbose=True,
        )
        is None
    )


def test_h5repair_displays_warning():
    with pytest.warns(UserWarning):
        assert (
            h5repair(
                "BL7011/test_data/missing_frames/ccd_data16x16.h5",
                jsonfilename="BL7011/test_data/missing_frames/labview.json",
                roi=[0, 2048, 0, 2048],
                average=10,
                verbose=True,
            )
            is None
        )
