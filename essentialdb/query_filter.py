__author__ = 'scmason'
from essentialdb import Keys


class LogicalOperator:
    """
    Logical)perator rmodels a list of expressions that are bnound by logical operator - inclusing::

        { $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
        { $or: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
        { $nor: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
        { $not: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }

    The expressiona are stores as an ordered array, each are executed on calls to 'test_document'.
    """

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
            for expression in self.expressions:
                match = expression.test_document(document)
                if match is False:
                    break
            match = not match

        return match


class ComparisonOperator:
    """
    ComparisonOperator represents expressions with comparison operators of the form::

        { field: { operator: value } }

    For example:

        { 'first_name' : { '$eq' : 'john' } }
        { 'year' : { '$gt' : 1900 } }

    And so on.
    """

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
        try:
            return self.comparator_function(document[self.field], self.match_value)
        except:
            return False


class EqualityOperator:
    """
    EqualityOperator checks for basic eqaulity, in expressions of the form::

            {field : value}

    For example:

            {'first_name' : 'John'}
            {'subscriber' : True}

    And so on.
    """

    def __init__(self, field, value):
        self.field = field
        self.value = value

    def test_document(self, document):
        try:
            return self.value == document[self.field]
        except:
            return False


class QueryFilter:
    """
    Models a 'compiled' query document. The raw query doscument is sent in and 'parsed' or compiled into a list of
    expressions. Later, the filter can be executed across a set of documents.
    """

    def __init__(self, query_document):
        self.expressions = self.__parse_query(query_document, [])

    def execute_filter(self, documents, filter_function=None):
        """
        Execute the filter across a ser of provided documents.
        """
        # first, look for the most simple case, which is an id lookup
        if len(self.expressions) == 1 and isinstance(self.expressions[0], EqualityOperator) and self.expressions[
            0].field == Keys.id:
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
