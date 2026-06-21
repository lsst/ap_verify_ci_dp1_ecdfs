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

"""Script for copying standard refcats that cover this dataset's fields.

Running this script allows for updates to the refcats to be incorporated
into the dataset.
"""

import argparse
import logging
import os
import sys

from lsst.daf.butler import Butler, CollectionType


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


########################################
# Fields and catalogs to process

DATA_IDS = [dict(detector=0, visit=2024111100094, physical_filter="r_03", instrument="LSSTComCam"),
            dict(detector=3, visit=2024111100094, physical_filter="r_03", instrument="LSSTComCam"),
            dict(detector=4, visit=2024111600297, physical_filter="r_03", instrument="LSSTComCam"),
            dict(detector=5, visit=2024111600297, physical_filter="r_03", instrument="LSSTComCam"),
            dict(detector=3, visit=2024111900082, physical_filter="r_03", instrument="LSSTComCam"),
            dict(detector=6, visit=2024111900082, physical_filter="r_03", instrument="LSSTComCam"),
            dict(detector=4, visit=2024112000208, physical_filter="r_03", instrument="LSSTComCam"),
            dict(detector=5, visit=2024112000208, physical_filter="r_03", instrument="LSSTComCam"),
            dict(detector=3, visit=2024120600098, physical_filter="r_03", instrument="LSSTComCam"),
            dict(detector=4, visit=2024120600098, physical_filter="r_03", instrument="LSSTComCam"),
            dict(detector=4, visit=2024112800140, physical_filter="r_03", instrument="LSSTComCam"),
            dict(detector=7, visit=2024112800140, physical_filter="r_03", instrument="LSSTComCam")
]
REFCAT_NAMES = {"the_monster_20250219"}

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
REPO_LOCAL = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "preloaded"))


########################################
# Command-line options

def _make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="src_dir", default="/repo/main",
                        help="Refcat source Butler repo, defaults to '/repo/main'.")
    parser.add_argument("-i", dest="src_collection", default="refcats",
                        help="Refcat source collection, defaults to 'refcats'.")
    return parser


args = _make_parser().parse_args()


########################################
# Identify all required shards


def _find_refcats(butler, refcats, data_ids):
    """Return refcats overlapping a set of exposures.

    Parameters
    ----------
    butler : `lsst.daf.butler.Butler`
        The butler to query for the refcats.
    refcats : iterable [`str`]
        The names of the refcats to search.
    data_ids : iterable [`dict` or `lsst.daf.butler.DataCoordinate`]
        The IDs of the exposures for which refcats are needed.

    Returns
    -------
    refcats : iterable [`lsst.daf.butler.DatasetRef`]
        The refcats that overlap with ``data_ids``.
    """
    query_prefix = "(instrument='{instrument}' AND (".format(**data_ids[0])
    subquery = "(visit={visit} AND detector={detector})"
    where = " OR ".join(subquery.format(**id) for id in data_ids)
    where = query_prefix + where + "))"

    return set(butler.registry.queryDatasets(refcats, where=where))

src_butler = Butler(args.src_dir, collections=args.src_collection, writeable=False)
logging.info("Searching for refcats in %s:%s...", args.src_dir, args.src_collection)
refcats = _find_refcats(src_butler, REFCAT_NAMES, DATA_IDS)
if not refcats:
    raise RuntimeError("No refcats found.")
logging.debug("%d refcat shards found", len(refcats))


########################################
# Transfer shards

STD_REFCAT = "refcats"

dest_butler = Butler(REPO_LOCAL, writeable=True)

logging.info("Copying refcats...")
# Copy to ensure that dataset is portable.
dest_butler.transfer_from(src_butler, refcats, transfer="copy", register_dataset_types=True)

dest_butler.registry.registerCollection(STD_REFCAT, CollectionType.CHAINED)
# We want to use these refcats, and no other.
dest_butler.registry.setCollectionChain(STD_REFCAT, {ref.run for ref in refcats})

logging.info("%d refcat shards copied to %s:%s", len(refcats), REPO_LOCAL, STD_REFCAT)
