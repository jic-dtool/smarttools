"""Run bowtie2."""

import os

from smarttoolbase import SmartTool, parse_args


def find_paired_read(dataset, identifier):

    illumina_metadata = dataset.get_overlay('illumina_metadata')

    specific_metadata = illumina_metadata[identifier]

    del specific_metadata['read']

    matched_identifiers = []

    # Find all items in the dataset where the illumina metadata matches except
    # for the read tag
    for candidate_id in dataset.identifiers:
        candidate_metadata = illumina_metadata[candidate_id]
        if candidate_metadata is not None:
            if all(
                (candidate_metadata[k] == v)
                for k, v, in specific_metadata.items()
            ):
                matched_identifiers.append(candidate_id)

    # This should be exactly two items
    assert len(matched_identifiers) == 2

    matched_identifiers.remove(identifier)

    return matched_identifiers[0]


class AlignSeqsBowtie2(SmartTool):

    def __init__(self, input_uri, output_uri):

        super(AlignSeqsBowtie2, self).__init__(input_uri, output_uri)

        self.base_command_props = {
            'reference_prefix': os.environ['BOWTIE2_REFERENCE']
        }

    def pre_run(self, identifier):

        self.base_command_props['forward_read_fpath'] = self.input_dataset.item_content_abspath(identifier)  # NOQA
        paired_read_identifier = find_paired_read(self.input_dataset, identifier)  # NOQA
        self.base_command_props['reverse_read_fpath'] = self.input_dataset.item_content_abspath(paired_read_identifier)  # NOQA
        self.base_command_props['output_fpath'] = os.path.join(self.working_directory, 'OUT.sam')  # NOQA


def main():
    args = parse_args()
    with AlignSeqsBowtie2(args.input_uri, args.output_uri) as smart_tool:

        smart_tool.base_commands = [
            "bowtie2 -x {reference_prefix} -1 {forward_read_fpath} -2 {reverse_read_fpath} -S {output_fpath}",  # NOQA
            "samtools view -bS OUT.sam -o OUT.bam",
            "samtools sort OUT.bam -o OUT.sorted.bam",
            "samtools index OUT.sorted.bam OUT.sorted.bai",
        ]

        smart_tool.outputs = [
            'OUT.sorted.bam',
            'OUT.sorted.bai',
        ]

        smart_tool(args.identifier)


if __name__ == "__main__":
    main()
