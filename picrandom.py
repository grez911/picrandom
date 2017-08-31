#!/usr/bin/python3
import sys
import time
import os
import threading
import shutil
import random

class BadDirException(Exception):
    pass

class Spinner:
    def spinning_cursor(self):
        while 1:
            for cursor in "|/-\\": yield cursor

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
            sys.stdout.write("\b")
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
    def __init__(self, argv):
        self.path       = os.getcwd()
        self.files      = set() # here will be set of all available files
        self.bad_files  = 0     # counter for unreadable files
        self.bad_dirs   = 0     # unreadable dirs (have no permission to read)
        self.good_files = 0     # files that are readable
        if len(argv) > 2:
            self.path = None
        elif len(argv) == 2:
            self.path = argv[1]
        if self.path is not None:
            if not os.path.isdir(self.path):
                raise BadDirException("Directory is not correct of not "
                    + "accessible.")

    def help(self):
        print("Pictures randomizer. It copies five random pictures from")
        print("a specified directory to the /tmp/picrandom/. If the path")
        print("has been omitted it will try to find pictures in the")
        print("current directory.")
        print()
        print("Usage: python {} [/path/to/images]".format(sys.argv[0]))

    def scan(self):
        """
        Gets all files from self.path recursively
        """
        for root, dirnames, filenames in os.walk(self.path, followlinks=True):
            subdir = set()
            for filename in filenames:
                _filename = os.path.join(root, filename)
                if os.access(_filename, os.R_OK):
                    subdir.update([_filename])
                    self.good_files += 1
                else:
                    print("Can't read file {}".format(_filename))
                    self.bad_files += 1
            self.files.update(subdir)
            for dirname in dirnames:
                _dirname = os.path.join(root, dirname)
                if not os.access(_dirname, os.R_OK | os.W_OK):
                    print("Can't open directory {}".format(_dirname))
                    self.bad_dirs += 1

    def copy(self, count=5):
        """
        Choses random five files from all files and copies them
        to the /tmp/picrandom/
        """
        # CHECK EXCEPTIONS WHEN CALL THIS FUNCTION!
        if os.path.exists("/tmp/picrandom/"):
            shutil.rmtree("/tmp/picrandom/")
        os.mkdir("/tmp/picrandom/")
        chosen_files = random.sample(self.files, min(count, self.good_files))
        for f in chosen_files:
            new_name = self.choose_new_name(f)
            shutil.copy2(f, "/tmp/picrandom/{}".format(new_name))
    
    def choose_new_name(self, old_name):
        """
        Returns a new name if there is already file with such name
        in the /tmp/picrandom/
        """
        name = self.get_filename(old_name)
        if not os.path.exists("/tmp/picrandom/{}".format(name)):
            return name

        i = 0
        while True:
            new_name = "{}_{}".format(i, name)
            # crop filename if too big
            new_name[:os.pathconf("/tmp/picrandom/", "PC_NAME_MAX")]
            if os.path.exists("/tmp/picrandom/{}".format(new_name)):
                i += 1
            else:
                return new_name

    def get_filename(self, full_name):
        """
        Returns name from full name
        E.g.: get_file_name("/home/user/test.txt") == "test.txt"
        """
        return full_name.split("/")[-1]

def main():
    #spinner = Spinner()
    #spinner.start()
    # ... some long-running operations
    #time.sleep(3)
    #spinner.stop()

    # MAKE CHECK FOR PYTHON VERSION!

    picrandom = Picrandom(sys.argv)
    picrandom.scan()
    picrandom.copy()
#    if not picrandom.path:
#        picrandom.help()
#        sys.exit(1)
#    if not picrandom.is_path_correct(path):
#        print("ERROR: Incorrect directory.")
#        sys.exit(2)
#    files_list = get_all_files(path)

if __name__ == "__main__":
    main()
