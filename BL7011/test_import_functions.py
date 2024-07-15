from BL7011.import_functions import import_broken_h5


print(
    import_broken_h5(
        "BL7011/test_data/missing_frames16x16.h5",
        average=10,
        verbose=True,
        roi=[0, 10, 0, 10],
        missing_frames=[0, 1],
        eps=0.01,
        for_roi=False,
        save_to_h5=False
    ).shape
)
