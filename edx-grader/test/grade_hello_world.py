from grader import decorators


# @decorators.test
# @decorators.set_description("Adding 1 and 2 should yield 3")
# @decorators.timeout(300)
# def t_1(m):
#     m.stdin.put(2)
#     m.stdin.put(1)
#     assert m.stdout.new() == "3\n"


@decorators.test
@decorators.set_description("Ispisi Hello World!")
@decorators.timeout(250)
def check_hello_world(m):
    assert m.stdout.read() == "Hello World!\n"