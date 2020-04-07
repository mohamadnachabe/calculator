def calculate(o):
    if len(o) == 1:
        return o

    if o[1] == '+':
        return int(calculate(o[0])) + int(calculate(o[2:]))

def clean_white_space(o):
    if len(o) == 1:
        return o

    if o[0] != ' ':
        return o[0] + clean_white_space(o[1:])
    else:
        return clean_white_space(o[1:])

t = clean_white_space('344*4 + 4')
print(calculate(t))