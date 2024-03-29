#
# Copyright (C) 2020 RFI
#
# Author: James Parkhurst
#
# This code is distributed under the GPLv3 license, a copy of
# which is included in the root directory of this package.
#
import logging
import numpy
import scipy.ndimage.measurements
import skimage.filters
from maptools.util import read, write


# Get the logger
logger = logging.getLogger(__name__)


def array_segment(data, num_objects=1):
    """
    Segment the map

    Args:
        data (array): The input data
        num_objects (int): The number of objects

    Returns:
        array: The segmented array

    """

    # Compute a threshold value
    threshold = skimage.filters.threshold_otsu(data)
    logger.info("Using threshold = %f" % threshold)

    # Label the pixels
    labels, num_labels = scipy.ndimage.measurements.label(
        (data >= threshold).astype("int8")
    )
    logger.info("Found %d objects" % num_labels)

    # Compute the largest objects
    num_pixels = numpy.bincount(labels.flatten())
    sorted_indices = numpy.argsort(num_pixels[1:])[::-1] + 1
    result = numpy.zeros(shape=data.shape, dtype="uint8")
    for index in sorted_indices[:num_objects]:
        logger.info("Selecting object with %d pixels" % num_pixels[index])
        result[labels == index] = 1

    # Return the data
    return result


def mapfile_segment(input_filename, output_filename, num_objects=1):
    """
    Segment the map

    Args:
        input_filename (str): The input map filename
        output_filename (str): The output map filename
        num_objects (int): The number of objects

    """

    # Open the input file
    infile = read(input_filename)

    # Get data
    data = infile.data.copy()

    # Apply the segment
    data = array_segment(data, num_objects=num_objects)

    # Write the output file
    write(output_filename, data, infile=infile)


def segment(*args, **kwargs):
    """
    Segment the map

    """
    if len(args) > 0 and type(args[0]) == "str" or "input_filename" in kwargs:
        func = mapfile_segment
    else:
        func = array_segment
    return func(*args, **kwargs)
