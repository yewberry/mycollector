# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe
import shutil
import os
import glob

# Remove the build folder
shutil.rmtree("build", ignore_errors=True)
# Remove the dist folder
shutil.rmtree("dist", ignore_errors=True)

data_files = []
includes = []
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll',
                'MSVCP90.dll', 'mswsock.dll', 'powrprof.dll']
msCrtDll = glob.glob(r".\etc\Microsoft.VC90.CRT\*.*")
# install the MSVC 9 runtime dll
data_files += [("Microsoft.VC90.CRT", msCrtDll)]

# --------------------------- APP CONFIG --------------------------------------
_name = "Collector"
app_version = "1.0"
app_name = _name
app_script = "%s.py" % _name
app_company = ""
app_copyright = ""
icon_resources = [(1, "./etc/app.ico")]
bitmap_resources = []
other_resources = []
# data_files += ["%s.ini" % _name, ("logs", "")]
data_files += []
# -----------------------------------------------------------------------------

setup(
    options={
        "py2exe": {
            "compressed": 1,
            # 0 = don’t optimize (generate .pyc) 1 = normal optimization (like python -O)
            # 2 = extra optimization (like python -OO)
            "optimize": 0,
            "includes": includes,
            "excludes": excludes,
            "packages": packages,
            "dll_excludes": dll_excludes,
            # 3 = don't bundle (default) 2 = bundle everything but the Python interpreter
            # 1 = bundle everything, including the Python interpreter
            "bundle_files": 1,
            "dist_dir": "dist",
            "xref": False,
            "skip_archive": False,
            "ascii": False,
            "custom_boot_script": '',
        }
    },
    data_files=data_files,
    # use console if you want
    windows=[{
        "version": app_version,
        "name": app_name,
        "script": app_script,
        "company_name": app_company,
        "copyright": app_copyright,
        "icon_resources": icon_resources,
        "bitmap_resources": bitmap_resources,
        "other_resources": other_resources,
    }], zipfile=None
)

# don't need support win9x
os.remove(".\dist\w9xpopen.exe")


