from pathlib import Path
from setuptools import setup, find_packages

README = (Path(__file__).parent / "README.md").read_text()

REQUIRED = [
        "bs4",
        "pandas",
        "numpy"
]

setup(
    name='clued',
    version='0.1',
    description="Personal library of Python tools",
    long_description=README,
    long_description_content_type="text/markdown",
    url = "https://github.com/chrisluedtke/clued",
    packages=find_packages(),
    author="Chris Luedtke",
    install_requires=REQUIRED,
)
