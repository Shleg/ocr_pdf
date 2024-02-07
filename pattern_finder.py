import re
import dateparser


def parse_date(input_string):
    parsed_date = dateparser.parse(input_string)
    if parsed_date:
        formatted_date = parsed_date.strftime('%d.%m.%Y')
        return formatted_date
    else:
        return None  # Если не удалось распознать дату, возвращаем None


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

    for key, patterns in pattern_dict.items():
        found_match = False
        for phrase in sorted(phrases):
            for pattern in patterns:
                match = find_matching_pattern_in_phrase(phrase, pattern)

                if match:
                    if key == 'date':
                        matching_info[key] = parse_date(match)
                    else:
                        matching_info[key] = match
                    found_match = True
                    break

            if found_match:
                break

    return matching_info or None
