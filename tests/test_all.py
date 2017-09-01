#!/usr/bin/python3
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from picrandom import *

def test_init():
    assert Picrandom("/").dir == "/"
    assert Picrandom("tests").dir == "tests"
    assert Picrandom("tests/").dir == "tests/"
    assert Picrandom("tests/..").dir == "tests/.."
    assert Picrandom("tests/.").dir == "tests/."
    assert Picrandom("..").dir == ".."
    assert Picrandom(".").dir == "."
    assert Picrandom("tests/data/symlinks/2").dir == "tests/data/symlinks/2"
    with pytest.raises(BadDirException):
        Picrandom("tests/data/symlinks/3/test3.txt").dir
    with pytest.raises(BadDirException):
        Picrandom("tests/data/permissions/7/test.txt").dir
    with pytest.raises(BadDirException):
        Picrandom("gh87g56hg8h5gnb").dir
    with pytest.raises(BadDirException):
        Picrandom("").dir

def test_scan():
    picrandom = Picrandom("tests/data/complex_names/")
    picrandom.scan()
    assert picrandom.good_files == 661

    picrandom = Picrandom("tests/data/permissions/")
    picrandom.scan()
    assert picrandom.good_files == 6
    assert picrandom.bad_dirs == 7
    assert picrandom.bad_files == 4

    picrandom = Picrandom("tests/data/depth/")
    picrandom.scan()
    assert picrandom.good_files == 3

    picrandom = Picrandom("tests/data/depth")
    picrandom.scan()
    assert picrandom.good_files == 3

    picrandom = Picrandom("tests/data/depth/depth/")
    picrandom.scan()
    assert picrandom.good_files == 2

    picrandom = Picrandom("tests/data/depth/depth/.")
    picrandom.scan()
    assert picrandom.good_files == 2
    
    picrandom = Picrandom("tests/data/depth/depth/./")
    picrandom.scan()
    assert picrandom.good_files == 2

    picrandom = Picrandom("tests/data/depth/depth/./.")
    picrandom.scan()
    assert picrandom.good_files == 2

    picrandom = Picrandom("tests/data/depth/depth/depth/..")
    picrandom.scan()
    assert picrandom.good_files == 2

    picrandom = Picrandom("tests/data/depth/depth/depth/../..")
    picrandom.scan()
    assert picrandom.good_files == 3

def test_prepare_folder():
    picrandom = Picrandom(".")
    picrandom.prepare_folder("tests/data/prepare_test/picrandom")
    assert len(os.listdir("tests/data/prepare_test/picrandom")) == 0
    picrandom.prepare_folder("tests/data/prepare_test/1/picrandom")
    assert len(os.listdir("tests/data/prepare_test/1/picrandom")) == 0
    picrandom.prepare_folder("tests/data/prepare_test/2/picrandom")
    assert len(os.listdir("tests/data/prepare_test/2/picrandom")) == 0
    picrandom.prepare_folder("tests/data/prepare_test/3/picrandom")
    assert len(os.listdir("tests/data/prepare_test/3/picrandom")) == 0

def test_copy():
    picrandom = Picrandom("tests/data/depth/")
    picrandom.scan()
    picrandom.copy()
    assert set(os.listdir("/tmp/picrandom")) \
            == {"0_test.txt", "1_test.txt", "test.txt"}

    picrandom = Picrandom("tests/data/complex_names")
    picrandom.scan()
    picrandom.copy(1000)
    assert len(os.listdir("/tmp/picrandom")) == 661

    picrandom = Picrandom("tests/data/long_names")
    picrandom.scan()
    picrandom.copy()
    assert len(os.listdir("/tmp/picrandom")) == 3

    picrandom = Picrandom("tests/data/symlinks")
    picrandom.scan()
    picrandom.copy()
    assert set(os.listdir("/tmp/picrandom")) \
            == {"0_test.txt", "test.txt", "test3.txt"}

    picrandom = Picrandom("tests/data/symlinks/3/")
    picrandom.scan()
    picrandom.copy()
    assert set(os.listdir("/tmp/picrandom")) == {"test3.txt"}

    picrandom = Picrandom("tests/data/permissions")
    picrandom.scan()
    picrandom.copy(20)
    assert set(os.listdir("/tmp/picrandom")) \
            == {"4.txt", "5.txt", "6.txt", "7.txt", "77.txt", "55.txt"}

    picrandom = Picrandom("tests/data/empty")
    picrandom.scan()
    picrandom.copy()
    assert set(os.listdir("/tmp/picrandom")) == set()
