"""Run bowtie2."""

import os

from smarttoolbase import SmartTool, Command, parse_args

BASE_COMMANDS = [
    Command("bowtie2 -x {reference_prefix} -1 {forward_read_fpath} -2 {reverse_read_fpath} -S {output_fpath}"),  # NOQA
    Command("samtools view -bS OUT.sam -o OUT.bam"),
    Command("samtools sort OUT.bam -o OUT.sorted.bam"),
    Command("samtools index OUT.sorted.bam OUT.sorted.bai"),
]

OUTPUTS = [
    'OUT.sorted.bam',
    'OUT.sorted.bai',
]


def find_paired_read(dataset, identifier):
    pair_id = dataset.get_overlay('pair_id')
    return pair_id[identifier]


class AlignSeqsBowtie2(SmartTool):

    def pre_run(self, identifier):

        self.base_command_props['reference_prefix'] = os.environ['BOWTIE2_REFERENCE']  # NOQA
        self.base_command_props['forward_read_fpath'] = self.input_dataset.item_content_abspath(identifier)  # NOQA
        paired_read_identifier = find_paired_read(self.input_dataset, identifier)  # NOQA
        self.base_command_props['reverse_read_fpath'] = self.input_dataset.item_content_abspath(paired_read_identifier)  # NOQA
        self.base_command_props['output_fpath'] = os.path.join(self.working_directory, 'OUT.sam')  # NOQA


def main():
    args = parse_args()
    with AlignSeqsBowtie2(args.input_uri, args.output_uri) as smart_tool:

        smart_tool.base_commands = BASE_COMMANDS
        smart_tool.outputs = OUTPUTS

        smart_tool(args.identifier)


if __name__ == "__main__":
    main()
