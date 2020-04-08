class Add:
    def __init__(self, __op1):
        self.__op1 = __op1

    def apply(self, __op2):
        return self.__op1 + __op2


class Subtract:
    def __init__(self, __op1):
        self.__op1 = __op1

    def apply(self, __op2):
        return self.__op1 - __op2


class Multiply:
    def __init__(self, __op1):
        self.__op1 = __op1

    def apply(self, __op2):
        return self.__op1 * __op2


class Divide:
    def __init__(self, __op1):
        self.__op1 = __op1

    def apply(self, __op2):
        return self.__op1 / __op2


class Power:
    def __init__(self, __op1):
        self.__op1 = __op1

    def apply(self, __op2):
        return pow(self.__op1,  __op2)


class NoOp:
    def apply(self, __op):
        return __op

