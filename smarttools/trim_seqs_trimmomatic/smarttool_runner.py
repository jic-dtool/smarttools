"""Run trimmomatic.

The trimmers are specified using the TRIMMOMATIC_TRIMMERS environment variable,
e.g.:

export TRIMMOMATIC_TRIMMERS="ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"
"""

import os

from smarttoolbase import SmartTool, Command, parse_args

BASE_COMMANDS = [
    Command("trimmomatic PE {forward_read_fpath} {reverse_read_fpath} read_1.fq.gz read_2.fq.gz {trimmers}"),  # NOQA
]

OUTPUTS = [
    'read_1.fq.gz',
    'read_2.fq.gz',
]


def find_paired_read(dataset, identifier):
    pair_id = dataset.get_overlay('pair_id')
    return pair_id[identifier]


class TrimSeqsTrimmomatic(SmartTool):

    def pre_run(self, identifier):

        self.base_command_props['trimmers'] = os.environ['TRIMMOMATIC_TRIMMERS']  # NOQA
        self.base_command_props['forward_read_fpath'] = self.input_dataset.item_content_abspath(identifier)  # NOQA
        paired_read_identifier = find_paired_read(self.input_dataset, identifier)  # NOQA
        self.base_command_props['reverse_read_fpath'] = self.input_dataset.item_content_abspath(paired_read_identifier)  # NOQA

    def stage_outputs(self, identifier):
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
            else:
                self.output_proto_dataset.add_item_metadata(
                    out_id,
                    "is_read1",
                    False
                )

def main():
    args = parse_args()
    with TrimSeqsTrimmomatic(args.input_uri, args.output_uri) as smart_tool:

        smart_tool.base_commands = BASE_COMMANDS
        smart_tool.outputs = OUTPUTS

        smart_tool(args.identifier)


if __name__ == "__main__":
    main()
