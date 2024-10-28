"""

Script to identify all the differences between two versions of a GraphQL schema.

"""
# import packages
from graphql import GraphQLSchema, GraphQLObjectType, GraphQLInterfaceType, GraphQLScalarType, \
    GraphQLEnumType, GraphQLInputObjectType, GraphQLUnionType
import logging
from typing import List, Dict


# ----  check types ---- #

def compare_types(schema_version1: GraphQLSchema, schema_version2: GraphQLSchema) -> list[dict]:
    """
    Compare types between two schemas and detect type-level changes.

    Args:
        schema_version1 (GraphQLSchema): The first version of the GraphQL schema.
        schema_version2 (GraphQLSchema): The second version of the GraphQL schema.

    Returns:
        List[Dict]: List of changes detected at the type level.
    """

    changes = []
    for type_name, type_v1 in schema_version1.type_map.items():
        if type_name.startswith("__"):  # Skip internal types (e.g., introspection types)
            continue

        # disregard the scalar types in this part of the script
        if type_name in ['Int', 'Float', 'String', 'Boolean', 'ID']:
            continue

        # check if type exists in the new schema
        type_v2 = schema_version2.get_type(type_name)

        # if it does not exist
        if not type_v2:
            # Type removed
            changes.append(type_removed_change(type_name))
        else:
            # if it exists
            # check the type's GraphQL-type
            type_v1_type = identify_graphql_type(type_v1)
            type_v2_type = identify_graphql_type(type_v2)

            # if the old new version of the type, have a different GraphQL type
            if type_v1_type != type_v2_type:
                changes.append(type_type_changed_change(type_name, type_v1_type, type_v2_type))

            else:
                # if the 2 types have identical GraphQL type check their fields
                changes.extend(compare_type_fields(type_name, type_v1, type_v2))

    # Check for new types in schema_version2
    for type_name in schema_version2.type_map:
        if type_name.startswith("__"):  # Skip internal types (e.g., introspection types)
            continue

        # disregard the scalar types in this part of the script
        if type_name in ['Int', 'Float', 'String', 'Boolean', 'ID']:
            continue

        if type_name not in schema_version1.type_map:
            # New type added
            changes.append(type_added_change(type_name))

    return changes


def identify_graphql_type(graphql_type):
    """
    :param graphql_type:
    :return:
    """
    if isinstance(graphql_type, GraphQLObjectType):
        return "GraphQLObjectType"
    elif isinstance(graphql_type, GraphQLInterfaceType):
        return "GraphQLInterfaceType"
    elif isinstance(graphql_type, GraphQLScalarType):
        return "GraphQLScalarType"
    elif isinstance(graphql_type, GraphQLEnumType):
        return "GraphQLEnumType"
    elif isinstance(graphql_type, GraphQLInputObjectType):
        return "GraphQLInputObjectType"
    elif isinstance(graphql_type, GraphQLUnionType):
        return "GraphQLUnionType"
    else:
        return "Unknown type"


def type_type_changed_change(type_name: str, type_v1, type_v2) -> dict:
    """
    Create a change record for a changed type (e.g., scalar to enum).

    Args:
        type_name (str): Name of the changed type.
        type_v1: The first version of the type.
        type_v2: The second version of the type.

    Returns:
        Dict: A change record indicating a type change.
    """
    return {
        "type": type_name,
        "change": f"Type changed from '{type_v1}' to '{type_v2}'",
        "breaking": True,
        "release_note": f"The type '{type_name}' has changed from '{type_v1}' to '{type_v2}'. This is a breaking change."
    }


def type_removed_change(type_name: str) -> dict:
    """
    Create a change record for a removed type.

    Args:
        type_name (str): Name of the removed type.

    Returns:
        Dict: A change record indicating a type removal.
    """
    return {
        "type": type_name,
        "change": f"Type '{type_name}' was removed",
        "breaking": True,
        "release_note": f"The type '{type_name}' has been removed. This is a breaking change and will affect any queries relying on this type."
    }


def type_added_change(type_name: str) -> dict:
    """
    Create a change record for a new type.

    Args:
        type_name (str): Name of the new type.

    Returns:
        Dict: A change record indicating a new type addition.
    """
    return {
        "type": type_name,
        "change": f"Added new type '{type_name}'",
        "breaking": False,
        "release_note": f"A new type '{type_name}' has been added. This is a non-breaking change."
    }


# ----  check type fields & enum type values ---- #

def compare_type_fields(type_name: str, type_v1, type_v2) -> list[dict]:
    """
    Compare fields between two versions of a type.

    Args:
        type_name (str): The name of the type being compared.
        type_v1 (GraphQLObjectType): The first version of the GraphQL type.
        type_v2 (GraphQLObjectType): The second version of the GraphQL type.

    Returns:
        List[Dict]: List of changes detected at the field level.
    """
    changes = []

    if isinstance(type_v1, (GraphQLObjectType, GraphQLInterfaceType)) and isinstance(type_v2, (
    GraphQLObjectType, GraphQLInterfaceType)):
        changes.extend(compare_existing_fields(type_name, type_v1, type_v2))
        changes.extend(compare_new_fields(type_name, type_v1, type_v2))

    elif isinstance(type_v1, GraphQLEnumType):
        changes.extend(compare_enum_type_values(type_name, type_v1, type_v2))


    return changes

