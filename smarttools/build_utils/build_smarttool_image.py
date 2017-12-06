"""Build a single smartool image."""

import os
import subprocess

import yaml

docker_template = """
FROM {docker_base_image}

{docker_snippet}

ADD {tool_python_url} /scripts/
"""


def build_smarttool_image(tool_dir):

    tool_file = os.path.join(tool_dir, 'tool.yml')
    tool_python_url_bits =  [
        'https://raw.githubusercontent.com/',
        'jic-dtool/smarttools/master/smarttools/smarttools/',
        os.path.basename(tool_dir),
        '/smarttool_runner.py'
    ]
    tool_python_url = "".join(tool_python_url_bits)

    with open(tool_file) as fh:
        tool_description = yaml.load(fh)

    smarttool_script = os.path.join(tool_dir, 'smarttool_runner.py')
    tool_description.update(
        {'tool_python_url': tool_python_url}
    )

    dockerfile_contents = docker_template.format(**tool_description)

    build_command = [
        'docker', 'build',
        '-t', 'jicscicomp/{}'.format(tool_description['name']),
        '-'
    ]

    p = subprocess.Popen(build_command, stdin=subprocess.PIPE)
    p.communicate(dockerfile_contents)


