"""Script for building Smart tools."""

import click

from build_utils.build_docker_images import build_docker_images
from build_utils.build_smarttool_image import build_smarttool_image

@click.command()
@click.argument('tool_dir')
def main(tool_dir):
    build_docker_images()
    build_smarttool_image(tool_dir)

if __name__ == "__main__":
    main()
