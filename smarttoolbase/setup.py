from setuptools import setup

url = ""
version = "0.1.0"
readme = open('README.rst').read()

setup(
    name="smarttoolbase",
    packages=["smarttoolbase"],
    version=version,
    description="Base classes for making Smart tools",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@jic.ac.uk",
    url=url,
    install_requires=[
        "dtoolcore",
    ],
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
