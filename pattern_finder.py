import re
import dateparser


def parse_date(input_string):
    parsed_date = dateparser.parse(input_string, date_formats=['%d.%m.%Y'])
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


# Function to process each phrase
def process_phrase(phrase):
    # Find the index of the first letter
    first_digit = re.search(r'(\d|[А-Я]{3})', phrase)
    first_digit_index = first_digit.start() if first_digit else 0

    # Find the index of the last digit
    last_digit = re.search(r'\d', phrase[::-1])
    last_digit_index = len(phrase) - last_digit.start() - 1 if last_digit else len(phrase)

    # Return the substring between the first letter and the last digit
    return phrase[first_digit_index:last_digit_index + 1]


def contain_digit(text):
    return any(char.isdigit() for char in text)


def find_info_in_list(phrases, pattern_dict):
    matching_info = {}

    for key, patterns in pattern_dict.items():
        found_match = False

        phrases_with_digit = [phrase for phrase in phrases if contain_digit(phrase)]
        strip_phrases = [process_phrase(phrase) for phrase in phrases_with_digit]
        sorted_phrases = sorted(strip_phrases, key=len, reverse=True)
        for phrase in sorted_phrases:
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
