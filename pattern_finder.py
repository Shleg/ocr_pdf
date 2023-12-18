import re


def find_info_in_list(phrases, pattern_dict):
    matching_info = {}

    for phrase in phrases:
        for key, pattern in pattern_dict.items():
            regex = re.compile(pattern)
            match = regex.search(phrase)

            if match:
                matching_info[key] = match.group()

    return matching_info or None
