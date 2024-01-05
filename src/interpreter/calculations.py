from error_manager.interpreter_er import WrongTypeForOperation, ValueSizeExceed
from parse_objects.objects import (
    Operator,
    AddExpression,
)
from interpreter.reference import Reference
from currency.config import exchange_rates
from currency.currency import Currency
import sys

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
            result = self._try_negate_currency()
        if result is None:
            error = WrongTypeForOperation(position=expression.position, name=(type(self._left), type(self._right)))
            self._error_manager.fatal_error(error)
        return Reference(value=result)

    def handle_relations(self, left, right, expression, method):
        if type(left) is not bool or type(right) is not bool:
            error = WrongTypeForOperation(position=expression.position, name=(type(left), type(right)))
            self._error_manager.fatal_error(error)
        return Reference(value=method(left, right))


    def _check_number_size(self, value):
        if value > sys.maxsize or value < (-1) * sys.maxsize:
            error = ValueSizeExceed(position=self._position)
            self._error_manager.fatal_error(error)

    def _try_compare_currency(self):
        if not isinstance(self._left, Currency) and not isinstance(self._right, Currency):
            return
        exchange = exchange_rates[self._left.type][self._right.type]
        value = self._left.value * exchange
        method = NUMBER_OPERATOR_MAPPING.get(self._operator)
        if not method:
            return
        return method(value, self._right.value)

    def _try_compare_numbers(self):
        if type(self._left) not in NUMBER_TYPES and type(self._right) not in NUMBER_TYPES:
            return
        method = NUMBER_OPERATOR_MAPPING.get(self._operator)
        if not method:
            return
        return method(self._left, self._right)

    def _try_compare_bools(self):
        if type(self._left) is not bool and type(self._right) is not bool:
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
        value = self._method(self._left, self._right)
        self._check_number_size(value)
        return value
    
    def _transfer(self):
        if self._right in CURRENCY and isinstance(self._left, Currency):
            exchange = exchange_rates[self._left.type][self._right]
            value = self._left.value * exchange
            self._check_number_size(value)
            return Currency(value, self._right)
        elif isinstance(self._left, Currency) and isinstance(self._right, Currency):
            exchange = exchange_rates[self._left.type][self._right.type]
            value = self._left.value * exchange + self._right.value
            self._check_number_size(value)
            return Currency(value, self._right.type)
        
    def _operate_on_Currency(self):
        if(self._right.type != self._left.type):
            exchange = exchange_rates[self._right.type][self._left.type]
            value = self._method(self._left.value, self._right.value * exchange)
            self._check_number_size(value)
            return Currency(value, self._left.type)
        value = self._method(self._left.value, self._right.value)
        self._check_number_size(value)
        return Currency(value, self._left.type)
        
    def _try_calculate_currency(self):
        if not isinstance(self._left, Currency) and not isinstance(self._right, Currency):
            return
        if self._method == "tran":
            return self._transfer()
        if type(self._left) in NUMBER_TYPES and isinstance(self._right, Currency):
            value = self._method(self._left, self._right.value)
            self._check_number_size(value)
            return Currency(value, self._right.type)
        elif type(self._right) in NUMBER_TYPES and isinstance(self._left, Currency):
            value = self._method(self._left.value, self._right)
            self._check_number_size(value)
            return Currency(value, self._left.type)
        elif isinstance(self._right, Currency) and isinstance(self._left, Currency):
            return self._operate_on_Currency()
        return

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

    def _try_negate_currency(self):
        if not isinstance(self._right, Currency):
            return
        return Currency(-self._right.value, self._right.type)