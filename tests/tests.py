import * from picrandom

def test_get_path():
    assert get_path(["picrandom.py", "/"]) == "/"
    assert get_path(["picrandom.py", "/home"]) == "/home"
    assert get_path(["picrandom.py", "/home/"]) == "/home/"
    assert get_path(["picrandom.py", "tests/"]) == "tests/"
    assert get_path(["picrandom.py", "tests"]) == "tests"
    assert get_path(["picrandom.py", "tests/Test"]) == "tests/Test"
