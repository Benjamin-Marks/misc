"""dir_cleanup.py [-dir DIR] [-t T] [-rf] [-v]
Search directory (default cwd), remove files unmodified for T hours (default 72)
"""


import os
import sys
import time
import argparse


__author__ = "Ben Marks"


CONST_DEFAULT_HOURS = 72


def is_pos(v):
    num = int(v)
    if num < 1:
        raise argparse.ArgumentTypeError("%s must be non-zero positive int" % v)
    return num


def main(argv):
    """Gets command line parameters and calls file removal"""

    parser = argparse.ArgumentParser(usage="%(prog)s [-dir DIR] [-t T] [-rf] [-v]",
        description="Search directory (default cwd), remove files unmodified "
        "for T hours (default 72)")

    parser.add_argument("-dir", default=os.getcwd,
        help="directory from which to delete files")
    parser.add_argument("-t", type=is_pos, default=CONST_DEFAULT_HOURS,
        help="delete files T hours since modification")
    parser.add_argument("-rf", action="store_true",
        help="Do recursive file removal WARNING: DO NOT USE")
    parser.add_argument("-v", "--verbose", action="store_true",
        help="verbose: list files removed",)
    args = parser.parse_args()

    #Begin removal
    remove_files(args.dir, args.t, args.rf, args.verbose)


def remove_files(cur_dir, hours, do_recur, verbose):
    """Clears old files, recurses into sub-folders if requested"""
    cur_time = time.time()

    #Go through files in current directory
    for file_ in os.listdir(cur_dir):
        path = os.path.join(cur_dir, file_)

        #Check file age, delete if too old -- 3600 converts seconds to hours
        # TODO: Check if dir is readable/writeable?
        if cur_time - os.path.getmtime(path) > 3600 * hours: 
            if os.path.isfile(path):
                if verbose:
                    print(path)
                os.remove(path)
            elif do_recur and os.path.isdir(path):
                remove_files(path, hours, do_recur, verbose)

if __name__ == "__main__":
    main(sys.argv[1:])
