"""

Script calls GPT3.5 model to identify changes in a GraphQL schema.

"""
# import packages
import openai
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# get the api key
MY_API_KEY = os.getenv('MY_API_KEY')

# Initialize the OpenAI client
client = openai.OpenAI(api_key=MY_API_KEY)

def analyze_schema_changes(schema_v1, schema_v2):
    # Prepare the messages for the chat
    messages = [
        {"role": "user", "content": "Forget all previous interactions."},
        {"role": "system",
         "content": "You are a helpful assistant that identifies breaking and non-breaking changes in GraphQL schemas."},
        {"role": "user", "content": f"""

        Given two versions of a GraphQL schema, identify ALL breaking and non-breaking
        changes between them and format them as a JSON array of changes.

        Schema Version 1:
        {schema_v1}

        Schema Version 2:
        {schema_v2}

        Ensure each change has a 'type', 'field', 'change', 'breaking' (true/false), and 'release_note'.
        
        Type should always have the name of the type that the change was located in: example: type Name1.
        For type level changes field is none.
        For field-level or argument level changes, field should have the name of the field the change
        was located in, and the Type should have the type name the feature belongs to.
        
        The change message should refer the type and feature values if applicable.
                      
        The 'release_note' for each change should:
        1. Describe the change in a short phrase. 
        2. Explicitly mention if it is breaking or non-breaking change, appending
        the description sentence with 'this is a breaking (or non-breaking) change.'.
        3. If possible, for breaking the changes, mention how it will affect future
        queries, in a second sentence.
                     
        """}
    ]

    # Make the API call using the new chat completion method
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=4096,
        temperature=0
    )

    # Access the response content
    changes = response.choices[0].message.content.strip()

    # Parse the response text to JSON
    try:
        # Remove the 'json' prefix
        changes = changes.replace("json", "", 1).strip()
        # Replace backticks with nothing
        changes = changes.replace('```', '').strip()
        # Parse the JSON string
        changes = json.loads(changes)

    except json.JSONDecodeError:
        changes = {"error": "Failed to parse the response. Please check the model's output format."}

    return changes


# Example usage with provided schemas
if __name__ == "__main__":
    schema_v1 = """scalar Status


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
            ratings(minScore: Int = 1, maxScore: Int = 6): [Int!]
        }

        type Query {
            getBookById(id: ID!): Book
            getAllBooks: [Book]
        }

        type Mutation {
            addBook(title: String!, author: String!, publishedYear: Int, genre: String): Book
        }
    }"""

    schema_v2 = """enum Status {
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
            publishedYear: Int!
            genre: ID
            ratings(minScore: Int = 1, maxScore: Int = 5): [Int!]!
        }

        type Query {
            getBookById(id: ID!): Book
        }

        type Mutation {
            addBook(title: String!, author: String!, publishedYear: Int, genre: String): Book
        }
    }"""



    output = analyze_schema_changes(schema_v1, schema_v2)
    print(json.dumps(output, indent=2))
