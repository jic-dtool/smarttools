Smart Tools
===========

A Smart tool is a docker/singularity containerised analysis that takes
standardised input and output arguments, which allows it to be run by something
else that understands those arguments. This means that it is possible to write
other tools that can process all the items in the input dataset.

A Smart tool takes as input:

* An input dataset
* An identifier (of an item in the input dataset)
* An output dataset

Global data are passed into the Smart tool using environment variables, e.g.::

    export PROTEIN_FASTA_FILE_PATH=~/swissprot.fasta

.. code-block:: none

    python my_smarttool.py  \
      -i item_identifier  \
      -d file:///tmp/input_dataset/  \
      -o file:///tmp/ouptut_dataset/
