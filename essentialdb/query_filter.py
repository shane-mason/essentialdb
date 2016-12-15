__author__ = 'scmason'
from essentialdb import Keys


class LogicalOperator:
    def __init__(self, type, expressions):
        self.type = type
        self.expressions = expressions

    def test_document(self, document):
        match = True
        if self.type == Keys._and:
            for expression in self.expressions:
                match = expression.test_document(document)
                if match is False:
                    return False
        elif self.type == Keys._or:
            for expression in self.expressions:
                match = expression.test_document(document)
                if match is True:
                    return True
        elif self.type == Keys._nor:
            for expression in self.expressions:
                match = expression.test_document(document)
                if match is True:
                    return False
                else:
                    match = True
        elif self.type == Keys._not:
            raise NotImplementedError("We have not implemented NOT yet...")
        return match


class ComparisonOperator:
    def __init__(self, field, expression):
        self.field = None
        self.comparator_function = None
        self.match_value = None
        self.parse_expression(field, expression)

    def parse_expression(self, field, expression):
        self.field = field
        # expression is something like {'$eq': 'something'}
        # get the comparator function
        comparator = list(expression.keys())[0]
        self.comparator_function = Keys.comparisons[comparator]
        self.match_value = expression[comparator]

    def test_document(self, document):
        return self.comparator_function(document[self.field], self.match_value)


class EqualityOperator:
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def test_document(self, document):
        try:
            return self.value == document[self.field]
        except:
            return False


class QueryFilter:
    def __init__(self, query_document):
        self.expressions = self.__parse_query(query_document, [])

    def execute_filter(self, documents, filter_function=None):
        # first, look for the most simple case, which is an id lookup
        if len(self.expressions) == 1 and isinstance(self.expressions[0],EqualityOperator) and self.expressions[0].field == Keys.id:
            id = self.expressions[0].value
            if id in documents:
                return [documents[id]]
            else:
                return []

        results = []
        for key in documents:
            matches = True
            for expression in self.expressions:
                matches = expression.test_document(documents[key])
                if matches is False:
                    break
            if filter_function:
                matches = filter_function(documents[key])

            if matches is True:
                results.append(documents[key])

        return results

    def __parse_query(self, query_document, expression_list):
        expressions = expression_list
        for key in query_document:

            # { $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
            # { $or: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
            # { $nor: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
            # { $not: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
            if key in [Keys._and, Keys._or, Keys._nor, Keys._not]:
                log_expressions = []
                for item in query_document[key]:
                    log_expressions = self.__parse_query(item, log_expressions)
                logical_operator = LogicalOperator(key, log_expressions)
                expressions.append(logical_operator)
            # first basic expression - something like {"field': {'$eq': 'something'}}
            elif isinstance(query_document[key], dict):
                expressions.append(ComparisonOperator(key, query_document[key]))
            # then we are left with {"field 1", "value 1"}
            else:

                expressions.append(EqualityOperator(key, query_document[key]))

        return expressions
