"""

Unit-test the main method in schema_diff_report
All test cases, are simple, a single breaking or non-breaking change.

"""
# import the tested module
from schema_diff_report import graphql_diff_report

def test_compare_schemas_non_breaking_new_feature():
    """

    Tests detection of a new field in the schema.

    """
    schema_v1 = """
    type Query {
        hello: String
    }
    
    """
    schema_v2 = """
    type Query {
        hello: String
        goodbye: String
    }
    """
    expected_result = {
    "changes": [
    {
      "type": "Query",
      "field": "goodbye",
      "change": "Added new field 'goodbye'",
      "breaking": False,
      "release_note": "A new field 'goodbye' has been added to 'Query'. This is a non-breaking change."
    }],
    "release_notes": {
    "summary": "This release introduces 0 breaking change(s) and 1 non-breaking change(s): Non-breaking changes: Added new field 'goodbye' in Query."
    }}

    # Act
    changes = graphql_diff_report(schema_v1, schema_v2, 'algorithmic', 'algorithmic')

    # Assert
    assert changes == expected_result


def test_compare_schemas_type_removed():
    """
    Tests detection of a breaking change when a type is removed.
    """
    schema_v1 = """
    type Query {
        hello: String
    }
    
    type Weather
    
    """
    schema_v2 = """
    type Query {
        hello: String
    }
    """
    expected_result = {
  "changes": [
    {
      "type": "Weather",
      "change": "Type 'Weather' was removed",
      "breaking": True,
      "release_note": "The type 'Weather' has been removed. This is a breaking change and will affect any queries relying on this type."
    }
  ],
  "release_notes": {
    "summary": "This release introduces 1 breaking change(s) and 0 non-breaking change(s): Breaking changes: Type 'Weather' was removed. "
  }
}

    changes = graphql_diff_report(schema_v1, schema_v2, 'algorithmic','algorithmic')
    assert changes == expected_result


def test_compare_schemas_type_type_changed():
    """
    Tests detection of a breaking change when the type of a field is changed.
    """
    schema_v1 = """
    type Query {
        hello: String
    }
    """
    schema_v2 = """
    interface  Query {
        hello: String
    }
    """
    expected_result = {
  "changes": [
    {
      "type": "Query",
      "change": "Type changed from 'GraphQLObjectType' to 'GraphQLInterfaceType'",
      "breaking": True,
      "release_note": "The type 'Query' has changed from 'GraphQLObjectType' to 'GraphQLInterfaceType'. This is a breaking change."
    }
  ],
  "release_notes": {
    "summary": "This release introduces 1 breaking change(s) and 0 non-breaking change(s): Breaking changes: Type changed from 'GraphQLObjectType' to 'GraphQLInterfaceType'. "
  }
}

    changes = graphql_diff_report(schema_v1, schema_v2, 'algorithmic','algorithmic')
    assert changes == expected_result


def test_compare_schemas_type_feature_removed():
    """
    Tests detection of a breaking change when a feature is removed.
    """
    schema_v1 = """
    type Query {
        hello: String
        goodbye: String
    }
    """
    schema_v2 = """
    type Query {
        hello: String
    }
    """
    expected_result = {
  "changes": [
    {
      "type": "Query",
      "field": "goodbye",
      "change": "Field 'goodbye' was removed",
      "breaking": True,
      "release_note": "The field 'goodbye' on type 'Query' has been removed. Update any queries or mutations using this field."
    }
  ],
  "release_notes": {
    "summary": "This release introduces 1 breaking change(s) and 0 non-breaking change(s): Breaking changes: Field 'goodbye' was removed in Query 'goodbye'. "
  }
}

    changes = graphql_diff_report(schema_v1, schema_v2, 'algorithmic','algorithmic')
    assert changes == expected_result

#WRONG FIX IT
def test_compare_schemas_feature_type_changed():
    """
    Tests detection of a breaking change when the type of a field is changed.
    """
    schema_v1 = """
    type Query {
        hello: String
    }
    """
    schema_v2 = """
    type Query {
        hello: Int
    }
    """
    expected_result ={
    "changes": [
    {
      "type": "Query",
      "field": "hello",
      "change": "Field type changed from 'String' to 'Int'",
      "breaking": True,
      "release_note": "The type of field 'hello' on type 'Query' has changed from 'String' to 'Int'. This is a breaking change."
    }
  ],
  "release_notes": {
    "summary": "This release introduces 1 breaking change(s) and 0 non-breaking change(s): Breaking changes: Field type changed from 'String' to 'Int' in Query 'hello'. "
  }
}

    changes = graphql_diff_report(schema_v1, schema_v2, 'algorithmic','algorithmic')
    assert changes == expected_result

