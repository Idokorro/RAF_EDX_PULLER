from grader import decorators


@decorators.test
@decorators.set_description("Adding 1 and 2 should yield 3")
@decorators.timeout(300)
def t_1(m):
    m.stdin.put(2)
    m.stdin.put(1)
    assert m.stdout.new() == "3\n"

#
# @decorators.test
# @decorators.set_description("Adding 3 and 4 should yield 7")
# @decorators.timeout(250)
# def t_2(m):
#     m.stdin.put(3)
#     m.stdin.put(4)
#     assert m.stdout.new() == "7\n"
# @decorators.test
# @decorators.set_description("Ispisi Hello World!")
# @decorators.timeout(250)
# def check_hello_world(m):
#     assert m.stdout.read() == "Hello World!\n"