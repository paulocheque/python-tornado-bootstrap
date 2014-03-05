# coding: utf-8


def smart_split(text, comma=','):
    if isinstance(text, (str, unicode)):
        text = text.strip()
        text = text.split(comma)
        text = map(lambda x: x.strip(), text)
        text = filter(str, text)
        text = list(set(text))
    return text


def to_lower_case(text):
    if text:
        if isinstance(text, (str, unicode)):
            text = text.lower()
        elif isinstance(text, (list, set)):
            text = map(lambda x: x.lower(), text)
    return text


def taggify(text_or_list, comma=','):
    text_or_list = smart_split(text_or_list, comma=comma)
    text_or_list = to_lower_case(text_or_list)
    if text_or_list and isinstance(text_or_list, (list, set)):
        text_or_list = map(lambda x: x.strip(), text_or_list)
        text_or_list = filter(str, text_or_list)
        text_or_list = list(set(text_or_list))
    return text_or_list
