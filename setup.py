from setuptools import setup
from setuptools import find_packages
import os
import re


with open("README.md", "r") as fs:
    long_description = fs.read()


def find_version(*file_paths):
    """
    This pattern was modeled on a method from the Python Packaging User Guide:
        https://packaging.python.org/en/latest/single_source_version.html
    We read instead of importing so we don't get import errors if our code
    imports from dependencies listed in install_requires.
    """
    base_module_file = os.path.join(*file_paths)
    with open(base_module_file) as f:
        base_module_data = f.read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", base_module_data, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name="nornir_arista",
    version=find_version("nornir_arista", "__init__.py"),
    description="Python library to interact with Arista devices. Based on Arista EAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vicnz03/nornir_arista",
    author="Vic Chen",
    author_email="vicnz03@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
    install_requires=[
        "pyeapi>=1.0.2",
    ],
)