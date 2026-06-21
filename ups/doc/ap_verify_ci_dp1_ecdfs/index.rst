.. _ap_verify_ci_dp1_ecdfs-package:

##########################
ap_verify_ci_dp1_ecdfs
##########################

The ``ap_verify_ci_dp1_ecdfs`` package is used to create :doc:`datasets</modules/lsst.ap.verify/datasets>` for :doc:`/modules/lsst.ap.verify/index`.
It is not itself a valid dataset.

.. _ap_verify_ci_dp1_ecdfs-using:

Using ap_verify_ci_dp1_ecdfs
================================

This package provides an example for how a dataset package can be put together.
It is not guaranteed to be ingestible using ``ap_verify``, nor are the individual files guaranteed to be usable with each other.
The package provides some instructions on how to create a new dataset; more information can be found in :doc:`/modules/lsst.ap.verify/datasets-creation`.

.. _ap_verify_ci_dp1_ecdfs-contents:

Dataset contents
================

This package provides a number of demonstration files copied from `obs_test <https://github.com/lsst/obs_test/>`_.
See that package for detailed file and provenance information.

This package contains only raw files, with no calibration information or difference imaging templates.

.. _ap_verify_ci_dp1_ecdfs-contributing:

Contributing
============

``ap_verify_ci_dp1_ecdfs`` is developed at https://github.com/lsst-dm/ap_verify_ci_dp1_ecdfs.
You can find Jira issues for this module under the `ap_verify <https://jira.lsstcorp.org/issues/?jql=project%20%3D%20DM%20AND%20component%20%3D%20ap_verify%20AND%20text~"dataset template">`_ component.

.. If there are topics related to developing this module (rather than using it), link to this from a toctree placed here.

.. .. toctree::
..    :maxdepth: 1
