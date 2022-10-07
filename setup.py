import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "path": sys.path,
    "packages": ["requests", "riot_auth", "InquirerPy"],
    "excludes": ["tkinter", "test", "unittest", "pygments", "xmlrpc"]
}

setup(
    name="some VALORANT thing",
    version="0.1",
    description="sVt - some VALORANT thing",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", target_name="sVt.exe")],
)
