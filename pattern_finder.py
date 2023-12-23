import re


def find_matching_pattern_in_phrase(phrase, pattern):
    match = re.fullmatch(pattern, phrase)

    if match:
        return phrase  # Фраза полностью соответствует паттерну
    else:
        match = re.search(pattern, phrase)
        if match:
            return match.group()  # Возвращаем совпадение внутри фразы
        else:
            return None  # Совпадений не найдено

def find_info_in_list(phrases, pattern_dict):
    matching_info = {}
    found_match = False
    for phrase in phrases:
        for key, patterns in pattern_dict.items():
            for pattern in patterns:
                match = find_matching_pattern_in_phrase(phrase, pattern)

                if match:
                    matching_info[key] = match
                    found_match = True
                    break

            if found_match:
                break

        if found_match:
            break

    return matching_info or None
