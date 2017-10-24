"""smarttoolbase package."""

import os
import shutil
import argparse
import subprocess
import tempfile
import shlex
from contextlib import contextmanager

import dtoolcore

__version__ = "0.1.0"


TMPDIR_PREFIX = os.path.expanduser(
    "~/tmp/tmp"
)


@contextmanager
def temp_working_dir():
    dtoolcore.utils.mkdir_parents(TMPDIR_PREFIX)
    working_dir = tempfile.mkdtemp(prefix=TMPDIR_PREFIX)

    try:
        yield working_dir
    finally:
        shutil.rmtree(working_dir)


def parse_args():
    """Return the argparse object."""
    parser = argparse.ArgumentParser(
        description="Smart tool argument parsing"
    )
    parser.add_argument(
        "-d",
        "--input_uri",
        required=True,
        help="URI of the input dataset"
    )
    parser.add_argument(
        "-o",
        "--output_uri",
        required=True,
        help="URI of the output proto dataset"
    )
    parser.add_argument(
        "-i",
        "--identifier",
        required=True,
        help="Item identifier"
    )
    args = parser.parse_args()
    return args



class SmartTool(object):
    """Base class for creating a Smart tool."""

    def __init__(self, input_uri, output_uri):
        self.input_dataset = dtoolcore.DataSet.from_uri(input_uri)
        self.output_proto_dataset = dtoolcore.ProtoDataSet.from_uri(output_uri)

    def command_list(self, identifier):
        """Return list representing command to be run."""
        command_string = self.base_command.format(
            **self.base_command_props
        )
        return shlex.split(command_string)

    def run(self, identifier):
        """Run an analysis."""
        subprocess.call(self.command_list(identifier))


    def stage_outputs(self, identifier, working_directory):
        for filename in self.outputs:

            useful_name = self.input_dataset.get_overlay(
                'useful_name'
            )[identifier]

            fpath = os.path.join(working_directory, filename)
            relpath = os.path.join(useful_name, filename)
            out_id = self.output_proto_dataset.put_item(fpath, relpath)
            self.output_proto_dataset.add_item_metadata(
                out_id,
                'from',
                "{}/{}".format(self.input_dataset.uri, identifier)
                )
