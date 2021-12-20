# coding: utf-8
# @Time : 11/10/21 11:14 AM
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="shino",
    version="0.0.1",
    description="common spider",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hacksman/shino",
    author="hacksman",
    author_email="funblessu@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    entry_points={
        'console_scripts': ['shino = shino.cmdline:execute']
    },
    include_package_data=True,
    install_requires=[
        "requests",
        "loguru",
        "retrying",
        "pymysql",
        "dbutils",
        "glom",
        "redis",
        "furl",
        "arrow",
        "pytz",
        "grpcio-tools",
        "kombu",
        "croniter",
        "schedule",
        "cryptography",
        "lxml",
        "stringcase",
        "sqlalchemy",
        "pymongo",
        "amqp"
    ]
)