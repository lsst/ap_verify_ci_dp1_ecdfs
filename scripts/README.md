Dataset management script templates
===================================

This directory has example scripts for (re)creating an ap_verify dataset.
Adopting such scripts for your own datasets is highly recommended, to make it easy to update the pipeline inputs (in particular, calibs and templates) for pipeline improvements.
These scripts are *not* intended to be used as-is; they may require some fine-tuning to adapt to the specifics of your data set.

*Any* change to the repo requires running `make_preloaded_export.py` to ensure the export file is up-to-date.
The data set will not run correctly without this step, but it also makes it easy to see and review each commit's changes.

The scripts are designed to be modular, and can be called either all at once (through `make_all.sh`), or individually.
`generate_self_preload.py` now includes fake-catalog generation and sharding as part of its workflow.
For routine regeneration, prefer `generate_self_preload.py` and treat `generate_fake_injection_catalog.sh` as deprecated.
See each script's docstring for usage instructions; those scripts that take arguments also support `--help`.

Contents
--------
path                               | description
:----------------------------------|:-----------------------------
make_all.sh                        | Rebuild everything from scratch.
generate_fake_injection_catalog.sh | Deprecated for routine use; fake catalog generation and sharding are handled by `generate_self_preload.py`.
generate_group_dimensions.py       | Predefine the group dimensions corresponding to the input raws. This allows support for preprocessing datasets.
generate_self_preload.py           | Create preloaded APDB datasets by simulating a processing run with no pre-existing DIAObjects, then generate and shard fake injection catalogs.
get_ephemerides.py                 | Download solar system ephemerides and register them in `preloaded/`.
get_nn_models.py                   | Transfer a selected pretrained model from an external repo (such as `repo/main`) and register it in `preloaded/`.
import_calibs.py                   | Transfer calibs from an external repo (such as `repo/main`) and register them in `preloaded/`.
import_templates.py                | Transfer templates from an external repo (such as `repo/main`) and register them in `preloaded/`.
ingest_refcats.py                  | Transfer refcats from an external repo (such as `repo/main`) and register them in `preloaded/`.
make_empty_repo.sh                 | Replace `preloaded/` with a repo containing only dimension definitions and standard "curated" calibs.
make_preloaded_export.py           | Create an export file of `preloaded/` that's compatible with `butler import`.
