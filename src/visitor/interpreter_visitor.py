from collections import deque
from currency.currency import Currency

from visitor.interface import Visitor
from context.context import Context
from parse_objects.objects import (
    VariableAccess,
    BuiltInFunction
)
from interpreter.reference import Reference
from error_manager.interpreter_er import (
    NoMainFunction,
    NotExactArguments,
    UndefinedVariable,
    FunctionNotFound,
    DivisionByZero
)
from parse_objects.objects import BuiltInFunction
from interpreter.calculations import Calculations

class InterpreterVisitor(Visitor):
    def __init__(self, error_manager):
        self._error_manager = error_manager
        self._calculations_handler = Calculations(error_manager)
        self._last_result = None
        self._global_context = Context()
        self._call_context = Context(global_context=self._global_context)
        self._last_contexts = deque()
        self._call_position = None
        self._returning = False
        self._breaking = False
        self._continuing = False
        self._resolving = True

    def _consume_last_result(self):
        value = self._last_result
        self._last_result = None
        return value

    def _insert_builtin_functions(self):
        for function in BUILTINS_LIST:
            function_obj = BuiltInFunction(position=None, name=function[0], function=function[1])
            self._global_context.insert_symbol(function[0], function_obj)

    def _get_left_right_expressions(self, expression):
        expression.left.accept(self)
        left = self._consume_last_result()
        expression.right.accept(self)
        right = self._consume_last_result()
        return left, right
    
    def _call_function(self, function, arguments):
        self._last_contexts.append(self._call_context)
        self._call_context = Context(global_context=self._global_context)
        function.accept(self)
        self._call_context = self._last_contexts.pop()

    def visit_program(self, program):
        for function in program.functions.values():
            self._global_context.insert_symbol(function.name, function)
        self._insert_builtin_functions()
        main_function = self._global_context.get_value('main')
        if not main_function:
            error = NoMainFunction(position=None, name=None)
            self._error_manager.fatal_error(error) 
        self._call_function(main_function, []) ## Done

    def visit_function_definition(self, function_definition):
        arguments = self._consume_last_result() or []
        if len(arguments) != len(function_definition.parameters):
            error = NotExactArguments(position=(function_definition.position, self._call_position)
            , name=function_definition.name) ## DONE
            self._error_manager.fatal_error(error)
        for argument, parameter in zip(arguments, function_definition.parameters):
            self._call_context.insert_symbol(parameter.name, argument)
        function_definition.block.accept(self)
        self._returning = False

    def visit_block(self, block):
        self._call_context.enter_scope()
        for statement in block.statements:
            statement.accept(self)
            if self._returning:
                break
            self._last_result = None
            if self._breaking or self._continuing:
                break
        self._call_context.leave_scope()

    def visit_identifier_expression(self, identifier_expression):
        if self._resolving:
            value_obj = self._call_context.get_value(identifier_expression.name)
            if value_obj is None:
                error = UndefinedVariable(position=identifier_expression.position, name=identifier_expression.name)
                self._error_manager.fatal_error(error)
            self._last_result = value_obj
        else:
            self._last_result = identifier_expression.name

    def visit_if_stmt(self, statement):
        statement.condition.accept(self)
        if self._consume_last_result().value:
            statement.true_block.accept(self)
        elif statement.else_block:
            statement.else_block.accept(self)

    def visit_while_stmt(self, statement):
        statement.condition.accept(self)
        execute = self._consume_last_result()
        while execute.value:
            statement.true_block.accept(self)
            if self._breaking or self._returning:
                self._breaking = False
                break
            if self._continuing:
                self._continuing = False
            statement.condition.accept(self)
            execute = self._consume_last_result()

    def visit_return_stmt(self, statement):
        if statement.expression:
            statement.expression.accept(self)
        self._returning = True

    def visit_break_stmt(self, statement):
        self._breaking = True

    def visit_continue_stmt(self, statement):
        self._continuing = True

    def visit_expression(self, expression):
        ...

    def visit_comparison(self, comparison):
        left, right = self._get_left_right_expressions(comparison)
        self._last_result = self._calculations_handler.compare_values(left.value, right.value, comparison)

    def visit_add_expression(self, expression):
        left, right = self._get_left_right_expressions(expression)
        self._last_result = self._calculations_handler.calculate_result(
            left.value, right.value, expression, lambda a, b: a + b
        )

    def visit_sub_expression(self, expression):
        left, right = self._get_left_right_expressions(expression)
        self._last_result = self._calculations_handler.calculate_result(
            left.value, right.value, expression, lambda a, b: a - b
        )

    def visit_mul_expression(self, expression):
        left, right = self._get_left_right_expressions(expression)
        self._last_result = self._calculations_handler.calculate_result(
            left.value, right.value, expression, lambda a, b: a * b
        )

    def visit_div_expression(self, expression):
        left, right = self._get_left_right_expressions(expression)
        if right.value == 0:
            error = DivisionByZero(position=expression.position, name=None)
            self._error_manager.fatal_error(error)
        self._last_result = self._calculations_handler.calculate_result(
            left.value, right.value, expression, lambda a, b: a / b
        )

    def visit_pow_expression(self, expression):
        left, right = self._get_left_right_expressions(expression)
        self._last_result = self._calculations_handler.calculate_result(
            left.value, right.value, expression, lambda a, b: pow(a, b)
        )

    def visit_tran_expression(self, expression):
        left, right = self._get_left_right_expressions(expression)
        self._last_result = self._calculations_handler.calculate_result(
            left.value, right.value, expression, "tran"
        )

    def visit_negated_expression(self, negated):
        negated.right.accept(self)
        right = self._consume_last_result()
        self._last_result = self._calculations_handler.negate_value(right.value, negated)

    def visit_or_expression(self, expression):
        expression.left.accept(self)
        left = self._consume_last_result()
        if left.value is True:
            self._last_result = Reference(value=True)
            return
        expression.right.accept(self)
        right = self._consume_last_result()
        self._last_result = self._calculations_handler.handle_relations(
            left.value, right.value, expression, lambda a, b: a or b
        )

    def visit_and_expression(self, expression):
        expression.left.accept(self)
        left = self._consume_last_result()
        if left.value is False:
            self._last_result = Reference(value=True)
            return
        expression.right.accept(self)
        right = self._consume_last_result()
        self._last_result = self._calculations_handler.handle_relations(
            left.value, right.value, expression, lambda a, b: a and b
        )

    def visit_constant(self, constant):
        if isinstance(constant, Currency):
            self._last_result = Reference(value=constant)
        else:
            self._last_result = Reference(value=constant.value)

    def visit_variable_access(self, variable_access):
        variable_access.variable[0].accept(self)
        if len(variable_access.variable) == 1:
            return
        method_or_value = self._consume_last_result().value
        if isinstance(method_or_value, str):
            self._resolving = True
            variable_access.variable[0].accept(self)
            method_or_value = self._consume_last_result().value
        for part in variable_access.variable[1:]:
            method_name = part.variable[0].name if isinstance(part, VariableAccess) else part.name
            method_or_value = getattr(method_or_value, method_name)
            self._last_result = method_or_value

    def visit_assignment(self, assignment):
        self._resolving = False
        assignment.left.accept(self)
        variable_name = self._consume_last_result()
        self._resolving = True
        assignment.right.accept(self)
        value = self._consume_last_result()
        value = value.value if isinstance(value, Reference) else value
        old_value = self._call_context.get_value(variable_name)
        if old_value is None:
            self._call_context.insert_symbol(
                variable_name, value if isinstance(value, Reference) else Reference(value=value) # DONE
            )
        else:
            old_value.value = value

    def visit_function_call(self, fun_call):
        arguments = []
        self._call_position = fun_call.position
        for argument in fun_call.arguments:
            argument.accept(self)
            value = self._consume_last_result()
            arguments.append(value if isinstance(value, Reference) else Reference(value=value))
        self._last_result = arguments
        function = self._global_context.get_value(fun_call.name)
        if function is None:
            error = FunctionNotFound(position=fun_call.position, name=fun_call.name)
            self._error_manager.fatal_error(error)
        self._call_function(function, arguments)

    def visit_external_function(self, ext_function):
        arguments = self._consume_last_result() or []
        self._last_result = ext_function.function(*[argument.value for argument in arguments] if len(arguments) else " ") # DONE

def bytes_print(text):
    print(text.decode() if isinstance(text, bytes) else text)

BUILTINS_LIST = [
    ('print', bytes_print),
    ('input', input)
]