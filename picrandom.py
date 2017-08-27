import sys
import os

def help():
    print("Picture randomizer. It copies 5 random pictures from a specified")
    print("directory to the /tmp. If the path has been omitted it will try")
    print("to find pictures in the current directory.")
    print()
    print("Usage: python %s [/path/to/images]" % sys.argv[0])

def get_path(args):
    if len(args) > 2:
        path = None
    elif len(args) == 2:
        path = args[1]
    else:
        path = os.getcwd()
    return path
        
def is_path_correct(path):
    return os.path.isdir(path):

def get_all_files(path):
    files_list = []
    for root, dirnames, filenames in os.walk(path):
        subdir_list = [os.path.join(root, filename) for filename in filenames]
        files_list.extend(subdir_list)
    return files_list

def get_random_five(files_list):
    
    
def main():
    path = get_path(sys.argv)
    if not path:
        help()
        sys.exit(1)
    if not is_path_correct(path):
        print("ERROR: Incorrect directory.")
        sys.exit(2)
    files_list = get_all_files(path)

if __name__ == "__main__":
    main()
