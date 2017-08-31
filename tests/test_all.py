#!/usr/bin/python3
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from picrandom import *

def test_init():
    assert Picrandom(["./picrandom.py", "/"]).path == "/"
    assert Picrandom(["./picrandom.py", "tests"]).path == "tests"
    assert Picrandom(["./picrandom.py", "tests/"]).path == "tests/"
    assert Picrandom(["./picrandom.py", "tests/.."]).path == "tests/.."
    assert Picrandom(["./picrandom.py", "tests/."]).path == "tests/."
    assert Picrandom(["./picrandom.py", ".."]).path == ".."
    assert Picrandom(["./picrandom.py", "."]).path == "."
    assert Picrandom(["fnoisiubnrbtroktv3", "."]).path == "."
    assert Picrandom(["./picrandom.py", ".", "."]).path == None
    assert Picrandom(["./picrandom.py"]).path == os.getcwd()
    assert Picrandom(["./picrandom.py", "tests/data/symlinks/2"]).path \
        == "tests/data/symlinks/2"
    with pytest.raises(BadDirException):
        Picrandom(["./picrandom.py", "tests/data/symlinks/3/test3.txt"]).path
    with pytest.raises(BadDirException):
        Picrandom(["./picrandom.py", "tests/data/permissions/7/test.txt"]).path
    with pytest.raises(BadDirException):
        Picrandom(["./picrandom.py", "gh87g56hg8h5gnb"]).path

def test_scan():
    picrandom = Picrandom(["./picrandom.py", "tests/data/complex_names/"])
    picrandom.scan()
    assert picrandom.good_files == 661

    picrandom = Picrandom(["./picrandom.py", "tests/data/permissions/"])
    picrandom.scan()
    assert picrandom.good_files == 6
    assert picrandom.bad_dirs == 7
    assert picrandom.bad_files == 6

    picrandom = Picrandom(["./picrandom.py", "tests/data/depth/"])
    picrandom.scan()
    assert picrandom.good_files == 3

    picrandom = Picrandom(["./picrandom.py", "tests/data/depth"])
    picrandom.scan()
    assert picrandom.good_files == 3

    picrandom = Picrandom(["./picrandom.py", "tests/data/depth/depth/"])
    picrandom.scan()
    assert picrandom.good_files == 2

    picrandom = Picrandom(["./picrandom.py", "tests/data/depth/depth/."])
    picrandom.scan()
    assert picrandom.good_files == 2
    
    picrandom = Picrandom(["./picrandom.py", "tests/data/depth/depth/./"])
    picrandom.scan()
    assert picrandom.good_files == 2

    picrandom = Picrandom(["./picrandom.py", "tests/data/depth/depth/./."])
    picrandom.scan()
    assert picrandom.good_files == 2

    picrandom = Picrandom(["./picrandom.py",
        "tests/data/depth/depth/depth/.."])
    picrandom.scan()
    assert picrandom.good_files == 2

    picrandom = Picrandom(["./picrandom.py", 
        "tests/data/depth/depth/depth/../.."])
    picrandom.scan()
    assert picrandom.good_files == 3

def test_get_filename():
    picrandom = Picrandom(["./picrandom.py", "/"])
    assert picrandom.get_filename("/test.txt") == "test.txt"
    assert picrandom.get_filename("test.txt") == "test.txt"
    assert \
        picrandom.get_filename("tests/data/permissions/test.txt") == "test.txt"

def test_copy():
    picrandom = Picrandom(["./picrandom.py", "tests/data/depth/"])
    picrandom.scan()
    picrandom.copy()
    assert set(os.listdir("/tmp/picrandom")) \
            == {"0_test.txt", "1_test.txt", "test.txt"}

    picrandom = Picrandom(["./picrandom.py", "tests/data/complex_names"])
    picrandom.scan()
    picrandom.copy(1000)
    assert len(os.listdir("/tmp/picrandom")) == 661
