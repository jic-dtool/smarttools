"""Run bowtie2."""

import os

from smarttoolbase import SmartTool, parse_args, temp_working_dir


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

        self.base_command_props = { 'reference_prefix': os.environ['BOWTIE2_REFERENCE'] }

    def run(self, identifier):

        self.base_command_props['forward_read_fpath'] = self.input_dataset.item_content_abspath(identifier)
        paired_read_identifier = find_paired_read(self.input_dataset, identifier)
        self.base_command_props['reverse_read_fpath'] = self.input_dataset.item_content_abspath(paired_read_identifier)

        with temp_working_dir() as tmp:
            self.base_command_props['output_fpath'] = os.path.join(tmp, 'OUT.sam')

            super(AlignSeqsBowtie2, self).run(identifier)


def main():
    args = parse_args()
    smart_tool = AlignSeqsBowtie2(args.input_uri, args.output_uri)

    smart_tool.base_command = "bowtie2 -x {reference_prefix} -1 {forward_read_fpath} -2 {reverse_read_fpath} -S {output_fpath}"

    smart_tool.base_command_props = {
        "reference_prefix": "/Users/hartleym/data_repo/a_thaliana_ref_with_indexes/data/A_thaliana_indexes",
        "forward_read_fpath": "/tmp/input/data/read1.fq",
        "reverse_read_fpath": "/tmp/input/data/read2.fq",
        "output_fpath": "/tmp/working/output",
    }

    smart_tool.run(args.identifier)


if __name__ == "__main__":
    main()
