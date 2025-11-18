from graphql import ExecutionResult

def execute_graphql_query(schema, query: str, variables: dict = None) -> ExecutionResult:
    if not isinstance(query, str):
        raise TypeError("Error: query must be graphene.String type")
    if variables is not None and not isinstance(variables, dict):
        raise TypeError("Error: variables must be dict type")

    result = schema.execute(query, variable_values=variables)
    return result


