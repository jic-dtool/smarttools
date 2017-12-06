Bioinformatics support as code
==============================

This project contains functionality for describing bioinformatic analyses as
code.

Quick start
-----------

Install the dependencies::

    $ pip install -r requirements
    $ cd smarttools/smarttoolbase && python setup.py install && cd ../..

Create the file ``analysis.yml`` with the content below.

.. code-block:: yaml

    input_dataset_uri: runners/example_analysis/data/todo_lists
    output_dataset_base: /tmp
    output_dataset_name_suffix: top_4_things
    local_smarttool_fpath: smarttools/smarttools/simple_example_tool/smarttool_runner.py

Run the analysis::

    $ python runners/scripts/local_runner.py analysis.yml
    Created: file:///tmp/todo_lists_top_4_things

Repository overview
-------------------

The directory ``smarttools`` contains code and Docker image definitions for
building so called Smart tools.

A Smart tool is a docker/singularity containerised analysis that takes
standardised input and output arguments, which allows it to be run by something
else that understands those arguments. This means that it is possible to write
other tools, so called "runners", that can process all the items in the input
dataset.

These tools runners are present in the ``runners`` directory.  Smarttool
runners are programs designed to take input Dtool datasets and smartools and
produce the scripts or directly execute commands required to process the
dataset.

Some Smart tools require the input dataset to have specific overlays specified.
For example the ``align_seqs_hisat2`` Smart tool requires the overlays
``is_read1`` and ``pair_id`` to be set. These can be generated using overlay
creator scripts stored in the directory ``overlay_creators``. To create the
``is_read1`` and ``pair_id`` overlays on a dataset with fastq files one could
use the ``create_paired_read_overlays_from_fname.py`` script.
