"""Build the docker images."""

import os
import subprocess

_HERE = os.path.dirname(__file__)
DOCKER_DIR = os.path.join(_HERE, "docker")

def build_docker_images():
    for docker_subdir in os.listdir(DOCKER_DIR):
        docker_dir = os.path.join(DOCKER_DIR, docker_subdir)
        if not os.path.isdir(docker_dir):
            continue
        cmd = [
            "docker",
            "build",
            docker_dir,
            "--tag",  "jicscicomp/{}".format(docker_subdir)
        ]
        subprocess.call(cmd)

if __name__ == "__main__":
    build_docker_images()
