"""Merge transcript using stringtie.

This scripts merges all the files in the input dataset give any identifier in
the input dataset. It is up to the agent calling this script to ensure that
this smarttool is not called once for every item in the input dataset.
"""

import os

from smarttoolbase import SmartTool, Command, parse_args


BASE_COMMANDS = [
    Command(
        "stringtie --merge -G {gene_annotation_path} {mergelist_fpath} -o stringtie.gtf"
    ),
]
OUTPUTS = ["stringtie.gtf"]

class MergeTranscriptsStringtie(SmartTool):

    def pre_run(self, identifier):

        mergelist_fpath = os.path.join(self.working_directory, "mergelist.txt")
        with open(mergelist_fpath, "w") as fh:
            for i in self.input_dataset.identifiers:
                item_fpath = self.input_dataset.item_content_abspath(i)
                fh.write("{}\n".format(item_fpath))

        self.base_command_props.update(
            {'mergelist_fpath': mergelist_fpath}
        )

        self.base_command_props['gene_annotation_path'] = os.environ['GENE_ANNOTATION_PATH']  # NOQA

    def stage_outputs(self, identifier):
        for filename in self.outputs:

            useful_name = ""

            fpath = os.path.join(self.working_directory, filename)
            relpath = os.path.join(useful_name, filename)
            out_id = self.output_proto_dataset.put_item(fpath, relpath)
            self.output_proto_dataset.add_item_metadata(
                out_id,
                'from',
                "{}".format(self.input_dataset.uri)
                )

def main():
    args = parse_args()

    with MergeTranscriptsStringtie(args.input_uri, args.output_uri) as smart_tool:
        smart_tool.base_commands = BASE_COMMANDS
        smart_tool.outputs = OUTPUTS
        smart_tool(args.identifier)



if __name__ == '__main__':
    main()
