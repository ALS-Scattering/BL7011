import numpy as np 
import h5py
from .tools import where_is_my_frame_missing


def import_broken_h5(h5filename : str, average : int = None) -> np.array:
    """
    When in the bluesky exporter None is selected it exports the collected 
    detector data in an .h5 file while the recorded metadata from labview 
    is written to a .json file. This function returns the data of the 
    detectors.

    
    Parameters
    ----------
    h5filename : str
        whole path of the .json-file exported by bluesky exporter
    average : int
        averaging all X frames, if None missing frame will be replaced by 0

    Returns
    -------
    data : np.array
        data as np.array
    """
    # reading in the file and selecting the time stamps
    f = h5py.File(h5filename, 'r+')
    data = np.array(f["entry"]["data"]["data"][:])
    f.close()
    
    missing_frame = where_is_my_frame_missing(h5filename)

    if average is None:
        frame_shape = data.shape[1:]
        none_array = np.full(frame_shape,0)
        data = np.insert(data, missing_frame, none_array, axis=0)
        return data
    
    elif isinstance(average, int):
        all_average_list = []
        frac = missing_frame/average
        for n in range((len(data)+1)//average):
            if n + 1 < frac:
                all_average_list.append(np.mean(data[n*average:(n+1)*average,:,:], axis=0))
            if n + 1 > frac:
                all_average_list.append(np.mean(data[n*average-1:(n+1)*average-1,:,:], axis=0))
        data = np.array(all_average_list)
        return data
    
    else:
        return print('Probably wrong averager flag.')
