"""

Script initializes the GPT3.5 model, to summarize the
changes encountered between 2 versions of a GraphQL schema.

"""
# import packages
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain


def initialize_langchain(api_key: str) -> LLMChain:
    """
    Initializes the LangChain components for combining GraphQL schema change descriptions
    using the OpenAI language model.

    This function sets up the OpenAI model (GPT-3.5 Turbo) and a prompt template designed
    to guide the model in synthesizing multiple sentences describing changes in a GraphQL
    schema into coherent descriptions.

    Args:
        api_key (str): The API key for accessing the OpenAI service. This key is required
                       for authenticating requests to the OpenAI API.

    Returns:
        LLMChain: An instance of the LangChain LLMChain configured with the initialized
                  OpenAI model and prompt template.

    """
    # Initialize the OpenAI model
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=api_key,  # Use the provided OpenAI API key
        temperature=0.3,  # Adjust for more or less creativity in responses
    )

    # Define a prompt template to guide the model in combining the sentences
    prompt_template = PromptTemplate(
        input_variables=["schema_changes"],
        template=(
            "Here are some sentences describing changes in a GraphQL schema:\n"
            "{schema_changes}\n"
            "Combine these changes into one or two coherent descriptions of the overall schema updates."
        ),
    )

    # Set up the LangChain chain with the prompt and model
    chain = LLMChain(llm=llm, prompt=prompt_template)

    return chain