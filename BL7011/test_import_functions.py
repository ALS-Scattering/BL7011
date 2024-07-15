from BL7011.import_functions import import_broken_h5


print(
    import_broken_h5(
        "BL7011/test_data/test_missing_frames.h5",
        average=10,
        verbose=True,
        roi=[0, 10, 0, 10],
        missing_frames=[0, 1],
        eps=0.01,
        for_roi=True,
        save_to_h5=True
    ).shape
)
