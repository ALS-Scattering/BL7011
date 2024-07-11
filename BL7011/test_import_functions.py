from .import_functions import import_broken_h5


print(import_broken_h5("BL7011/test_data/test_missing_frames.h5", average = None).shape)
print(import_broken_h5("BL7011/test_data/test_missing_frames.h5", average = 10).shape)