# this is the real mistake
def test_compare_schemas_type_add():
    """
    Tests detection of a non-breaking change when a new type is added.
    """
    schema_v1 = """
    type Query {
        hello: String
    }
    """
    schema_v2 = """
    type Query {
        hello: String
    }
    type Weather {
        temperature: Int
    }
    """
    expected_result = {
        "changes": [
            {
                "type": "Weather",
                "change": "Added new type 'Weather'",
                "breaking": False,
                "release_note": "A new type 'Weather' has been added. This is a non-breaking change."
            }
        ],
        "release_notes": {
            "summary": "This release introduces 0 breaking change(s) and 1 non-breaking change(s): Non-breaking changes: Added new type 'Weather'."
        }
    }

    changes = graphql_diff_report(schema_v1, schema_v2, 'algorithmic','algorithmic')
    assert changes == expected_result


def test_compare_schemas_feature_added():
    """
    Tests detection of a non-breaking change when a new field is added.
    """
    schema_v1 = """
    type Query {
        hello: String
    }
    """
    schema_v2 = """
    type Query {
        hello: String
        goodbye: String
    }
    """
    expected_result = {
        "changes": [
            {
                "type": "Query",
                "field": "goodbye",
                "change": "Added new field 'goodbye'",
                "breaking": False,
                "release_note": "A new field 'goodbye' has been added to 'Query'. This is a non-breaking change."
            }
        ],
        "release_notes": {
            "summary": "This release introduces 0 breaking change(s) and 1 non-breaking change(s): Non-breaking changes: Added new field 'goodbye' in Query."
        }
    }

    changes = graphql_diff_report(schema_v1, schema_v2, 'algorithmic','algorithmic')
    assert changes == expected_result


def test_compare_schemas_argument_added():
    """
    Tests detection of a non-breaking change when a new argument is added.
    """
    schema_v1 = """
    type Query {
        getWeather: String
    }
    """
    schema_v2 = """
    type Query {
        getWeather(location: String): String
    }
    """
    expected_result = {
  "changes": [
    {
      "type": "Query",
      "field": "getWeather",
      "change": "Added new input parameter 'location'",
      "breaking": False,
      "release_note": "The input parameter `location` has been added."
    }
  ],
  "release_notes": {
    "summary": "This release introduces 0 breaking change(s) and 1 non-breaking change(s): Non-breaking changes: Added new input parameter 'location' in Query."
  }
}

    changes = graphql_diff_report(schema_v1, schema_v2, 'algorithmic','algorithmic')
    assert changes == expected_result


def test_compare_schemas_no_change():
    """
    Tests detection of no changes.
    """
    schema_v1 = """
    type Query {
        hello: String
    }
    """
    schema_v2 = """
    type Query {
        hello: String
    }
    """
    expected_result = {
        "changes": [],
        "release_notes": {
            "summary": "No differences between the schemas."
        }
    }

    changes = graphql_diff_report(schema_v1, schema_v2, 'algorithmic','algorithmic')
    assert changes == expected_result


def test_compare_schemas_cannot_be_parsed():
    """
    Tests handling of an error when schemas cannot be parsed.
    """
    schema_v1 = """
    type Query {
        hello: String
    }
    """
    schema_v2 = "Invalid schema"

    expected_result = {
        "changes": [
            {
                "status": "error",
                "message": "Schema parsing failed"
            }
        ],
        "release_notes": {
            "summary": "Unsuccessful identification of schema differences."
        }
    }

    changes = graphql_diff_report(schema_v1, schema_v2, 'algorithmic','algorithmic')
    assert changes["parsing_failed"][0] == "Version 2 of the GraphQL schema could not be parsed"


