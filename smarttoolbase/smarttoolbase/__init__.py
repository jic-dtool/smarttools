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


class Command(object):

    def __init__(self, cmd_string, stdout_fname=None):
        self.cmd_string = cmd_string
        self.stdout_fname = stdout_fname


class SmartTool(object):
    """Base class for creating a Smart tool."""

    def __init__(self, input_uri, output_uri):
        self.input_dataset = dtoolcore.DataSet.from_uri(input_uri)
        self.output_proto_dataset = dtoolcore.ProtoDataSet.from_uri(output_uri)

        self.working_directory = None

        self.base_command_props = {}

    def create_subprocess_input(self, cmd_string, identifier):
        """Return list representing command to be run."""
        formatted_cmd_string = cmd_string.format(
            **self.base_command_props
        )
        return shlex.split(formatted_cmd_string)

    def __call__(self, identifier):
        """Run an analysis."""

        if self.working_directory is None:
            raise RuntimeError("run() can only be called within use of the class as a context")

        self.pre_run(identifier)

        for cmd in self.base_commands:
            subprocess_input = self.create_subprocess_input(cmd.cmd_string, identifier)
            if cmd.stdout_fname is None:
                subprocess.call(
                    subprocess_input,
                    cwd=self.working_directory
                )
            else:
                stdout_fpath = os.path.join(
                    self.working_directory,
                    cmd.stdout_fname
                )
                stdout = subprocess.check_output(
                    subprocess_input,
                    cwd=self.working_directory
                )
                with open(stdout_fpath, "w") as fh:
                    fh.write(stdout)

        self.stage_outputs(identifier)

    def __enter__(self):
        dtoolcore.utils.mkdir_parents(TMPDIR_PREFIX)
        self.working_directory = tempfile.mkdtemp(prefix=TMPDIR_PREFIX)
        return self

    def __exit__(self, type, value, tb):
        shutil.rmtree(self.working_directory)
        assert not os.path.isdir(self.working_directory)

    def pre_run(self, identifier):
        raise(NotImplementedError())

    def stage_outputs(self, identifier):
        # Set default useful name to relpath minus file extension.
        useful_name = self.input_dataset.item_properties(
            identifier
        )["relpath"].rsplit(".", 1)[0]

        # Update the useful name if the "useful_name" overlay exists
        # in the input dataset.
        if "useful_name" in self.input_dataset.list_overlay_names():
            useful_name = self.input_dataset.get_overlay(
                'useful_name'
            )[identifier]

        for filename in self.outputs:


            fpath = os.path.join(self.working_directory, filename)
            relpath = os.path.join(useful_name, filename)
            out_id = self.output_proto_dataset.put_item(fpath, relpath)
            self.output_proto_dataset.add_item_metadata(
                out_id,
                'from',
                "{}/{}".format(self.input_dataset.uri, identifier)
                )
