https://habr.com/post/141411/
https://habr.com/post/141501/

sum = 122
def foo(x=122):
    print(locals())
    def bar():
        x = 1
        y = 2
        print(locals())
        print(sum)
    print(locals())
    return bar

b = foo()
b()

x = 12
def foo(x=122):
    def bar():
        global x
        print(x)
    return bar

b = foo()
b()

x = 12
def foo(x=122):
    def bar():
        nonlocal x
        print(x)
    return bar

#замыкание

def make_adder(x):
    def adder(y):
        return x + y
    return adder

add_five = make_adder(5)
add_five(10)
add_five(-5)

def deprecated(func):
    def wrapper(*args, **kwargs):
        print '{} is deprecated !'.format(func.__name__)
