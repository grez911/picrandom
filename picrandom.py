#!/usr/bin/python3
import sys
import time
import os
import threading

class BadDirException(Exception):
    pass

class Spinner:
    def spinning_cursor(self):
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.busy = False
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
    def __init__(self, argv):
        self.path = os.getcwd()
        self.files = set()  # here will be set of all available files
        self.bad_files = 0  # counter for unreadable files
        self.bad_dirs = 0   # unreadable dirs (have no permission to read)
        if len(argv) > 2:
            self.path = None
        elif len(argv) == 2:
            self.path = argv[1]
        if self.path is not None:
            if not os.path.isdir(self.path):
                raise BadDirException("Directory is not correct of not \
                        accessible.")

    def help(self):
        print("Pictures randomizer. It copies 5 random pictures from a")
        print("specified directory to the /tmp. If the path has been omitted")
        print("it will try to find pictures in the current directory.")
        print()
        print("Usage: python %s [/path/to/images]" % sys.argv[0])

    def scan(self):
        for root, dirnames, filenames in os.walk(self.path, followlinks=True):
            subdir = set()
            for filename in filenames:
                _filename = os.path.join(root, filename)
                if os.access(_filename, os.R_OK):
                    subdir.update([_filename])
                else:
                    print("Can't read file %s" % _filename)
                    self.bad_files += 1
            self.files.update(subdir)
            for dirname in dirnames:
                _dirname = os.path.join(root, dirname)
                if not os.access(_dirname, os.R_OK | os.W_OK):
                    print("Can't open directory %s" % _dirname)
                    self.bad_dirs += 1

    def get_random(self, files_list):
        pass

    def copy(self, files_list):
        pass
    
def main():
    #spinner = Spinner()
    #spinner.start()
    # ... some long-running operations
    #time.sleep(3)
    #spinner.stop()

    # MAKE CHECK FOR VERSION!

    picrandom = Picrandom(sys.argv)
#    if not picrandom.path:
#        picrandom.help()
#        sys.exit(1)
#    if not picrandom.is_path_correct(path):
#        print("ERROR: Incorrect directory.")
#        sys.exit(2)
#    files_list = get_all_files(path)

if __name__ == "__main__":
    main()
