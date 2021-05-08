from json import load
import re


def remove_duplicates(text):
    return list(dict.fromkeys([clean_text(i.lower()).strip() for i in text if i.strip()]))

def clean_text(text, replacement_string=None):
    replacements = {
        "  ": "",
        "\n": "",
        "(": " ",
        ")": " ",
    } if replacement_string is None else replacement_string

    for replacement in replacements:
        text = text.replace(replacement, replacements[replacement])

    return text

def is_number(text):
    replacements = {
        " " : "",
        "-" : "",
        "+": "",
        "\n": "",
        "\t": "",
        "/" : "",
        "\\": ""
    }

    temp = "".join(clean_text(text, replacements).split())

    if temp.isdigit() and (len(temp) in [*range(10, 15)]):
        return True
    return False

def get_info(text, existing_dict = None, filename="regex_lookup.json"):
    
    json_obj = load(open(filename))
    result_dict = existing_dict if existing_dict else {}

    for key in json_obj:
        if (result := [clean_text(found.group().strip()) for found in re.finditer(json_obj[key], text, re.IGNORECASE)]):
            if len(result) >= 1:
                result_dict[key] = result_dict.get(key, []) + remove_duplicates(result)
            else:
                result_dict[key] = result_dict.get(key, []) + result

            # Extract Phone Numbers
            result_dict[key] = [i for i in result_dict[key] if is_number(i)] if key=="Phone-Numbers" else result_dict[key]
            result_dict[key] = remove_duplicates(result_dict[key]) if type(result_dict[key]) == list else result_dict[key]

            if existing_dict:
                result_dict.update({
                    key: remove_duplicates(existing_dict[key] + result_dict[key])
                })

    return result_dict

if __name__ == "__main__":
    from pprint import pprint
    pprint(get_info(
            """hello oxygen plasma (A+, A-,o-, AB+) and cylinder concentrator required
               age 22 0132-2205379/78 +91-9763484463 asap verified needed hs@test.in ju2@hulu.com"""
            )
        )

