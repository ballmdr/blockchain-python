name = 'ballmdr'
age = '33'

def print_name():
    print(name + age)

def print_arg(arg1, arg2):
    print(arg1 + arg2)

def decade():
    print(int(age) % 10)

print_name()
print_arg('hello', 'world')
decade()
