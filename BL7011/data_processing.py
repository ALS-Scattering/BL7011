"""
    This file contains functions to process various CCD data acquired at
    the COSMIC Scattering BL7.0.1.1

    Stuff to add at some point:
    - Q conversion
    - Peak finding function
    - Peak broadening function
    - Consider making some kind of class out of calculate_dichroism

    Authors: Dayne Sasaki
"""
import numpy as np
from BL7011 import file_processing as fp


def calculate_dichroism(
        image_pol_a: np.ndarray,
        image_pol_b: np.ndarray,
        mode: str = 'difference'
) -> np.ndarray:
    """
    Calculates the dichroism image using two CCD images of different
    polarizations. This function assumes that you're using the appropriate
    pair of polarization images to calculate with (i.e., same dimensions,
    using both circular or linear polarized light)

    PARAMETERS
    -----
    image_pol_a: np.ndarray
        The first M x N polarization image
    image_pol_b: np.ndarray
        The second M x N polarization image
    mode: str
        The type of dichroism calculation to perform
        - 'difference': Calculates image as (image_pol_A - image_pol_B)
        - 'asymmetry': Calculates image as
                      (image_pol_A - image_pol_B) / (image_pol_A + image_pol_B)

    RETURNS
    -----
    np.ndarray of the calculated dichroism image
    """
    image_dichroism = image_pol_a - image_pol_b
    if mode is 'difference':
        return image_dichroism
    elif mode is 'asymmetry':
        return image_dichroism / (image_pol_a + image_pol_b)
    else:
        raise ValueError(
            'A calculation mode other than difference or asymmetry was '
            'specified')


def calculate_dichroism_from_file(file_pol_a: str,
                                  file_pol_b: str,
                                  *,
                                  mode: str = 'difference',
                                  correction: str = '',
                                  variable_stack: bool = False
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculates a dichroism image using two opposite polarization images loaded
    from HDF5 files.

    Parameters
    ----------
    file_pol_a: str
        File path of the first polarization image
    file_pol_b: str
        File path of the second polarization image
    mode: str
        The type of dichroism calculation to perform
        - 'difference': Calculates image as (image_pol_A - image_pol_B)
        - 'asymmetry': Calculates image as
                (image_pol_A - image_pol_B) / (image_pol_A + image_pol_B)
    correction: str
        Type of intensity correction to perform on the CCD image 'ccd_image'
            - Nothing : Return the raw ccd image
            - 'i0 blade' : Normalize ccd image by the right blade current
            - 'i0 rlrl' : Normalized by the XS111 RLRL diode (what is this?)
            - 'cps' : Normalize ccd image by acquisition time (counts per sec)
    variable_stack: bool
        Setting this to False will make the function calculate an average
        of an image stack (i.e., each frame in the stack represents multiple
        "redundant" camera exposure and do not have any parameters varying)


    Returns a tuple containing...
    -------
    im_dichro: np.ndarray
        The calculated dichroism image
    im_pol_a: np.ndarray
        The first polarization image
    im_pol_b: np.ndarray
        The second polarization image
    """
    # Load the two polarization images
    im_pol_a = fp.load_h5_image(file_pol_a, correction)
    im_pol_b = fp.load_h5_image(file_pol_b, correction)

    # If the user sets variable_stack = False, then average the
    # entire image stack to a single image
    if not variable_stack:
        im_pol_a = np.average(im_pol_a, axis=0)
        im_pol_b = np.average(im_pol_b, axis=0)

    # Calculate dichroism
    im_dichro = calculate_dichroism(im_pol_a, im_pol_b, mode=mode)

    return im_dichro, im_pol_a, im_pol_b