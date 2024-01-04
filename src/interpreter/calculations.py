from error_manager.interpreter_er import WrongTypeForOperation
from parse_objects.objects import (
    Operator,
    AddExpression,
)
from interpreter.reference import Reference
from currency.config import exchange_rates
from currency.currency import Currency

NUMBER_TYPES = [int, float]
STR_TYPES = [str, bytes]
CURRENCY = ["EUR", "PLN", "USD"]
NUMBER_OPERATOR_MAPPING = {
    Operator.EQ: lambda a, b: a == b,
    Operator.NE: lambda a, b: a != b,
    Operator.GT: lambda a, b: a > b,
    Operator.LT: lambda a, b: a < b,
    Operator.GE: lambda a, b: a >= b,
    Operator.LE: lambda a, b: a <= b,
}
BOOL_OPERATOR_MAPPING = {
    Operator.EQ: lambda a, b: a is b,
    Operator.NE: lambda a, b: a is not b
}

STRING_OPERATOR_MAPPING = {
    Operator.EQ: lambda a, b: a == b,
    Operator.NE: lambda a, b: a != b,
}


class Calculations:
    def __init__(self, error_manager):
        self._error_manager = error_manager

    def compare_values(self, left, right, comparison):
        self._left = left
        self._right = right
        self._operator = comparison.operator
        result = self._try_compare_currency()
        if result is None:
            result = self._try_compare_numbers()
        if result is None:
            result = self._try_compare_bools()
        if result is None:
            result = self._try_compare_strings()
        if result is None:
            error = WrongTypeForOperation(position=comparison.position, name=(type(self._left), type(self._right)))
            self._error_manager.fatal_error(error)
        return Reference(value=result)

    def calculate_result(self, left, right, expression, method):
        self._left = left
        self._right = right
        self._position = expression.position
        self._concatenating = isinstance(expression, AddExpression)
        self._method = method
        result = self._try_calculate_currency()
        if result is None:
            result = self._try_calculate_numbers()
        if result is None:
            result = self._try_concatenate_strings()
        if result is None:
            error = WrongTypeForOperation(position=expression.position, name=(type(self._left), type(self._right)))
            self._error_manager.fatal_error(error)
        return Reference(value=result)

    def negate_value(self, right, expression):
        self._right = right
        result = self._try_negate_number()
        if result is None:
            result = self._try_negate_bool()
        if result is None:
            error = WrongTypeForOperation(position=expression.position, name=(type(self._left), type(self._right)))
            self._error_manager.fatal_error(error)
        return Reference(value=result)

    def handle_relations(self, left, right, expression, method):
        if type(left) is not bool or type(right) is not bool:
            error = WrongTypeForOperation(position=expression.position, name=(type(left), type(right)))
            self._error_manager.fatal_error(error)
        return Reference(value=method(left, right))


    def _try_compare_currency(self):
        if not isinstance(self._left, Currency) or not isinstance(self._right, Currency):
            return
        exchange = exchange_rates[self._left.symbol][self._right.symbol]
        value = self._left.value * exchange
        method = NUMBER_OPERATOR_MAPPING.get(self._operator)
        if not method:
            return
        return method(value, self._right.value)

    def _try_compare_numbers(self):
        if type(self._left) not in NUMBER_TYPES or type(self._right) not in NUMBER_TYPES:
            return
        method = NUMBER_OPERATOR_MAPPING.get(self._operator)
        if not method:
            return
        return method(self._left, self._right)

    def _try_compare_bools(self):
        if type(self._left) is not bool or type(self._right) is not bool:
            return
        method = BOOL_OPERATOR_MAPPING.get(self._operator)
        if not method:
            return
        return method(self._left, self._right)
    
    def _try_compare_strings(self):
        if type(self._left) not in STR_TYPES or type(self._right) not in STR_TYPES:
            return
        method = STRING_OPERATOR_MAPPING.get(self._operator)
        if not method:
            return
        return method(self._left, self._right)

    def _try_calculate_numbers(self):
        if type(self._left) not in NUMBER_TYPES or type(self._right) not in NUMBER_TYPES:
            return
        return self._method(self._left, self._right)
    
    def _try_calculate_currency(self):
        if not isinstance(self._left, Currency) or (not isinstance(self._right, Currency) and self._right not in CURRENCY):
            return
        if self._method == "tran":
            if self._right in CURRENCY:
                exchange = exchange_rates[self._left.symbol][self._right]
                self._left.value = self._left.value * exchange
                self._left.symbol = self._right.symbol
                return self._left
            exchange = exchange_rates[self._left.symbol][self._right.symbol]
            self._left.value = self._left.value * exchange
            self._left.symbol = self._right.symbol
            return self._left
        exchange = exchange_rates[self._right.symbol][self._left.symbol]
        self._left.value = self._method(self._left.value, self._right.value * exchange)
        return self._left

    def _try_concatenate_strings(self):
        if type(self._left) not in STR_TYPES or type(self._right) not in STR_TYPES or not self._concatenating:
            return
        return self._method(self._left, self._right)

    def _try_negate_number(self):
        if type(self._right) not in NUMBER_TYPES:
            return
        return self._right * -1

    def _try_negate_bool(self):
        if type(self._right) is not bool:
            return
        return not self._right
