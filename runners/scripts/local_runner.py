"""Run all jobs locally."""

import os
import shlex
import subprocess

import yaml
import click

from analysis import Analysis


class LocalRunner(object):

    def __init__(self, analysis):

        self.analysis = analysis
        self.command_base = "python {}".format(
            self.analysis.config["local_smarttool_fpath"]
        )

        smarttool_fpath = self.analysis.config["local_smarttool_fpath"]
        smarttool_dirname = os.path.dirname(smarttool_fpath)
        smarttool_config_file = os.path.join(smarttool_dirname, 'tool.yml')
        with open(smarttool_config_file) as fh:
            self.tool_config = yaml.load(fh)

    def construct_single_process_command(self, identifier):

        command_as_list = shlex.split(self.command_base)

        command_as_list += ['-d', self.analysis.input_dataset.uri]
        command_as_list += ['-o', self.analysis.output_dataset.uri]
        command_as_list += ['-i', identifier]

        return command_as_list

    def process_single_identifier(self, identifier):

        run_env = os.environ.copy()
        if 'env_vars' in self.analysis.config:
            run_env.update(self.analysis.config['env_vars'])

        run_command = self.construct_single_process_command(identifier)
        subprocess.call(run_command, env=run_env)


@click.command()
@click.argument('analysis_fpath')
def main(analysis_fpath):

    analysis = Analysis(analysis_fpath)
    runner = LocalRunner(analysis)

    analysis.initialise()

    for identifier in runner.analysis.identifiers_to_process:
        runner.process_single_identifier(identifier)

    analysis.notes = "\nprocessed with: {}".format(runner.tool_config["name"])
    analysis.notes += "\nenv_vars: '{}'".format(
            analysis.config['env_vars']
        )

    analysis.finalise()

    click.secho("Created: ", nl=False)
    click.secho("{}".format(analysis.output_dataset.uri), fg='green')

if __name__ == '__main__':
    main()
