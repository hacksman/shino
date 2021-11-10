# coding: utf-8
# @Time : 9/14/21 10:43 AM


def to_unicode(text, encoding=None, errors='strict'):
    if isinstance(text, str):
        return text
    if not isinstance(text, bytes):
        raise TypeError(f"to_unicode must receive a bytes or str, got {type(text).__name__}")
    if encoding is None:
        encoding = 'utf8'
    return text.decode(encoding, errors)


def to_bytes(text, encoding=None, errors='strict'):
    if isinstance(text, bytes):
        return text
    if not isinstance(text, str):
        raise TypeError(f"to_bytes must receive a str or bytes, got {type(text).__name__}")
    if encoding is None:
        encoding = 'utf-8'
    return text.encode(encoding, errors)
