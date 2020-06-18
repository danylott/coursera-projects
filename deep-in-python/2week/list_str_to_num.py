objects = ['1', '2', '3', '4']

objects = list(map(lambda x: int(x), objects))


from functools import reduce

print(reduce(lambda a, b: a*b, objects))