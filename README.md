# Identify changes in a GraphQL Schema

## Project Description
The module identifies all the breaking and non-breaking changes between 2 versions
of a GraphQL schema. 
- Each change is provided with its own release notes.
- Finally, all the changes are summarized in a single paragraph.
- The summarization is executed either algorithmically, or by employing OpenAI's GPT3.5 model.  

## Components
- FAST-API app
- Python Source code


## Installation

### Python Version

- Python 3.12

### Steps

To get started with graph-schema-diff, follow these steps:

1. Clone the repository:
   ```bash
   https://github.com/GeorgiosEtsias/graph-schema-diff.git
   ```
2. Navigate to the project directory:
   ```bash
   cd graph-schema-diff
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Launch the FAST-API app: main-fastapi.py script
2. Access the app through the browser: http://127.0.0.1:8000/docs 
3. Import the schema1 and schema2 in the designated boxes (keep only the schema, no starting """ """ needed.)
4. Choose summarization technique: 'algorithmic' or 'GPT3.5'.
5. Generate the results.

![img_1.png](img_1.png)

### Prerequisites
To use GPT3.5 as a summarization technique, you need to add your own API-KEY in the  release_summary.py script.

## Project Structure

```
├── graph-schema-diff
│   ├── src/
│   │   ├── gpt35_summarization.py
│   │   ├── main-fastapi.py
│   │   ├── release_summary.py
│   │   ├── schema_changes.py
│   │   ├── schema_diff_report.py
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_graphql_diff.py
│   ├── README.md
│   ├── requirements.txt
│   ├── run_unit_tests.sh
│   ├── run_unit_tests_with_coverage.sh
```

## Project Summary

- **`src/`**: Contains the python package.
  - `__init__.py`: Marks the directory as a Python package and can be used to expose specific functions.
  - `gpt35_summarization.py`: Script initializes the GPT3.5 model, to summarize the changes encountered between 2 versions of a GraphQL schema.
  - `main-fastapi.py`: Script launches a fast-api app, that enables the user  to test the changes between 2 versions fo a GraphQL schema.
  - `release_summary.py`: Script generates the release summary, for a given release changes list of dictionaries.
  - `schema_changes.py`: Script to identify all the differences between two versions of a GraphQL schema.
  - `schema_diff_report.py`: Script determines all the breaking and non-breaking changes between 2 versions of a GraphQL schema, and generates a summary report.


- **`tests/`**: Includes all tests and test files.
  - **`unit/`**: Contains unit tests.
    - `test_graphql_diff.py`: Unit tests the main method of schema_diff_report.py

- `README.md`: Provides documentation for the project, explaining the project setup, usage, and configuration.
- `requirements.txt`: Lists all Python library dependencies for the project.

### Example data:
##### Schema Version1
```
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
```

##### Schema Version2
```
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
```
##### Expected output
```
{
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
```

## Author
- Georgios Etsias: etsiasg@hotmail.gr