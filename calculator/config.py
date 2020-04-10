open_bracket = '('
closed_bracket = ')'
addition_sign = '+'
subtraction_sign = '-'
multiplication_sign = '*'
division_sign = '/'
exponent_sign = '^'

supported_operations = {addition_sign,
                        subtraction_sign,
                        multiplication_sign,
                        division_sign,
                        exponent_sign}

#  includes all supported characters excluding numbers
supported_operators = supported_operations.union(open_bracket, closed_bracket)