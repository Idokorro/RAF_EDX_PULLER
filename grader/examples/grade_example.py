from grader.grader import decorators

@decorators.test
def test_hello_world(m):
    assert "Hello World\n" in m.stdout.read()