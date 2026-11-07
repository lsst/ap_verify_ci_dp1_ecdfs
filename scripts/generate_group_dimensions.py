#!/usr/bin/env python
# This file is part of ap_verify_dataset_template.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Script for (re)generating group dimensions for this data set.

Running this script allows for updates of the existing dimensions if the
repository is being rebuilt or new raws are being added. It is not needed
if another script already runs ingest and copies the dimensions over (as
do both ``get_ephemerides.py`` and ``generate_self_preload.py``).

Example:
$ python generate_group_dimensions.py
"""

import logging
import os
import sys

from lsst.daf.butler import Butler

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


INSTRUMENT = "LSSTComCam"
# The group IDs to generate. For precursor instruments they equal the exposure
# IDs. For Rubin instruments you can look them up from the raws' source
# repository.
GROUP_IDS = {
    "2024-11-12T02:10:52.368",
    "2024-11-17T07:52:30.357",
    "2024-11-20T01:16:40.691",
    "2024-11-21T05:49:25.789",
    "2024-12-07T02:29:08.761",
    "2024-11-29T01:35:04.206"
}

# Avoid explicit references to dataset package to maximize portability.
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
DATASET_REPO = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "preloaded"))


########################################

records = [{"name": group, "instrument": INSTRUMENT} for group in GROUP_IDS]

repo = Butler(DATASET_REPO, writeable=True)
repo.registry.insertDimensionData("group", *records, replace=True, skip_existing=False)

logging.info(f"Records for groups {GROUP_IDS} stored in {DATASET_REPO}.")