def test_multi_change_schema():
    """
    Check 2 schema versions with multiple breaking and non-breaking changes
    """

    schema_v1 = """ 
        scalar Status

        enum Role {
            ADMIN
            ACTIVE
        }

        schema {
            query: Query
            mutation: Mutation
        }

        type Character {
        id: ID!
        name: String!
        }

        type OldCharacter {
        id: ID!
        name: String!
        }

        type Book {
            id: ID!
            title: String!
            author: String!
            publishedYear: Int
            genre: String!
            ratings(minScore: Int = 1, maxScore: Int = 6): [Int!]!
        }

        type Query {
            getBookById(id: ID!): Book
            getAllBooks: [Book]
        }

        type Mutation {
            addBook(title: String!, author: String!, publishedYear: Int, genre: String): Book
        }

        """

    schema_v2 = """ 
        enum Status {
            ACTIVE
            INACTIVE
        }

        enum Role {
            ADMIN
            USER
            GUEST
        }

        interface Character {
        id: ID!
        name: String!
        }


        schema {
            query: Query
            mutation: Mutation
        }

        type Book {
            id: Int
            title: String!
            author: String
            publishedYear: Int
            genre: ID
            ratings(minScore: Int = 1, maxScore: Int = 5): [Int!]!
        }

        type Query {
            getBookById(id: ID!): Book
        } 

        type Mutation {
            addBook(title: String!, author: String!, publishedYear: Int, genre: String): Book
        }   

        """

    expected_result = {
  "changes": [
    {
      "type": "Status",
      "change": "Type changed from 'GraphQLScalarType' to 'GraphQLEnumType'",
      "breaking": True,
      "release_note": "The type 'Status' has changed from 'GraphQLScalarType' to 'GraphQLEnumType'. This is a breaking change."
    },
    {
      "type": "Role",
      "change": "Value 'ACTIVE' was removed",
      "breaking": True,
      "release_note": "Value 'ACTIVE' on enum type 'Role' has been removed. Update any queries or mutations using this field."
    },
    {
      "type": "Role",
      "change": "Added new value 'USER'",
      "breaking": False,
      "release_note": "A new value 'USER' has been added to enum type 'Role'. This is a non-breaking change."
    },
    {
      "type": "Role",
      "change": "Added new value 'GUEST'",
      "breaking": False,
      "release_note": "A new value 'GUEST' has been added to enum type 'Role'. This is a non-breaking change."
    },
    {
      "type": "Character",
      "change": "Type changed from 'GraphQLObjectType' to 'GraphQLInterfaceType'",
      "breaking": True,
      "release_note": "The type 'Character' has changed from 'GraphQLObjectType' to 'GraphQLInterfaceType'. This is a breaking change."
    },
    {
      "type": "OldCharacter",
      "change": "Type 'OldCharacter' was removed",
      "breaking": True,
      "release_note": "The type 'OldCharacter' has been removed. This is a breaking change and will affect any queries relying on this type."
    },
    {
      "type": "Book",
      "field": "id",
      "change": "Field type changed from 'ID!' to 'Int'",
      "breaking": True,
      "release_note": "The type of field 'id' on type 'Book' has changed from 'ID!' to 'Int'. This is a breaking change."
    },
    {
      "type": "Book",
      "field": "author",
      "change": "Field type changed from 'String!' to 'String'",
      "breaking": True,
      "release_note": "The type of field 'author' on type 'Book' has changed from 'String!' to 'String'. This is a breaking change."
    },
    {
      "type": "Book",
      "field": "genre",
      "change": "Field type changed from 'String!' to 'ID'",
      "breaking": True,
      "release_note": "The type of field 'genre' on type 'Book' has changed from 'String!' to 'ID'. This is a breaking change."
    },
    {
      "type": "Query",
      "field": "getAllBooks",
      "change": "Field 'getAllBooks' was removed",
      "breaking": True,
      "release_note": "The field 'getAllBooks' on type 'Query' has been removed. Update any queries or mutations using this field."
    }
  ],
  "release_notes": {
    "summary": "This release introduces 8 breaking change(s) and 2 non-breaking change(s): Breaking changes: Type changed from 'GraphQLScalarType' to 'GraphQLEnumType', Value 'ACTIVE' was removed, Type changed from 'GraphQLObjectType' to 'GraphQLInterfaceType', Type 'OldCharacter' was removed, Field type changed from 'ID!' to 'Int' in Book 'id', Field type changed from 'String!' to 'String' in Book 'author', Field type changed from 'String!' to 'ID' in Book 'genre', Field 'getAllBooks' was removed in Query 'getAllBooks'. Non-breaking changes: Added new value 'USER', Added new value 'GUEST'."
  }
}

    changes = graphql_diff_report(schema_v1, schema_v2, 'algorithmic','algorithmic')
    assert changes == expected_result
