"""
    This file contains functions to process various CCD data acquired at
    the COSMIC Scattering BL7.0.1.1



    Authors: Dayne Sasaki
"""
import numpy as np


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


