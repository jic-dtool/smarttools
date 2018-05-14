SMARTtools Specification
=======================

Overview
--------

SMARTTools is a bunch of related tools that allow dtool dataset to dateset processing.
Dataset to dataset processing is valuable as it can be used to automate data management.

Scenarios
---------

Joanna
^^^^^^

Joanna is an experimental biologist who has received some RNA sequencing data.

Earlier in the year Joanna sought advice from Chung, the in-house bioinformatician,
on how to process RNA sequencing data. He created an ``analysis.yml`` file for her
and showed her how to generate SLURM scripts from it on the cluster and how to
set those off.

Joanna asks Chung to package her new data into a dataset, which he does and
sends her back a URI from where the dataset can be accessed. Joanna then updates
her ``analysis.yml`` file using the new URI for the ``input_dataset`` field.
She then tries to run the script to generate the SLURM file. However, she gets
a message stating that the ``is_read1`` and ``paid_id`` overlays are missing.
She emails Chung to ask for help, ten minutes later he replies that he has sorted
the problem by running an overlay generation script on the dataset. This time
Joanna manges to generate the SLURM file and submit her jobs to the cluster.
When the job finishes she has been emailed a URI to the output dataset.

Chung
^^^^^

Chung is a bioinformatician that has a standardised and frequently used
workflow for which he wants to automate the data management.

The first step of the workflow trims adaptors of next generation sequencing
data. The trimmer takes a fastq file as input and writes out a trimmed fastq
file as output. To wrap this tool he therefore only needs to create a
``tool.yml`` file.

The second step of the workflow aligns pair end reads. The aligner takes as
input two files, the pair end reads, and produces one file as output.
Because this is a little bit more involved he needs to make use of the
SMARTTool Python API to create the wrapper.

Chung then writes a ``workflow.yml`` file where the output from the trimming
is used as the input for the aligner. He then uses the SLURM runner to create
batch scripts for processing the pipeline. These make use of dependencies to
automate the whole flow of the processing. The jobs are submitted to the cluster
and two days later the intermediate trimming and final alignment datasets URIs
are emailed to him.

Tjelvar
^^^^^^^

Tjelvar is a computational scientist charged with installing the SMARTTool
runners on the cluster. He reads the overview documentation to work out what
the SMARTTool project is all about. Here he learns that there are three aspects
to SMARTTools, end users can write ``analysis.yml`` files to define the
analysis they want to run, bioinformaticians and tool makers wrap existing
bioinformatics tools using the SMARTTool Python package, or otherwise create a
tool that adheres to the SMARTtool command line interface. However, the second
that is of interest to Tjelvar is the SMARTTool runner installation notes.
He follows these instructions to install the SMARTTool runner on the cluster.


Technical notes
---------------

- dtool-item-transform (currently smarttoolbase)
- dtool-dataset-transform (currently runners)

Questions
---------

- Can we make dtool-dataset-transform clever enough so that file-to-file tools can be defined using a tool.yml file?
- Should we move the dependence on dtool-item-transform into the tools that need them?
- Should we strip out the building of bioinformatics software as docker images from this repo, i.e. perhaps this repo should know nothing about specific tools?
- Is it possible to define software using URIs?
- How can we make make tools pluggable to the system? State that they simply have to provide the interface ``<input dataset URI> <identifier> <output dataset URI>``?
- At the moment it feels like everything is too couples and like the repository tries to do too many different things
- Maybe it should be split into a repository for runners; a repository with a helper classes and functions for making it easy to wrap tools to the interface; a JIC repository of tools
- What is responsible for checking that the analysis of an individual item has been successful?
- Perhaps nothing about smarttools should be worried about installation instructions for specific tools; perhaps this should be left to individual users/sys admins?
- What is responsible for defining what backends are accessible; the runner installation? Currently aligners need to be able to access overlays and the pair item which means that they would have to have the same backends configured in them...
- Perhaps the package with helper functions and classes for wrapping tools could depend on the runner package? That way the backends could be forced to stay in sync...
