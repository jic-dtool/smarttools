Smart Tools
===========

Repository of Smart tools for running analyses on dtool datasets.

A Smart tool is a docker/singularity containerised analysis that takes
standardised input and output arguments, which allows it to be run by something
else that understands those arguments. This means that it is possible to write
other tools that can process all the items in the input dataset.

A Smart tool takes as input:

* An input dataset
* An identifier (of an item in the input dataset)
* An output dataset
* Some parameters for specifying global data, e.g. a reference genome
  (implementation yet to be decided upon)

.. code-block:: none

    python my_smarttool.py  \
      -i item_identifier  \
      -d file:///tmp/input_dataset/  \
      -o file:///tmp/ouptut_dataset/


Levels of abstraction
---------------------

- Hardware (e.g. cluster)
- Scheduler (e.g. slurm)
- [Optional] Smart tool runner (e.g. Redis queue)
- Smart tool
- Analyses script or third party tool
