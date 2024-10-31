"""

Script generates the release summary, for a given release changes
list of dictionaries.

"""
import os
from dotenv import load_dotenv

# import packages
from gpt35_summarization import initialize_langchain

# Load environment variables from .env file
load_dotenv()

# get the api keyv
MY_API_KEY = os.getenv('MY_API_KEY')

def generate_release_summary(changes: list, summarization: str) -> dict:
    """
    Generate a release summary from the list of changes.

    Args:
        changes (list): A list of changes, each represented as a dictionary
                              containing details about the change.
        summarization (str): The technique for generating the summary could
            be: 'algorithmic' or 'LLM: GPT3.5'

    Returns:
        dict: A dictionary containing the release summary, including counts of
              breaking and non-breaking changes and a detailed summary.

    """
    # if the 2 schemas are identical, no summary will be generated
    if len(changes) == 0:
        return {
            "changes": changes,
            "release_notes": {
                "summary": 'No differences between the schemas.'
            }
        }

    # if the execution of compare_schemas failed
    elif len(changes) == 1 and 'status' in changes[0].keys():
        return {
            "changes": changes,
            "release_notes": {
                "summary": 'Unsuccessful identification of schema differences.'
            }
        }
    # successful identification of changes
    else:
        breaking_changes = [change for change in changes if change['breaking']]
        non_breaking_changes = [change for change in changes if not change['breaking']]

        breaking_count = len(breaking_changes)
        non_breaking_count = len(non_breaking_changes)

        breaking_change_messages = [format_change_message(change) for change in breaking_changes]
        non_breaking_change_messages = [format_change_message(change) for change in non_breaking_changes]

        summary = (
            f"This release introduces {breaking_count} breaking change(s) and "
            f"{non_breaking_count} non-breaking change(s): "
        )

        # adding messages in summary
        if summarization == 'algorithmic':
            if breaking_change_messages:
                summary += f"Breaking changes: {', '.join(breaking_change_messages)}. "
            if non_breaking_change_messages:
                summary += f"Non-breaking changes: {', '.join(non_breaking_change_messages)}."

        # calling LLM to create a summary
        elif summarization == 'GPT3.5':
            # call the GPT3.5 chain
            chain = initialize_langchain(api_key=MY_API_KEY)

            if breaking_change_messages:
                breaking_changes = "\n".join(breaking_change_messages)
                breaking_summary = chain.run({"schema_changes": breaking_changes})
                summary += f"Breaking changes: {breaking_summary}. "
            if non_breaking_change_messages:
                non_breaking_changes = "\n".join(non_breaking_change_messages)
                non_breaking_summary = chain.run({"schema_changes": non_breaking_changes})
                summary += f"Non-breaking changes: {non_breaking_summary}."

        return {
            "changes": changes,
            "release_notes": {
                "summary": summary
            }
        }


def format_change_message(change: dict) -> str:
    """

    Format a change message based on available keys in the change dictionary,
    and omit the field name if the change starts with 'Added' or 'Removed'.

    """

    change_message = change['change']
    type_name = change.get('type')
    field_name = change.get('field')

    if type_name and field_name:
        # If both type_name and field_name exist, check for 'Added'/'Removed'
        if change_message.startswith(('Added', 'Removed')):
            return f"{change_message} in {type_name}"
        else:
            return f"{change_message} in {type_name} '{field_name}'"

    else:
        # for additions or removals on the base level
        return change_message
