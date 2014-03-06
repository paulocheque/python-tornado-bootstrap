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
    a_list = smart_split(text_or_list, comma=comma)
    a_list = to_lower_case(a_list)
    if a_list and isinstance(a_list, (list, set)):
        a_list = map(lambda x: x.strip(), a_list)
        a_list = filter(str, a_list)
        a_list = list(set(a_list))
    return a_list
