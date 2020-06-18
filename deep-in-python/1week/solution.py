# import sys
#
#
# def sum_in_str(string):
#     result = 0
#     for digit in string:
#         result += int(digit)
#
#     return result
#
#
# digit_string = sys.argv[1]
# print(sum_in_str(digit_string))
#
# import sys
#
#
# def stairs(height):
#     for i in range(height):
#         print(' ' * (height - i - 1) + '#' * (i + 1))
#
#
# stairs(int(sys.argv[1]))


import sys


def disk(a_, b_, c_):
    return b_ * b_ - 4*a_*c_


a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])

print(int((-b + disk(a, b, c) ** 0.5) / (2*a)))
print(int((-b - disk(a, b, c) ** 0.5) / (2*a)))


