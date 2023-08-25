import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
packages = ["pandas", "numpy", "sklearn"]
# files = ["./app/client/assets/", "./app/client/model/", "./app/client/service/"]
build_exe_options = {
    "excludes": ["pyinstaller", "unittest"],
    "packages": packages,
    # "include_files": files,
    # "zip_include_packages": ["encodings", "PySide6"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

main_file = "./main.py"
setup(
    name="smaglator",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[Executable(main_file, base=base)],
)
