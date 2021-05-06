from json import load
import re


def remove_duplicates(text):
    return list(dict.fromkeys([clean_text(i.lower()).strip() for i in text if i.strip()]))

def clean_text(text):

    replacements = {
        ".": " ",
        "(": "",
        ")": "",
    }

    for replacement in replacements:
        text = text.replace(replacement, replacements[replacement])

    return text

def is_number(text):
    text = text.replace(" ", "").replace("+","").replace("-", "")
    return text.isdigit() or text.replace("/","").isdigit()

def get_info(text, filename="regex_lookup.json"):

    text = text.strip()
    json_obj = load(open(filename))
    result_dict = {}

    for key in json_obj:
        if (result := [clean_text(found.group().strip()) for found in re.finditer(json_obj[key], text, re.IGNORECASE)]):
            if len(result) == 1:
                if is_number(result[0]):
                    # Todo: Extract Number
                    result_dict[key] = result

                else:
                    result_dict[key] = result[0]

            elif len(result) > 1:
                # Todo: Extract Number
                result_dict[key] = remove_duplicates(result)
            else:
                result_dict[key] = result
                
    return result_dict

if __name__ == "__main__":
    from pprint import pprint
    pprint(get_info(
            "hello oxygen plasma (A+, A-,o-, AB+) and cylinder concentrator required "
            "age 22 0132-2205379/78 +91-1234567890 asap verified needed"
            )
        )

