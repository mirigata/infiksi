import os.path


def _load_fixture(fixture):
    with open(os.path.join(os.path.dirname(__file__), "fixtures", fixture)) as f:
        return f.read()
