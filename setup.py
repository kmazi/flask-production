"""Define setup instructions."""

from setuptools import setup

setup(
    name="Flaskproduction",
    packages=["flaskapp"],
    include_package_data=True,
    install_requires=['flask']
)
