The nexus.h5 files are not the original files produced by the bluesky exporter when Nexus is selected. The arrays in the file where trimmed down using this funcion (can also be found [here](https://gist.github.com/gnzng/0ee6408d4ea0c2cd609f0007cd9c79ea) is the link to the website.

code snippet: 
```python
import h5py


# Paths for the original and new H5 files
original_file_path = "BL7011/test_data/uncorrupted_frames/nexus.h5"
new_file_path = "BL7011/test_data/uncorrupted_frames/nexus16x16.h5"


# Open the H5 file, slice and save
def copy_and_modify_dataset(original_group, new_group, target_path):
    for name, item in original_group.items():
        if isinstance(item, h5py.Dataset):
            if len(item.shape) > 2:
                # Slicing out a smaller piece from more dimensional data
                # this will be the maximum of slicing for the target operation
                data = item[:, :, :20, :20]
            elif len(item.shape) <= 2:
                try:
                    data = item[:]
                except:
                    data = item
            else:
                data = item
            if original_group.name + "/" + name == target_path:
                # Modify the data by slicing an even smaller piece
                data = data[:, :, :16, :16]
            new_group.create_dataset(name, data=data)
        elif isinstance(item, h5py.Group):
            new_subgroup = new_group.create_group(name)
            copy_and_modify_dataset(item, new_subgroup, target_path)


# Define the path of the dataset to modify and the modification function
target_dataset_path = "/entry1/instrument_1/detector_1/data"

# Open the original H5 file for reading
with h5py.File(original_file_path, "r") as original_h5file:
    # Create a new H5 file for writing
    with h5py.File(new_file_path, "w") as new_h5file:
        copy_and_modify_dataset(original_h5file, new_h5file, target_dataset_path)

print(
    "Array modified and saved to the new file successfully, with all other datasets preserved."
)
```
