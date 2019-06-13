import os
import sys
import datetime
import contextlib

from jt64gentc import version_list
from colorconsole import terminal

# process variables
base_path = os.environ["JTSDK_HOME"]
tc_dir = os.path.join(base_path, "tools", "tcfiles")
script_name = os.path.basename(__file__)

# Hamlib base path
hamlib_base_path = os.path.join(base_path, "tools", "hamlib", "qt")
hamlib_base_path = hamlib_base_path.replace('\\', '/')

# other paths
fftw_path = os.environ["fftw3f_dir_f"]
adoc_path = os.environ["ruby_dir_f"]
svn_path = os.environ["svn_dir_f"]


# TODO: Move this to jt64common package
def clear():
    """Clear screen Windows or *Nix"""
    os.system('cls' if os.name == 'nt' else 'clear')


# TODO: Move this to jt64common package
def make_dir():
    """Makes a directory if not exist"""
    if not os.path.exists(tc_dir):
        os.makedirs(tc_dir)


def main():
    """Generates Tool Chain files for each QT version in version_list"""
    clear()
    screen = terminal.get_terminal(conEmu=False)
    print("------------------------------------------------------------")
    screen.set_color(3, 0)
    print(f"JTSDK64 Generate QT Tool Chain Files {os.environ['VERSION']}")
    screen.reset_colors()
    print("------------------------------------------------------------\n")

    # loop through each supported QT version adn generate TC file
    for i in version_list:
        time_now = datetime.datetime.now()
        print(f"* Generating TC File for QT v{i}")
        file_name = "qt" + i.replace(".", "") + ".tc"
        file = os.path.join(tc_dir, file_name)

        # Qt Directory back slash
        qtdir = os.path.join(base_path, "tools", "Qt", i, "mingw73_64", "bin")
        qtdir = qtdir.replace('\\', '/')

        # Set GCCD: both 5.12.2 and 5.12.3 use GCC 730_64
        gccd = os.path.join(base_path, "tools", "Qt", "Tools", "mingw730_64", "bin")
        gccd = gccd.replace('\\', '/')

        hamlib_dir = os.path.join(hamlib_base_path, i)
        hamlib_dir = hamlib_dir.replace('\\', '/')

        # remove file while supressing not found error
        with contextlib.suppress(FileNotFoundError):
            os.remove(file)

        # Open file
        with open(file, "w") as f:
            f.write(f"# -------------------------------------------------------\n")
            f.write(f"# Tool Chain File for Qt {i}\n")
            f.write(f"# This file is auto-generated by : {script_name}\n")
            f.write(f"# Time Stamp: {time_now}\n")
            f.write(f"# --------------------------------------------------------\n")
            f.write(f"\n# System Type and Base Paths\n")
            f.write(f"SET (CMAKE_SYSTEM_NAME Windows)\n")
            f.write(f"SET (QTDIR {qtdir})\n")
            f.write(f"SET (GCCD {gccd}\n")
            f.write(f"\n# Asciidoctor\n")
            f.write(f"SET (ADOCD {adoc_path})\n")
            f.write(f"\n# FFTW\n")
            f.write(f"SET (FFTWD {fftw_path})\n")
            f.write(f"\n# Hamlib\n")
            f.write(f"SET (HLIB {hamlib_dir})\n")
            f.write(f"\n# Subversion\n")
            f.write(f"SET (SVND {svn_path})\n")
            f.write(f"\n# CMake Consolidated variables\n")
            f.write("SET (CMAKE_PREFIX_PATH ${GCCD} ${QTDIR} ${HLIB} ${HLIB}/bin ${ADOCD} ${FFTWD} ${SVND})\n")
            f.write(f"SET (CMAKE_FIND_ROOT_PATH_PROGRAM NEVER)\n")
            f.write(f"SET (CMAKE_FIND_ROOT_PATH_LIBRARY BOTH)\n")
            f.write(f"SET (CMAKE_FIND_ROOT_PATH_INCLUDE BOTH)\n")
            f.write(f"\n# END Cmake Tool Chain File")

        f.close()


if __name__ == '__main__':
    make_dir()
    main()
    sys.exit(0)
