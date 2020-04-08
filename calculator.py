import sys


def calculate(o):

    numbers = parse_numbers(o)
    operations = parse_operators(o)

    print('-------')
    print('looking for:')
    print('-------')
    print(numbers)
    print(operations)
    print('-------')

    return calculate_helper(numbers, operations)


recursive_call_count = 0


def calculate_helper(numbers, operations):
    global recursive_call_count
    recursive_call_count += 1

    if len(numbers) == 1 and len(operations) != 0:
        raise RuntimeError

    if len(numbers) == 1:
        return int(numbers[0])

    result = 0

    if operations[0] == '(':
        i = find_index_of_closing_bracket(operations)
        j = find_operations(operations, i)

        n = calculate_helper(numbers[:j + 1], operations[1:i])
        result = calculate_helper([n] + numbers[j + 1:len(numbers)], operations[i + 1:len(operations)])

    elif operations[0] == '*':
        if len(operations) > 1 and operations[1] == '(':  # if bracket is coming up it takes higher precedence
            i = find_index_of_closing_bracket(operations[1:]) + 1
            j = find_operations(operations[1:], i) + 1

            n = int(numbers[0]) * calculate_helper(numbers[1:j + 1], operations[2:i])
            result = calculate_helper([n] + numbers[j + 1:len(numbers)], operations[i + 1:len(operations)])
        else:
            n = [int(numbers[0]) * int(numbers[1])] + numbers[2:]
            result = calculate_helper(n, operations[1:])

    elif operations[0] == '/':
        if len(operations) > 1 and operations[1] == '(':  # if bracket is coming up it takes higher precedence
            i = find_index_of_closing_bracket(operations[1:]) + 1
            j = find_operations(operations[1:], i) + 1

            n = int(numbers[0]) / calculate_helper(numbers[1:j + 1], operations[2:i])
            result = calculate_helper([n] + numbers[j + 1:len(numbers)], operations[i + 1:len(operations)])
        else:
            n = [int(numbers[0]) / int(numbers[1])] + numbers[2:]
            result = calculate_helper(n, operations[1:])

    elif operations[0] == '+':
        result = int(numbers[0]) + calculate_helper(numbers[1:], operations[1:])

    elif operations[0] == '-':
        result = int(numbers[0]) - calculate_helper(numbers[1:], operations[1:])

    else:
        raise RuntimeError

    print(numbers)
    print(operations)
    print(result)
    print('-----')

    return result


def find_index_of_closing_bracket(operations):
    stack = []
    index = 0
    to_return = index
    for i in operations:
        if len(stack) == 0 and to_return != 0:
            return to_return
        if i == '(':
            stack.append('x')
        if i == ')':
            stack.pop()
            to_return = index
        index = index + 1

    return to_return


def parse_numbers(o):
    result = []
    while len(o) != 0:
        n = ''

        if o[0] == ' ':
            o = o[1:]
            continue

        while len(o) != 0 and o[0].isdigit():
            n = n + o[0]
            o = o[1:]
        if len(o) != 0:
            o = o[1:]

        if n.isdigit():
            result.append(n)

    return result


def find_operations(o, w):
    j = 0
    for i in range(0, w):
        x = o[i]
        if x == '+' or x == '*' or x == '/' or x == '-':
            j = j + 1
    return j


def parse_operators(o):
    r = []
    for i in o:
        if i == ' ':
            continue
        if i == '+' or i == '*' or i == '/' or i == '-' or i == '(' or i == ')':
            r.append(i)

    return r


def validate_brackets(o):
    stack = []
    index = 0
    index_of_opened = index
    for i in o:
        if i == '(':
            stack.append('x')
            index_of_opened = index
        if i == ')':
            stack.pop()
        index += 1

    if len(stack) > 0:
        m = 'Unbalanced bracket''\n' \
            + o[:index_of_opened] + '' + o[index_of_opened] + '' + o[index_of_opened+1:len(o)] \
            + '\n' + (' ' * index_of_opened + '^')
        raise RuntimeError(m)


t = '(4 + 4) * 344 + (((6 + 7) * 1333) + 2 + 100000) * (30 + 2) + (4 + 4) * 344 * (((6 + 7) * 1333) + 2 + 100000) * (' \
    '30 + 2) + (4 + 4) * 344 + (((6 + 7) * 1333)) '

print("-------")
print("equation: " + t)

validate_brackets(t)

# need to validate that brackets are balanced
print("result: " + str(calculate(t)))

print("-------")
print("recursion stack size: " + str(sys.getrecursionlimit()))
print("recursive calls made: " + str(recursive_call_count))
print("time complexity: O(n)")
print("space complexity: O(n)?")
