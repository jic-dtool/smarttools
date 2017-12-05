"""Quality control of sequencing data using fastqc."""

import os

from smarttoolbase import SmartTool, Command, parse_args


BASE_COMMANDS = [
    Command('fastqc -o {working_directory} {input_fpath}')]


class FastQC(SmartTool):

    def pre_run(self, identifier):
        input_fpath = self.input_dataset.item_content_abspath(identifier)

        self.base_command_props.update(
            {
                'input_fpath': input_fpath,
                'working_directory': self.working_directory,
            }
        )

    def stage_outputs(self, identifier):
        for fname in os.listdir(self.working_directory):
            print(fname)
            fpath = os.path.join(self.working_directory, fname)
            out_id = self.output_proto_dataset.put_item(fpath, fname)
            self.output_proto_dataset.add_item_metadata(
                out_id,
                'from',
                "{}/{}".format(self.input_dataset.uri, identifier)
            )


def main():
    args = parse_args()

    with FastQC(args.input_uri, args.output_uri) as smart_tool:
        smart_tool.base_commands = BASE_COMMANDS
        smart_tool(args.identifier)


if __name__ == '__main__':
    main()
