"""smarttoolbase package."""

import subprocess
import shlex

import dtoolcore

__version__ = "0.1.0"


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
