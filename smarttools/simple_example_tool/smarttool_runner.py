
from smarttoolbase import SmartTool, parse_args


BASE_COMMAND = 'head -n 4 {input_fpath}'

class SimpleExampleTool(SmartTool):

    def pre_run(self, identifier):
        input_fpath = self.input_dataset.item_content_abspath(identifier)

        self.base_command_props.update(
            {'input_fpath': input_fpath}
        )


def main():
    args = parse_args()

    with SimpleExampleTool(args.input_uri, args.output_uri) as smart_tool:
        smart_tool.base_command = BASE_COMMAND
        smart_tool(args.identifier)




if __name__ == '__main__':
    main()
