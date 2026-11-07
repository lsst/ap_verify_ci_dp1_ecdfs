#!/bin/bash
# This file is part of ap_verify_dp1_ecdfs.
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

# Script for regenerating a complete repository in preloaded/.
# Running this script allows for AP pipeline inputs to incorporate Science
# Pipelines improvements. It makes no attempt to update the set of input
# exposures; they are hard-coded into the files.
# This script takes roughly <TBD> hours to run on rubin-devl.
#
# Example:
# $ nohup make_all.sh -t "u/me/DM-123456" &
# fills this dataset, using the u/me/DM-123456 collection in
# /repo/main as a staging area. See make_all.sh -h for more options.

# # Abort script on any error
# set -e
# # Echo all commands
# set -x

SCRIPT_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"
DATASET_REPO="${SCRIPT_DIR}/../preloaded/"

INSTRUMENT=LSSTComCam
UMBRELLA_COLLECTION="${INSTRUMENT}/defaults"  # Hardcoded into ap_verify, do not change!
RB_MODEL="tac_cnn_comcam_2025-02-18"
INJECTION_CATALOG_COLLECTION="fake-injection-catalog"

TEMPLATE_COLLECTION="LSSTComCam/runs/DRP/DP1/w_2025_17/DM-50530"
TEMPLATE_COLLECTION="LSSTComCam/ci_ecdfs_test"
TEMPLATE_DATAQUERY="\"instrument='LSSTComCam' AND skymap='lsst_cells_v1' AND band='r' AND (tract=4848 AND patch IN (90,91) OR tract=4849 AND patch IN (89) OR tract=5063 AND patch IN (4,5,13,14,15,16,23,24,25,26,33,34,35,36))\""

########################################
# Command-line options

print_error() {
    >&2 echo "$@"
}

usage() {
    print_error
    print_error "Usage: $0 [-b BUTLER_REPO] [-c CALIB_COLLECTION] [-h]"
    print_error
    print_error "Specific options:"
    print_error "   -b          Butler repo URI, defaults to /sdf/group/rubin/repo/main"
    print_error "   -c          calibration collection (chain) from which to draw calibs, defaults to <instrument>/calib"
    print_error "   -h          show this message"
    exit 1
}

parse_args() {
    while getopts "b:c:t:h" option $@; do
        case "$option" in
            b)  SCRATCH_REPO="$OPTARG";;
            c)  CALIB_COLLECTION="$OPTARG";;
            h)  usage;;
            *)  usage;;
        esac
    done
    if [[ -z "${SCRATCH_REPO}" ]]; then
        SCRATCH_REPO=/sdf/group/rubin/repo/main
    fi
    if [[ -z "${CALIB_COLLECTION}" ]]; then
        CALIB_COLLECTION="${INSTRUMENT}/calib"
    fi
}
parse_args $@


# Unlikely to be workflow- or version-dependent, so hardcode it.
REFCAT_COLLECTION=refcats


########################################
# Repository creation and instrument registration

"${SCRIPT_DIR}/make_empty_repo.sh"


########################################
# Import calibs, templates, and refcats

python "${SCRIPT_DIR}/import_calibs.py" -b ${SCRATCH_REPO} -c "${CALIB_COLLECTION}"
python "${SCRIPT_DIR}/import_templates.py" -b ${SCRATCH_REPO} -t "${TEMPLATE_COLLECTION}" #--where "${TEMPLATE_DATAQUERY}"
python "${SCRIPT_DIR}/ingest_refcats.py" -b ${SCRATCH_REPO} -i "${REFCAT_COLLECTION}"


########################################
# Import pretrained NN models

python "${SCRIPT_DIR}/get_nn_models.py" -m "${RB_MODEL}"


########################################
# Download solar system ephemerides

# python "${SCRIPT_DIR}/generate_group_dimensions.py"

python "${SCRIPT_DIR}/get_ephemerides.py"

########################################
# Preloaded APDB and fake-injection catalogs
# generate_self_preload.py now builds:
# - dia_catalogs/apdb
# - fake-injection-catalog/*

python "${SCRIPT_DIR}/generate_self_preload.py"

########################################
# Final clean-up

# The individual collections are set in the appropriate sub-scripts.
# Keep fake-injection-catalog in the umbrella chain for downstream defaults.
butler collection-chain "${DATASET_REPO}" "${UMBRELLA_COLLECTION}" \
    templates skymaps ${INSTRUMENT}/calib refcats sso dia_catalogs models \
    ${INJECTION_CATALOG_COLLECTION}

python "${SCRIPT_DIR}/make_preloaded_export.py"

echo "Preloaded repository complete."
echo "All preloaded data products are accessible through the ${UMBRELLA_COLLECTION} collection."
