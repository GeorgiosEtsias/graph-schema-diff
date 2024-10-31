"""

Script determines all the breaking and non-breaking changes
between 2 versions of a GraphQL schema.

"""

# import packages
import logging
from graphql import GraphQLSchema, build_schema

# import custom modules
from schema_changes import compare_schemas
from schema_changes_llm import  analyze_schema_changes
from release_summary import generate_release_summary

def parse_schema(schema_str: str ) -> GraphQLSchema | dict:
    """
    Parse the GraphQL schema string and return a schema object.

    Args:
        schema_str (str): The GraphQL schema as a string.

    Returns:
        GraphQLSchema: Parsed GraphQL schema object.
    """
    try:
        return build_schema(schema_str)

    except Exception as e:
        # unable to create a schema
        error_message = f"Error parsing schema: {schema_str}. Exception: {e}"
        logging.error(error_message)
        return {
            "status": "Failed",
            "reason": [error_message]
            }

def check_graphql_parsing_failure(schema_version1, schema_version2):
    """
    Checks the types of two GraphQL schema versions and logs errors if either or both
    schemas are not of type GraphQLSchema.

    Args:
        schema_version1 (any): The first GraphQL schema version to check.
        schema_version2 (any): The second GraphQL schema version to check.

    Returns:
        list or dict: A structured output indicating parsing failure, including error messages
        and the schema versions that could not be parsed. The output can be:
            - A list containing a single dictionary if neither schema is valid.
            - A dictionary if only one of the schemas is invalid.
    """
    if type(schema_version1) != GraphQLSchema and type(schema_version2) != GraphQLSchema:
        error_message = 'Neither of the 2 GraphQL schema versions could be parsed'
        logging.error(error_message)
        output = [{'parsing_failed': [error_message, schema_version1, schema_version2]}]
        return output
    elif type(schema_version1) != GraphQLSchema:
        error_message = 'Version 1 of the GraphQL schema could not be parsed'
        logging.error(error_message)
        output = {'parsing_failed': [error_message, schema_version1]}
        return output
    elif type(schema_version2) != GraphQLSchema:
        error_message = 'Version 2 of the GraphQL schema could not be parsed'
        logging.error(error_message)
        output = {'parsing_failed': [error_message, schema_version2]}
        return output

    # If both schemas are valid, return None or any other appropriate value
    return None


def graphql_diff_report(schema_v1_str: str,
                        schema_v2_str: str,
                        identify_changes_technique: str,
                        summarization_technique: str) -> dict | str:
    """

    Method checks two versions GraphQL schema strings, and returns a
    detailed report of all breaking and non-breaking changes,
    alongside a summary.

    Args:
        schema_v1_str (str): the string of the first version of the GraphQL schema
        schema_v2_str (str): the string of the second version of the GraphQL schema
        identify_changes_technique (str): The technique for identifying the schema changes
            could be: 'algorithmic' or 'GPT3.5' based
        summarization_technique (str): The technique for generating the summary could
            be: 'algorithmic' or 'GPT3.5' based

    Returns:
        dict: A dictionary with the changes and the summary report.


    """
    # instantiate changes
    changes = []

    # remove string whitespace
    schema_v1_str = ' '.join(schema_v1_str.strip().split())
    schema_v2_str = ' '.join(schema_v2_str.strip().split())

    # if the schema strings are identical terminate the procedure.
    if schema_v1_str == schema_v2_str:
        changes = []
        # summarize the differences
        changes_with_summary = generate_release_summary(changes, summarization_technique)
        return changes_with_summary

    # Check if the schemas have the expected GraphQL structure
    schema_v1_str_mod = schema_v1_str.replace('\r\n', '\n').strip()
    schema_v2_str_mod = schema_v2_str.replace('\r\n', '\n').strip()

    # parse the GraphQL schemas
    schema_version1 = parse_schema(schema_v1_str_mod)
    schema_version2 = parse_schema(schema_v2_str_mod)

    # terminate the procedure if schemas were not parsed
    parsing_failure = check_graphql_parsing_failure(schema_version1, schema_version2)
    if parsing_failure is not None:
        return parsing_failure

    # if the parsed schemas are identical terminate the procedure.
    if schema_version1 == schema_version2:
        changes = []
        # summarize the differences
        changes_with_summary = generate_release_summary(changes, summarization_technique)
        return changes_with_summary


    # identify the differences between the 2 schemas
    if identify_changes_technique == 'GPT3.5': # LLM based solution
        changes = analyze_schema_changes(schema_v1_str, schema_v2_str)

    elif identify_changes_technique == 'algorithmic':  # Pythonic solution
        changes = compare_schemas(schema_version1, schema_version2)

    # summarize the differences
    changes_with_summary = generate_release_summary(changes, summarization_technique)

    return changes_with_summary
