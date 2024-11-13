import pandas as pd
import re
from unidecode import unidecode

# Load the data
df = pd.read_csv('Code_HE_PFE_original.csv')
df.head()

def generate_default_code(name):
    code = ""
    # Remove any special characters from the name
    name = unidecode(name)
    # Split the name into words
    words = name.split()

    for word in words:
        # Ignore "de", "DE", or "De"
        if word.lower() in ["de", "et", "la", "le", "les", "des", "du", "d'"]:
            continue

        # Check if the word is inside brackets
        if word.startswith('[') and word.endswith(']'):
            # Extract the type inside brackets and append it to the code in the specified format
            type_code = word[1:-1]
            code += f"_{type_code}"

        # Check if the word starts with a number and ends with "ML" or "ml"
        elif re.match(r"^\d+ml$", word, re.IGNORECASE):
            # Add the whole number+ml to the code
            code += word.upper()
        else:
            # Otherwise, add the first 3 characters of the word (if available)
            code += word[:3].upper()

    return code

# Apply the function to generate default_code for each row
df['default_code'] = df['name'].apply(generate_default_code)

# Save the updated DataFrame back to a CSV file
df.to_csv('Code_HE_PFE_updated.csv', index=False)
