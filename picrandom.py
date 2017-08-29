#!/usr/bin/python3
import sys
import time
import os
import threading

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

#spinner = Spinner()
#spinner.start()
# ... some long-running operations
#time.sleep(3)
#spinner.stop()

class Picrandom():
    def __init__(self, argv):
        if len(argv) > 2:
            self.path = None
        elif len(argv) == 2:
            self.path = argv[1]
        else:
            path = os.getcwd()

    def help(self):
        print("Pictures randomizer. It copies 5 random pictures from a")
        print("specified directory to the /tmp. If the path has been omitted")
        print("it will try to find pictures in the current directory.")
        print()
        print("Usage: python %s [/path/to/images]" % sys.argv[0])

    def is_path_correct(self, path):
        return os.path.isdir(path):

    def get_all_files(self, path):
        files_list = []
        for root, dirnames, filenames in os.walk(path):
            subdir_list = [os.path.join(root, filename) for filename in filenames]
            files_list.extend(subdir_list)
        return files_list

    def get_random(self, files_list):
        pass

    def copy(self, files_list):
        pass
    
def main():
    picrandom = Picrandom(sys.argv)
    if not picrandom.path:
        picrandom.help()
        sys.exit(1)
    if not picrandom.is_path_correct(path):
        print("ERROR: Incorrect directory.")
        sys.exit(2)
    files_list = get_all_files(path)

if __name__ == "__main__":
    main()
