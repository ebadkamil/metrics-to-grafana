import os.path as osp
import re
import sys

from setuptools import find_packages, setup


def find_version():
    with open(osp.join("metrics_to_grafana", "__init__.py"), "r") as f:
        match = re.search(r'^__version__ = "(\d+\.\d+\.\d+)"', f.read(), re.M)
        if match is not None:
            return match.group(1)
        raise RuntimeError("Unable to find version string.")


def get_readme_content():
    basedir = osp.dirname(osp.realpath(sys.argv[0]))
    with open(osp.join(basedir, "README.md"), "r") as f:
        content = f.read()
    return content


setup(
    name="metrics-to-grafana",
    version=find_version(),
    author="Ebad Kamil",
    author_email="ebad.kamil@ess.eu",
    maintainer="Ebad Kamil",
    description="Simple graphite publisher that publishes CPU load and memory to a graphite server",
    long_description=get_readme_content(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "start_load_publisher = metrics_to_grafana.load_publisher:start_load_publisher",
        ],
    },
    install_requires=[
        "graphyte>=1.7.0",
        "psutil",
        "black==20.8b1",
        "flake8==3.8.4",
        "isort==5.7.0",
    ],
    python_requires=">=3.6",
)
