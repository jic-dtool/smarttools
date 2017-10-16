"""Build the docker images."""

import os
import subprocess

_HERE = os.path.dirname(__file__)
DOCKER_DIR = os.path.join(_HERE, "docker")

def main():
    for docker_subdir in os.listdir(DOCKER_DIR):
        docker_dir = os.path.join(DOCKER_DIR, docker_subdir)
        cmd = [
            "docker",
            "build",
            docker_dir,
            "--tag",  "jicscicomp/{}".format(docker_subdir)
        ]
        subprocess.call(cmd)

if __name__ == "__main__":
    main()
