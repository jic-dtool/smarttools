"""Run bowtie2."""

from smarttoolbase import SmartTool, parse_args


class AlignSeqsBowtie2(SmartTool):
    pass

def main():
    args = parse_args()
    smart_tool = AlignSeqsBowtie2(args.input_uri, args.output_uri)
    smart_tool.run()


if __name__ == "__main__":
    main()
