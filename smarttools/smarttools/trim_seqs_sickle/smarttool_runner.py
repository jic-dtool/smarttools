"""Run sickle.

The trimmers are specified using the TRIMMOMATIC_TRIMMERS environment variable,
e.g.:

export TRIMMOMATIC_TRIMMERS="ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"
"""

import os

from smarttoolbase import SmartTool, Command, parse_args

from dtoolcore.utils import generate_identifier

BASE_COMMANDS = [
    Command("sickle pe -t sanger -f {forward_read_fpath}  -r  {reverse_read_fpath}  -o  sickled_1.fq  -p sickled_2.fq   -s  trash.fq")  # NOQA
]

OUTPUTS = [
    'sickled_1.fq',
    'sickled_2.fq',
]


def find_paired_read(dataset, identifier):
    pair_id = dataset.get_overlay('pair_id')
    return pair_id[identifier]


class TrimSeqsTrimmomatic(SmartTool):

    def pre_run(self, identifier):

        self.base_command_props['forward_read_fpath'] = self.input_dataset.item_content_abspath(identifier)  # NOQA
        paired_read_identifier = find_paired_read(self.input_dataset, identifier)  # NOQA
        self.base_command_props['reverse_read_fpath'] = self.input_dataset.item_content_abspath(paired_read_identifier)  # NOQA

    def stage_outputs(self, identifier):
        read1_handle = None
        read2_handle = None
        for filename in self.outputs:

            useful_name = self.input_dataset.get_overlay(
                'useful_name'
            )[identifier]

            fpath = os.path.join(self.working_directory, filename)
            relpath = os.path.join(useful_name, filename)
            out_id = self.output_proto_dataset.put_item(fpath, relpath)
            self.output_proto_dataset.add_item_metadata(
                out_id,
                'from',
                "{}/{}".format(self.input_dataset.uri, identifier)
                )

            # Add is_read1 overlay.
            if filename.find("_1") != -1:
                self.output_proto_dataset.add_item_metadata(
                    out_id,
                    "is_read1",
                    True
                )
                read1_handle = out_id
            else:
                self.output_proto_dataset.add_item_metadata(
                    out_id,
                    "is_read1",
                    False
                )
                read2_handle = out_id

        # Add pair_id overlay.
        self.output_proto_dataset.add_item_metadata(
            read1_handle,
            "pair_id",
            generate_identifier(read2_handle)
        )
        self.output_proto_dataset.add_item_metadata(
            read2_handle,
            "pair_id",
            generate_identifier(read1_handle)
        )

def main():
    args = parse_args()
    with TrimSeqsTrimmomatic(args.input_uri, args.output_uri) as smart_tool:

        smart_tool.base_commands = BASE_COMMANDS
        smart_tool.outputs = OUTPUTS

        smart_tool(args.identifier)


if __name__ == "__main__":
    main()
