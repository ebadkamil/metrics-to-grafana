import os.path as osp
import re

from setuptools import find_packages, setup


def find_version():
    with open(osp.join("metrics_to_grafana", "__init__.py"), "r") as f:
        match = re.search(r'^__version__ = "(\d+\.\d+\.\d+)"', f.read(), re.M)
        if match is not None:
            return match.group(1)
        raise RuntimeError("Unable to find version string.")


setup(
    name="metrics-to-grafana",
    version=find_version(),
    author="Ebad Kamil",
    author_email="ebad.kamil@ess.eu",
    maintainer="Ebad Kamil",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "start_load_publisher = metrics_to_grafana.load_publisher:start_load_publisher",
        ],
    },
    install_requires=[
        "graphyte>=1.7.0",
        "psutil",
        "rich>=10.6.0",
        "black==20.8b1",
        "flake8==3.8.4",
        "isort==5.7.0",
    ],
    python_requires=">=3.6",
)
