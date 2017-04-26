# -*- coding: utf-8 -*-
from distutils.core import setup
import py2app
import shutil
import os

includes = []
excludes = []
packages = []
datafiles = ["logging.conf", "MyCoder.ini"]

setup(
    app=["Collector.py"],
    name="Collector",
    options={
        "py2app": {
            "iconfile": "app.icns",
            "bdist_base": "dist/build",
        }
    },
    data_files=datafiles,
    setup_requires=["py2app"],
)


