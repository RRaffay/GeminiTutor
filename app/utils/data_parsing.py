import json
from datetime import datetime

def parse_questions(questions):
    """
    Parse the input string and extract the JSON substring.

    Args:
        questions (str): The input string containing JSON data.

    Returns:
        dict: A Python dictionary representing the parsed JSON data.
    """
    # Extract the JSON substring from the input string
    start = questions.index('{')
    end = questions.rindex('}') + 1
    json_string = questions[start:end]

    # Parse the JSON string into a Python dictionary
    data = json.loads(json_string)
    return data
def sort_timestamped_data(data, key='timestamp', return_num=5):
    """
    Sort a list of dictionaries containing timestamped data.

    Args:
        data (list): A list of dictionaries containing timestamped data.
        key (str): The key in the dictionary corresponding to the timestamp.
        return_num (int): The number of sorted items to return.

    Returns:
        list: A list of dictionaries sorted by the timestamp.
    """
    # Helper function to parse the timestamp into a datetime object

    # Sorting the data by timestamp in descending order
    sorted_data = sorted(data, key=lambda entry: datetime.fromisoformat(entry[key]), reverse=True)

    # Return the top N entries
    return sorted_data[:return_num]

def main():
    pass


if __name__ == "__main__":
    main()
