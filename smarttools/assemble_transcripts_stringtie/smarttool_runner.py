"""Assemble trabscript using stringtie."""

import os

from smarttoolbase import SmartTool, Command, parse_args


BASE_COMMANDS = [
    Command(
        "stringtie -G {gene_annotation_path} {input_fpath} -o stringtie.bam"
    ),
]
OUTPUTS = ["stringtie.bam"]

class VarScan(SmartTool):

    def pre_run(self, identifier):
        input_fpath = self.input_dataset.item_content_abspath(identifier)

        self.base_command_props.update(
            {'input_fpath': input_fpath}
        )

        self.base_command_props['gene_annotation_path'] = os.environ['GENE_ANNOTATION_PATH']  # NOQA


def main():
    args = parse_args()

    with VarScan(args.input_uri, args.output_uri) as smart_tool:
        smart_tool.base_commands = BASE_COMMANDS
        smart_tool.outputs = OUTPUTS
        smart_tool(args.identifier)



if __name__ == '__main__':
    main()