def compare_enum_type_values(type_name:str,
                             type_v1: GraphQLEnumType,
                             type_v2: GraphQLEnumType
                             )-> List[Dict]:
    """

    :return:
    """
    changes = []
    type_v1_values = list(type_v1.values)
    type_v2_values = list(type_v2.values)

    # check for removed enum values
    for v1_value in list(type_v1.values):
        if v1_value not in type_v2_values:
            changes.append(enum_value_removed_change(type_name, v1_value))

    # check for added enum values
    for v2_value in list(type_v2_values):
        if v2_value not in type_v1_values:
            changes.append(enum_value_added_change(type_name, v2_value))

    return changes


def enum_value_removed_change(type_name: str, value_name: str) -> dict:
    """
    Create a change record for a removed enum value.

    Args:
        type_name (str): Name of the type.
        value_name (str): Name of the removed value.

    Returns:
        Dict: A change record indicating a field removal.
    """
    return {
        "type": type_name,
        "change": f"Value '{value_name}' was removed", #GE
        "breaking": True,
        "release_note": f"Value '{value_name}' on enum type '{type_name}' has been removed. Update any queries or mutations using this field."
    }


def enum_value_added_change(type_name: str, value_name: str) -> dict:
    """
    Create a change record for a new value.

    Args:
        type_name (str): Name of the type.
        value_name (str): Name of the new value.

    Returns:
        Dict: A change record indicating a new field addition.
    """
    return {
        "type": type_name,
        "change": f"Added new value '{value_name}'",
        "breaking": False,
        "release_note": f"A new value '{value_name}' has been added to enum type '{type_name}'. This is a non-breaking change."
    }


def get_field_type_name(field_v1) -> str:
    """
    Extract the name of the field type from a GraphQL field type.

    Args:
        field_v1: A GraphQL field object that may have a name attribute or an of_type attribute.

    Returns:
        str: The name of the field type, or an empty string if no name is found.
    """
    # Declare the main variable type
    field_name: str = ""

    if hasattr(field_v1.type, 'name'):
        field_name = field_v1.type.name
    elif hasattr(field_v1.type.of_type, 'name'):
        field_name = field_v1.type.of_type.name + '!'

    return field_name


def compare_existing_fields(type_name: str, type_v1: GraphQLObjectType, type_v2: GraphQLObjectType) -> list[dict]:
    """
    Compare existing fields between two versions of a type.

    Args:
        type_name (str): Name of the type.
        type_v1 (GraphQLObjectType): Version 1 of the GraphQL type.
        type_v2 (GraphQLObjectType): Version 2 of the GraphQL type.

    Returns:
        List[Dict]: List of changes for fields present in both versions.
    """
    changes = []
    for field_name, field_v1 in type_v1.fields.items():
        field_v2 = type_v2.fields.get(field_name)

        if not field_v2:
            changes.append(field_removed_change(type_name, field_name))

        else:
            # identity field type for the 2 features
            field_v1_type_name = get_field_type_name(field_v1)
            field_v2_type_name = get_field_type_name(field_v2)

            if field_v1_type_name != field_v2_type_name:
                changes.append(field_type_changed_change(type_name,
                                                         field_name,
                                                         field_v1_type_name,
                                                         field_v2_type_name)
                               )
            # comparing the arguments of the fields, if the types where the same
            changes.extend(compare_arguments(type_name, field_name, field_v1, field_v2))

    return changes


def field_type_changed_change(type_name: str, field_name: str, old_type, new_type) -> dict:
    """
    Create a change record for a field type change.

    Args:
        type_name (str): Name of the type.
        field_name (str): Name of the field.
        old_type: The old type of the field.
        new_type: The new type of the field.

    Returns:
        Dict: A change record indicating a field type change.
    """
    return {
        "type": type_name,
        "field": field_name,
        "change": f"Field type changed from '{old_type}' to '{new_type}'",
        "breaking": True,
        "release_note": f"The type of field '{field_name}' on type '{type_name}' has changed from '{old_type}' to '{new_type}'. This is a breaking change."
    }


def compare_new_fields(type_name: str, type_v1: GraphQLObjectType, type_v2: GraphQLObjectType) -> list[dict]:
    """
    Detect new fields added to a type in version 2.

    Args:
        type_name (str): The name of the type being compared.
        type_v1 (GraphQLObjectType): The first version of the GraphQL type.
        type_v2 (GraphQLObjectType): The second version of the GraphQL type.

    Returns:
        List[Dict]: List of changes for newly added fields.
    """
    changes = []
    for field_name, field_v2 in type_v2.fields.items():
        if field_name not in type_v1.fields:
            changes.append(new_field_added_change(type_name, field_name))

    return changes


