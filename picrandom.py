#!/usr/bin/python3
# Project page: https://github.com/grez911/picrandom

import sys
import time
import os
import threading
import shutil
import random
import argparse
import platform

class BadDirException(Exception):
    pass

class Spinner:
    def spinning_cursor(self):
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.busy  = False
        self.delay = 0.2
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        t = threading.Thread(target=self.spinner_task)
        t.daemon = True
        t.start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)

class Picrandom():
    def __init__(self, dir):
        self.files      = set() # here will be set of all available files
        self.bad_files  = 0     # counter for unreadable files
        self.bad_dirs   = 0     # unreadable dirs (have no permission to read)
        self.good_files = 0     # files that are readable
        self.dir        = dir   # search path
        if not os.path.isdir(self.dir):
            raise BadDirException("Directory is not correct or "
                + "not accessible.")

    def scan(self):
        """
        Gets all files from self.dir recursively
        """
        for root, dirnames, filenames in os.walk(self.dir, followlinks=True):
            subdir = set()
            for filename in filenames:
                _filename = os.path.join(root, filename)
                if os.access(_filename, os.R_OK):
                    subdir.update([_filename])
                    self.good_files += 1
                else:
                    if os.access(root, os.R_OK | os.X_OK):
                        print("\rCan't read file {}".format(_filename))
                        self.bad_files += 1
            self.files.update(subdir)
            for dirname in dirnames:
                _dirname = os.path.join(root, dirname)
                if not os.access(_dirname, os.R_OK | os.X_OK):
                    print("\rCan't open directory {}".format(_dirname))
                    self.bad_dirs += 1

    def copy(self, count=5):
        """
        Choses random five files from all files and copies them
        to the /tmp/picrandom/
        """
        self.prepare_folder()
        chosen_files = random.sample(self.files, min(count, self.good_files))
        for f in chosen_files:
            new_name = self.choose_new_name(f)
            shutil.copy2(f, "/tmp/picrandom/{}".format(new_name))
    
    def choose_new_name(self, old_name):
        """
        Returns a new name if there is already file with such name
        in the /tmp/picrandom/
        """
        name = os.path.basename(old_name)
        if not os.path.exists("/tmp/picrandom/{}".format(name)):
            return name

        i = 0
        while True:
            new_name = "{}_{}".format(i, name)
            # crop filename if too big
            new_name = new_name[:os.pathconf("/tmp/picrandom/", 'PC_NAME_MAX')]
            if os.path.exists("/tmp/picrandom/{}".format(new_name)):
                i += 1
            else:
                return new_name

    def prepare_folder(self, path="/tmp/picrandom/"):
        """
        Deletes an existing file or a folder from a specified path
        and creates an empty folder
        """
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        os.mkdir(path)

def main():
    if sys.version_info < (3, 0):
        print("Python 2 is not supported, it will retire "
            + "soon, see: https://pythonclock.org/")
        sys.exit()

    if 'LINUX' not in platform.system().upper():
        print("Linux only, sorry.")
        sys.exit()

    spinner = Spinner()
    parser = argparse.ArgumentParser(description="Recursively scans a provided"
        + " path and copies five random files to the /tmp/picrandom/")
    parser.add_argument('dir', nargs='?', default=os.getcwd(),
        help="The search path. It will be the current folder if not specified")
    args = parser.parse_args()
    try:
        picrandom = Picrandom(args.dir)
        spinner.start()
        picrandom.scan()
        spinner.stop()
        print("\rTotal number of files: {}".format(picrandom.good_files))
        picrandom.copy()
        print("{} files copied to /tmp/picrandom/"\
            .format(min(5, picrandom.good_files)))
    except Exception as err:
        print("ERROR: {}".format(err))
        sys.exit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.exit()
