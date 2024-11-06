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
    if mode == 'difference':
        return image_dichroism
    elif mode == 'asymmetry':
        return image_dichroism / (image_pol_A + image_pol_B)
    else:
        raise ValueError(
            'A calculation mode other than difference or asymmetry was '
            'specified')


def align_detector_images(im_ref: str,
                          im_move: str,
                          path_ref: str,
                          path_move: str) -> np.ndarray:
    """
    Aligns pairs of detector images given their respective detector translate
     and 2theta values stored in the 'instrument_1' dataset of the original
     h5 file.

    Parameters
    ----------
    im_ref: The reference image with size M x N
    im_move: The image that will be aligned to im_ref, with size M x N
    path_ref: The path to the HDF5 dataset associated with im_ref
        (i.e., h5_file['entry1']['instrument_1')
    path_move: The path to the HDF5 dataset associated with im_move

    Returns
    -------
    An M x N array containing the shifted im_move

    TODO: Implement theta, sample translate, and sample lift at some point
    """

    # Define a function to grab the different datasets from the HDF5 file
    def metadata_grabber(path:str) -> dict:
        # First, define an empty dictionary
        metadata = {}

        # Open up the h5 file and store the datasets in 'metadata'
        with h5py.File(path, 'r') as file:
            # Create a variable for the parent group that the datasets are stored within
            grp = file['entry1']['instrument_1']
            metadata['det_translate'] = grp['labview_data']['det_translate'][0]
            metadata['detector_rotate'] = grp['labview_data']['detector_rotate'][0]
            metadata['detector_distance'] = grp['detector_1']['distance'][0]
            metadata['x_pixel_size'] = grp['detector_1']['x_pixel_size'][0]
            metadata['y_pixel_size'] = grp['detector_1']['y_pixel_size'][0]

        return metadata

    # Pull out the detector translate and 2theta positions
    md_ref = metadata_grabber(path_ref)
    md_move = metadata_grabber(path_move)

    # We assume here that the x and y pixel sizes are identical... complain
    # if they are not.
    if md_ref['x_pixel_size'] != md_ref['y_pixel_size']:
        raise ValueError('The x- and y-pixel sizes are not identical.')

    # Check that the parameters are consistent between the two images...
    # complain if they are not.
    if not ((md_ref['detector_distance'] != md_move['detector_distance'])
            or (md_ref['x_pixel_size'] != md_move['x_pixel_size'])):

        raise ValueError('Alignment cannot be performed between images with'
                         'two different sample-detector distances or pixel '
                         'sizes.')

    # Calculate the pixel shift needed to align the two images
    shift_translate = np.round((md_move['det_translate'] - md_ref['det_translate']) / md_ref['x_pixel_size'])
    shift_tth = np.round((md_ref['detector_distance'] *
                         (np.sin(md_move['detector_rotate']) - np.sin(md_ref['detector_rotate'])))
                         / md_ref['x_pixel_size'])

    # Apply the shift to the image
    return ndi.shift(im_move, (shift_tth,shift_translate))
