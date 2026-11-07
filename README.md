# ap_verify_ci_dp1_ecdfs
LSST ComCam data from Fall 2024 in the Euclid Chandra Deep Field South


Git LFS
-------

To clone and use this repository, you'll need Git Large File Storage (LFS).

Our [Developer Guide](http://developer.lsst.io/en/latest/tools/git_lfs.html) explains how to setup Git LFS for LSST development.

Usage
-----

Datasets are designed to be run using [`ap_verify`](https://pipelines.lsst.io/modules/lsst.ap.verify/), which is distributed as part of the `lsst_distrib` package of the [LSST Science Pipelines](https://pipelines.lsst.io/).

This dataset is not included in `lsst_distrib` and is not available through `newinstall.sh`.
However, it can be installed explicitly with the [LSST Software Build Tool](https://developer.lsst.io/stack/lsstsw.html) or by cloning directly:

    git clone https://github.com/lsst/<dataset>/
    setup -r <dataset>

See the Science Pipelines documentation for more detailed instructions on [installing datasets](https://pipelines.lsst.io/modules/lsst.ap.verify/datasets-install.html) and [running `ap_verify`](https://pipelines.lsst.io/modules/lsst.ap.verify/running.html).
