"""
    This file contains functions to process various CCD data acquired at
    the COSMIC Scattering BL7.0.1.1



    Authors: Dayne Sasaki
"""
import numpy as np
import h5py
from scipy import ndimage as ndi

def preprocess_ccd_image(
        image: np.ndarray,
        divisor: float
) -> np.ndarray:
    """
    Outputs an M x N CCD image normalized by some experimental normalizing
    factor, such as the blade current

    PARAMETERS
    -----
    image: np.ndarray
        A M x N numpy array
    divisor: float
        The value to


    """



def calculate_dichroism(
        image_pol_A: np.ndarray,
        image_pol_B: np.ndarray,
        mode: str = 'difference'
) -> np.ndarray:
    """
    Calculates the dichroism image using two CCD images of different
    polarizations. This function assumes that you're using the appropriate
    pair of polarization images to calculate with (i.e., same dimensions,
    using both circular or linear polarized light)

    PARAMETERS
    -----
    image_pol_A: np.ndarray
        The first M x N polarization image
    image_pol_B: np.ndarray
        The second M x N polarization image
    mode: str
        The type of dichroism calculation to perform
        - 'difference': Calculates image as (image_pol_A - image_pol_B)
        - 'asymmetry': Calculates image as
                      (image_pol_A - image_pol_B) / (image_pol_A + image_pol_B)
    """
    image_dichroism = image_pol_A - image_pol_B
    if mode is 'difference':
        return image_dichroism
    elif mode is 'asymmetry':
        return image_dichroism / (image_pol_A + image_pol_B)
    else:
        raise ValueError(
            'A calculation mode other than difference or asymmetry was '
            'specified')


def align_detector_images(im_ref: str,
                          im_move: str,
                          dataset_ref: h5py._hl.dataset.Dataset,
                          dataset_move: h5py._hl.dataset.Dataset) -> np.ndarray:
    """
    Aligns pairs of detector images given their respective detector translate
     and 2theta values stored in the 'instrument_1' dataset of the original
     h5 file.

    Parameters
    ----------
    im_ref: The reference image with size M x N
    im_move: The image that will be aligned to im_ref, with size M x N
    dataset_ref: The HDF5 dataset associated with im_ref
        (i.e., h5_file['entry1']['instrument_1')
    dataset_move: The HDF5 dataset associated with im_move

    Returns
    -------
    An M x N array containing the shifted im_move

    TODO: Implement theta, sample translate, and sample lift at some point
    """
    # Pull out the detector translate and 2theta positions
    det_translate_ref = dataset_ref['labview_data']['det_translate'][()]
    tth_ref = dataset_ref['labview_data']['detector_rotate'][()]

    det_translate_move = dataset_move['labview_data']['det_translate'][()]
    tth_move = dataset_move['labview_data']['detector_rotate'][()]

    # Grab the sample-detector distance and pixel size
    sample_detector_distance = dataset_ref['detector_1']['distance'][()]
    pixel_size = dataset_ref['detector_1']['x_pixel_size'][()]

    # We assume here that the x and y pixel sizes are identical... complain
    # if they are not.
    if pixel_size != dataset_ref['detector_1']['y_pixel_size'][()]:
        raise ValueError('The x- and y-pixel sizes are not identical.')

    # Check that the parameters are consistent between the two images...
    # complain if they are not.
    if not ((sample_detector_distance != dataset_move['detector_1']['distance'][()])
            or (pixel_size != dataset_ref['detector_1']['y_pixel_size'][()])):


        raise ValueError('Alignment cannot be performed between images with'
                         'two different sample-detector distances or pixel '
                         'sizes.')

    # Calculate the pixel shift needed to align the two images
    shift_translate = np.round((det_translate_move - det_translate_ref) / pixel_size)
    shift_tth = np.round((sample_detector_distance * (np.sin(tth_move) - np.sin(tth_ref))) / pixel_size)

    # Apply the shift to the image
    return ndi.shift(im_move, (shift_tth,shift_translate))
