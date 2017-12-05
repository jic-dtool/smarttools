"""Test the smarttoolbase package."""

from . import tmp_dir_fixture  # NOQA
import dtoolcore

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


def test_version_is_string():
    import smarttoolbase
    assert isinstance(smarttoolbase.__version__, str)

def test_functional(tmp_dir_fixture, monkeypatch):  # NOQA
    from smarttoolbase import SmartTool

    input_admin_metadata = dtoolcore.generate_admin_metadata(
        "my_input_ds",
        "testing_bot"
    )
    input_dataset = dtoolcore.generate_proto_dataset(
        admin_metadata=input_admin_metadata,
        prefix=tmp_dir_fixture,
        storage="file"
    )
    input_dataset.create()
    input_dataset.put_readme("")
    input_dataset.freeze()

    output_admin_metadata = dtoolcore.generate_admin_metadata(
        "my_output_ds",
        "testing_bot"
    )
    output_dataset = dtoolcore.generate_proto_dataset(
        admin_metadata=output_admin_metadata,
        prefix=tmp_dir_fixture,
        storage="file"
    )
    output_dataset.create()
    output_dataset.put_readme("")

    with  SmartTool(
        input_uri=input_dataset.uri,
        output_uri=output_dataset.uri,
    ) as smart_tool:

        assert smart_tool.input_dataset.uri == input_dataset.uri
        assert smart_tool.output_proto_dataset.uri == output_dataset.uri


        smart_tool.base_commands = [
            "bowtie2 -x {reference_prefix} -1 {forward_read_fpath} -2 {reverse_read_fpath} -S {output_fpath}",
        ]
        smart_tool.outputs = []

        smart_tool.base_command_props = {
            "reference_prefix": "/tmp/reference/Athaliana",
            "forward_read_fpath": "/tmp/input/data/read1.fq",
            "reverse_read_fpath": "/tmp/input/data/read2.fq",
            "output_fpath": "/tmp/working/output",
        }

        expected_command_list = [
            "bowtie2",
            "-x", "/tmp/reference/Athaliana",
            "-1", "/tmp/input/data/read1.fq",
            "-2", "/tmp/input/data/read2.fq",
            "-S", "/tmp/working/output"
        ]

#       assert smart_tool.command_list("identifier") == expected_command_list

        import subprocess
        subprocess.call = MagicMock()

        smart_tool.pre_run = MagicMock()

        smart_tool("identifier")

        subprocess.call.assert_called_once_with(
            expected_command_list,
            cwd=smart_tool.working_directory
        )
        smart_tool.pre_run.assert_called_once()
