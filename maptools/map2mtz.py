#
# Copyright (C) 2020 RFI
#
# Author: James Parkhurst
#
# This code is distributed under the GPLv3 license, a copy of
# which is included in the root directory of this package.
#
import logging
import os
import tempfile
import maptools.external


# Get the logger
logger = logging.getLogger(__name__)


def map2mtz(input_filename, output_filename=None, resolution=1):
    """
    Compute the CC between two maps

    Args:
        input_filename (str): The input map filename
        output_filename (str): The output mtz filename
        resolution (float): The resolution

    """
    maptools.external.map2mtz(
        mapin=os.path.abspath(input_filename),
        hklout=os.path.abspath(output_filename),
        resolution=resolution,
        wd=tempfile.mkdtemp(),
        stdout=None,
        param_file="map2mtz.dat",
        command_file="map2mtz.sh",
    )
