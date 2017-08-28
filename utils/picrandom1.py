import subprocess
import os

os.chdir("tests")
subprocess.call(["tar", "xzf", "data.tar.gz"])
