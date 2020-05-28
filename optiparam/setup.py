import os

from setuptools import find_packages, setup

VERSION = "0.1"

build_number = os.environ.get("OPTIPARAM_BUILD_NUMBER")
if build_number is not None:
    VERSION += ".{}".format(build_number)

local_version = os.environ.get("OPTIPARAM_LOCAL_VERSION")
if local_version is not None:
    VERSION += "+{}".format(local_version)

PACKAGE_NAME = "optiparam"


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas==1.0.0",
        "pathlib==1.0.1",
        "scipy",
        "Click==7.0",
    ],
    entry_points={
        "console_scripts": [
            "optiparam = optiparam.opt:main",
        ]
    },

)
