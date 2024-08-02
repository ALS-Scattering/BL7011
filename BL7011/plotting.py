"""
    This file contains functions to plot 2D images (M x N np.ndarrays).

    Authors: Dayne Sasaki, Damian Guenzing
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def plot_image(
        image: np.ndarray,
        *,
        title: str = ''
) -> None:
    """
    Plots a single CCD image. What more could you want?

    The intensity scaling is based on its 5th and 95th percentile intensity
    and is shown using a logarithmic viridis colormap.

    Parameters:
        image: np.ndarray
            A M x N CCD image.
        title: str
            Title of the figure

    Returns:
        None. It shows a matplotlib figure.
    """
    # Generate a figure with three side-by-side subplots
    # TODO: Generalize this function so that multiple images can
    #   be plotted at the same time
    fig, axarr = plt.subplots(nrows=1, ncols=1, layout='constrained',
                              figsize=(11, 3))

    axarr.set_box_aspect(aspect=1)
    axarr.set_title(title)

    # Show the images
    """
    im = axarr.imshow(image,
                      cmap='viridis',
                      origin='lower',
                      norm=LogNorm(vmin=np.percentile(image, 5),
                                      vmax=np.percentile(image, 95)))
    """
    im = axarr.imshow(image,
                      cmap='viridis',
                      origin='lower',
                      vmin=np.percentile(image, 5),
                      vmax=np.percentile(image, 95))

    fig.colorbar(im, ax=axarr)
    plt.draw()
    plt.pause(0.001)


def plot_three_images_dichroism(
        image_1: np.ndarray,
        image_2: np.ndarray,
        image_3: np.ndarray,
        *,
        title_main: str = '',
        title_1: str = '',
        title_2: str = '',
        title_3: str = '',
        save_path: str = None,
) -> None:
    """
    Plots three images side-by-side. The intensity scaling of the left and
    center images are based on their respective 5th and 95th percentile
    intensities and are shown using a logarithmic viridis colormap. The right
    image intensity is scaled based on either the 15th or 85th-percentile
    intensity magnitude. Whichever one is larger will define how the scaling
    where the intensity will vary from +- that intensity. The right image
    is shown in bwr colormap

    This function is intended to show two different polarization CCD images
    along with the associated dichroism image by its side.

    Parameters:
        image_1 through image_3: np.ndarray
            The three different M x N images. For plotting polarization and
            dichroism images, image_3 corresponds with the dichroism image.
            image_1, _2, and _3 are the left, center, and right images,
            respectively.
        title_main: str
            The main title of the plot
        title_1 through title_3: str
            The titles above each of the three images
        save_path: str
            If a save path is given, then the figure will be saved to that
            directory with the associated file name.

    Returns:
        None

    TODO: Allow this function to save figures
    """
    # Trick 1: use plt.ion() and plt.show()
    plt.ion()
    plt.show()

    # Generate a figure with three side-by-side subplots
    fig, axarr = plt.subplots(nrows=1, ncols=3, layout='constrained',
                              figsize=(11, 3))

    # Iteratively modify the axes to have aspect ratios of 1
    axarr[0].set_box_aspect(aspect=1)
    axarr[1].set_box_aspect(aspect=1)
    axarr[2].set_box_aspect(aspect=1)

    # Generate the titles
    fig.suptitle(title_main)
    axarr[0].set_title(title_1)
    axarr[1].set_title(title_2)
    axarr[2].set_title(title_3)

    # Figure out what the largest magnitude pixel in image_3 is for
    # setting the color limit in dichroism
    intensity_max = np.absolute(np.percentile(image_3, 15))
    intensity_min = np.absolute(np.percentile(image_3, 85))
    # Set the color limit of the image
    image_3_climit = max(intensity_max, intensity_min)

    # Show the images
    im1 = axarr[0].imshow(image_1,
                          cmap='viridis',
                          origin='lower',
                          norm=LogNorm(vmin=np.percentile(image_1, 5),
                                       vmax=np.percentile(image_1, 95)))
    im2 = axarr[1].imshow(image_2,
                          cmap='viridis',
                          origin='lower',
                          norm=LogNorm(vmin=np.percentile(image_1, 5),
                                       vmax=np.percentile(image_1, 95)))
    im3 = axarr[2].imshow(image_3, cmap='bwr',
                          vmin=-image_3_climit,
                          vmax=image_3_climit,
                          origin='lower')

    fig.colorbar(im1, ax=axarr[0])
    fig.colorbar(im2, ax=axarr[1])
    fig.colorbar(im3, ax=axarr[2])
    # Trick 2: call plt.draw() and wait a little while
    plt.draw()
    plt.pause(0.001)

    # If save_path has been defined, then save the figure
    if save_path is not None:
        fig.savefig(save_path)