def field_removed_change(type_name: str, field_name: str) -> dict:
    """
    Create a change record for a removed field.

    Args:
        type_name (str): Name of the type.
        field_name (str): Name of the removed field.

    Returns:
        Dict: A change record indicating a field removal.
    """
    return {
        "type": type_name,
        "field": field_name,
        "change": f"Field '{field_name}' was removed", #GE
        "breaking": True,
        "release_note": f"The field '{field_name}' on type '{type_name}' has been removed. Update any queries or mutations using this field."
    }


def new_field_added_change(type_name: str, field_name: str) -> dict:
    """
    Create a change record for a new field.

    Args:
        type_name (str): Name of the type.
        field_name (str): Name of the new field.

    Returns:
        Dict: A change record indicating a new field addition.
    """
    return {
        "type": type_name,
        "field": field_name,
        "change": f"Added new field '{field_name}'",
        "breaking": False,
        "release_note": f"A new field '{field_name}' has been added to '{type_name}'. This is a non-breaking change."
    }


# ----  check field arguments ---- #

def compare_arguments(type_name: str, field_name: str, field_v1, field_v2) -> list[dict]:
    """
    Compare arguments in fields between two versions of a type.

    Args:
        type_name (str): The name of the type containing the fields.
        field_name (str): The name of the field being compared.
        field_v1: The first version of the field.
        field_v2: The second version of the field.

    Returns:
        List[Dict]: List of changes detected at the argument level.
    """
    changes = []

    # create of arguments in each version for easier comparison
    old_args_list = set(list(field_v1.args.keys()))
    new_args_list = set(list(field_v2.args.keys()))

    # identify arguments present only in the old or new schema
    only_old_args = list(old_args_list - new_args_list)
    only_new_args = list(new_args_list - old_args_list)

    # no changes in this level
    if len(only_old_args) == 0 and len(only_new_args) == 0:
        return changes

    # single value replacement in this level
    elif len(only_old_args) == 1 and len(only_new_args)== 1:
        # definite replacement
        changes.append(argument_renamed_change(type_name,
                                               field_name, only_old_args[0],
                                               only_new_args[0]))

    # more changes in this level
    else:
        for old_param_name in only_old_args:
            # Remove and / or renamed
            changes.append(argument_removed_change(type_name, field_name, old_param_name))

        # Check for newly added parameters
        for new_param_name in only_new_args:
            changes.append({
                    "type": type_name,
                    "field": field_name,
                    "change": f"Added new input parameter '{new_param_name}'",
                    "breaking": False,
                    "release_note": f"The input parameter `{new_param_name}` has been added."
                })

    return changes


def argument_renamed_change(type_name: str, field_name: str, old_param_name: str, new_param_name: str) -> dict:
    """
    Create a change record for a renamed argument.

    Args:
        type_name (str): Name of the type.
        field_name (str): Name of the field.
        old_param_name (str): Old name of the argument.
        new_param_name (str): New name of the argument.

    Returns:
        Dict: A change record indicating an argument rename.
    """
    return {
        "type": type_name,
        "field": field_name,
        "change": f"Renamed input parameter '{old_param_name}' to '{new_param_name}'",
        "breaking": True,
        "release_note": f"The input parameter for `{field_name}` has been renamed from `{old_param_name}` to `{new_param_name}`. This is a breaking change, so make sure to update any queries that use `{old_param_name}` to `{new_param_name}`."
    }


def argument_removed_change(type_name: str, field_name: str, arg_name: str) -> dict:
    """
    Create a change record for a removed or renamed argument.

    Args:
        type_name (str): Name of the type.
        field_name (str): Name of the field.
        arg_name (str): Name of the argument that was removed or renamed.

    Returns:
        Dict: A change record indicating an argument removal.
    """
    return {
        "type": type_name,
        "field": field_name,
        "change": f"Renamed or removed argument '{arg_name}' in '{field_name}'",
        "breaking": True,
        "release_note": f"The argument '{arg_name}' has been removed or renamed in '{field_name}' on '{type_name}'. Update queries accordingly."
    }


# ---- main method --- #
def compare_schemas(schema_version1: GraphQLSchema,
                    schema_version2: GraphQLSchema) -> list[dict]:
    """
    Compare two GraphQL schemas and detect breaking/non-breaking changes.

    Args:
        schema_version1 (GraphQLSchema): The GraphQL schema in version 1 as a string.
        schema_version2 (GraphQLSchema): The GraphQL schema in version 2 as a string.

    Returns:
        List[Dict]: List of changes detected between the two schemas.
    """
    try:
        changes = compare_types(schema_version1, schema_version2)
        logging.info('Schema differences successfully identified.')


    except Exception as e:
        message = f"Unable to check differences in schema. Error comparing schemas: {e}"
        logging.error(message)
        changes = [
            {
            "status": "Failed",
            "reason": message
            }
        ]

    return changes

if __name__ == "__main__":
    import json
    from schema_diff_report import parse_schema
    schema_v1 = """ 
    scalar Status"""
    schema_v2= """ 
    scalar Status"""
    result = compare_schemas(parse_schema(schema_v1), parse_schema(schema_v2))
    print(json.dumps(result, indent=4))
