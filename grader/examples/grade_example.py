from grader.decorators import *


@test
def test_hello_world(m):
    assert "Hello World" in m.stdout.read()
