import re
from json import load


def clean_text(text):

    replacements = {
        " ": "",
        ".": "",
        ",": ", ",
        "(": "",
        ")": "",
        "-": ""
    }

    for replacement in replacements:
        text = text.replace(replacement, replacements[replacement])

    return text
    
def get_info(text, filename="regex_lookup.json"):

    text = text.strip()
    json_obj = load(open(filename))
    result_dict = {}

    for key in json_obj:
        
        if (result := [clean_text(found.group().strip()) for found in re.finditer(json_obj[key], text, re.IGNORECASE)]):
            if len(result) == 1:
                result_dict[key] = result[0] if result[0].isdigit() or result[0].replace("/","").isdigit() else True
            else:
                result_dict[key] = result

    return result_dict

if __name__ == "__main__":
    from pprint import pprint
    pprint(get_info("hello oxygen required 0132-2205379 +91-1234567890 asap verified needed"))

