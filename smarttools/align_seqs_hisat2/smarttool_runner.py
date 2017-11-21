"""Run hisat2."""

import os

from smarttoolbase import SmartTool, Command, parse_args

BASE_COMMANDS = [
    Command("hisat2 --dta -x {reference_prefix} -1 {forward_read_fpath} -2 {reverse_read_fpath} -S OUT.sam"),  # NOQA
    Command("samtools sort OUT.sam -o OUT.bam"),
]

OUTPUTS = [
    'OUT.bam',
]


def find_paired_read(dataset, identifier):
    pair_id = dataset.get_overlay('pair_id')
    return pair_id[identifier]


class AlignSeqsHisat2(SmartTool):

    def pre_run(self, identifier):

        self.base_command_props['reference_prefix'] = os.environ['HISAT2_REFERENCE']  # NOQA
        self.base_command_props['forward_read_fpath'] = self.input_dataset.item_content_abspath(identifier)  # NOQA
        paired_read_identifier = find_paired_read(self.input_dataset, identifier)  # NOQA
        self.base_command_props['reverse_read_fpath'] = self.input_dataset.item_content_abspath(paired_read_identifier)  # NOQA


def main():
    args = parse_args()
    with AlignSeqsHisat2(args.input_uri, args.output_uri) as smart_tool:

        smart_tool.base_commands = BASE_COMMANDS
        smart_tool.outputs = OUTPUTS

        smart_tool(args.identifier)


if __name__ == "__main__":
    main()
